import requests
from datetime import datetime
import lightgbm
import joblib
from kokoa.models.user_model import SubwayPassenger
from datetime import datetime

def gangnamBike(q=None):
    if q:
        if q=='1':# 주차된 따릉이 개수
            return f"현재 강남역 근처 5개 대여소에 주차된 따릉이는 총 {getBikeNow()}대 입니다."
        elif q=='2':#기상상태
            w = getWeather()
            return f"현재기온 : {w['temp']}도 , 습도 : {w['humid']}, 풍속 : {w['wind']}, 강수 : {w['rain']}, 적설 : {w['snow']}"
        elif q=='3':#강남역인근 코로나확진자수
            today,cnt,gang = getCoronaToday()
            return f"[최신]서울시의 {today} 확진자 수는 {cnt}명, 역근처인 강남구 및 서초구의 촥진자 수는 {gang}명 입니다. 데이터는 매일 오전 11시 갱신됩니다."
            # return getCoronaToday()
        elif q=='4':
            #TODO 이후 대여량 예측에 대한 모델 답변이 들어갈 부분
            return getNextPredict()
        else:
            return greeting()
    else:#Greeting with Question List
        return greeting()
    return 'None'

def greeting():
    return """
        알려드릴 수 있는 것들입니다. 
        1. 현재 주차된 따릉이 개수\n
        2. 현재 날씨\n
        3. 강남역 인근 코로나 확진자 수 \n
        4. 1시간 뒤 남은 자전거 수 예측\n
        (ex답변 : 1)
        """
def getBikeNow():
    KEY = '62744744686579653130355443705368'
    result2 = requests.get(f'http://openapi.seoul.go.kr:8088/{KEY}/json/bikeList/1001/2000/').json()['rentBikeStatus']['row']
    parked = 0 #잔여량
    for i in  [result2[533], result2[680], result2[682], result2[708], result2[715]]:
        parked += int(i['parkingBikeTotCnt'])
    return parked

def getWeather():
    seoul = 'Seoul,KR'
    api='19ab005fa1e4604eaa9fc53eb702346a'
    results = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={seoul}&APPID={api}&units=metric')
    result = results.json()
    temperature = result['main']['temp']#기온
    humidity = result['main']['humidity']#습도
    wind_speed = result['wind']['speed']#풍속
    try: 
        rain = result['rain']#강수
    except:
        rain = 0
    try:
        snow = result['snow']#적설
    except:
        snow = 0
    return {'temp':temperature, 'humid':humidity,'wind':wind_speed,'rain':rain,'snow':snow}

def getCoronaToday():
    KEY = '62744744686579653130355443705368'
    corurl=f'http://openapi.seoul.go.kr:8088/{KEY}/json/Corona19Status/1/999/'
    r = requests.get(corurl)
    result = r.json()
    today = r.json()['Corona19Status']['row'][0]['CORONA19_DATE']
    cnt=0
    gang=0
    for i in (r.json())['Corona19Status']['row']:
        if i['CORONA19_DATE']=='2021-03-27':
            # print(i)
            cnt+=1
            if i['CORONA19_AREA']=='강남구' or i['CORONA19_AREA']=='서초구':
                gang+=1
    return today,cnt,gang
    # return f"[최신]서울시의 {today} 확진자 수는 {cnt}명, 역근처인 강남구 및 서초구의 촥진자 수는 {gang}명 입니다. 데이터는 매일 오전 11시 갱신됩니다."

def getNextPredict():
    lgb= joblib.load('./lgb.pkl')
    _, cnt ,gang = getCoronaToday()
    w = getWeather() #temp, humid, wind, rain, snow
    bikenow = getBikeNow()
    if datetime.now().weekday():#평일 ==1
        holiday = False
    else: holiday = True
    hour = datetime.now().hour #시간
    month = datetime.now().month #월
    day = datetime.now().day #일
    subway = SubwayPassenger.query.filter(SubwayPassenger.hour==hour, SubwayPassenger.month==month).filter(SubwayPassenger.holiday==holiday).first()
    # 기온	강수량	풍속	습도	적설	month	day	hour	코로나확진자수	승차	하차	휴일
    modelinput = [[w['temp'],w['rain'],w['wind'],w['humid'],w['snow'],month,day,hour,gang,subway.insub, subway.outsub, holiday  ]]
    pred = int(lgb.predict(modelinput))
    return f"다음 1시간 동안 {pred}대의 대여량이 발생할 것으로 예측됩니다."

