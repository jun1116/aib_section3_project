# aib_section3_project
CodeStates_AI_Bootcamp_Section_3_Project_Repo  
섹션 3 - 프로젝트 폴더
## Gangnam Talk 
이 어플리케이션은 카카오톡의 UI를 그대로 만들어 사용하였으며, 2020년 12월 NOMAD CODER의 KAKAOTALK CLONE coding 강좌를 들으며 배웠던 내용을 기초하여 HTML과 CSS를 구성하였습니다. 

```bash
|-- __pycache__
|-- func
|   |-- company_answer.py
|   |-- func_gangnamBike.py
|
|-- kokoa
|   |-- __init__.py
|   |
|   |-- models
|   |   |-- user_model.py
|   |
|   |-- routes
|   |   |-- main_route.py
|   |   |-- chat_route.py
|   |   |-- find_route.py
|   |
|   |-- static
|   |   |-- css (생략)
|   |   |   |-- components
|   |   |   |-- screens
|   |   |-- images
|   |
|   |-- templates
|   |   |   |-- base
|   |   |   |   |-- base.html
|   |   |   |   
|   |   |   |-- index.html
|   |   |   |-- friends.html
|   |   |   |-- chats.html
|   |   |   |-- chatdetail.html
|   |   |   |-- find.html
|   |   |   |-- settings.html
|   |
|   |-- models
|   |   |-- user_model.py
|   
|-- migrations (생략)
|-- lgb.pkl (모델)
|-- config.py 
|-- Procfile
|-- requirements.txt
|-- runtime.txt
```

<center><img src="https://github.com/jun1116/aib_section3_project/blob/main/imagesFolder/db_scheme.png?raw=true" width="700" height="500"></center>

> 각종 업체 또는 단체의 챗봇을 제공하는 것을 주요 기능으로 합니다.  
현재 강남역 근처 따릉이를 운영하는 가상의 사업체를 가정하여 그를 통해 정보를 받아보는 것을 구현하였습니다. 

## 주요 기능
### 로그인, 로그아웃 및 계정 삭제

첫화면 | 이미존재하는 계정|계정 생성 성공 | 비밀번호 실패
:---:|:---:|:---:|:---:
![](https://github.com/jun1116/aib_section3_project/blob/main/imagesFolder/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202021-03-31%20%E1%84%8B%E1%85%A9%E1%84%8C%E1%85%A5%E1%86%AB%201.31.26.png?raw=true)|![](https://github.com/jun1116/aib_section3_project/blob/main/imagesFolder/login_1_%EC%9D%B4%EB%AF%B8%EC%A1%B4%EC%9E%AC%ED%95%98%EB%8A%94%EA%B3%84%EC%A0%95.png?raw=true) | ![](https://github.com/jun1116/aib_section3_project/blob/main/imagesFolder/login_2_%EA%B3%84%EC%A0%95%EC%83%9D%EC%84%B1%EC%84%B1%EA%B3%B5.png) | ![](https://github.com/jun1116/aib_section3_project/blob/main/imagesFolder/login_3_%EB%B9%84%EB%B0%80%EB%B2%88%ED%98%B8%EC%8B%A4%ED%8C%A8.png)

기본 화면에서 만들고 싶은 계정의 이름과 비밀번호 입력후, Sign Up 버튼을 통하여 계정 생성을 할 수 있으며, 그렇게 계정을 생성한 후, Log In 버튼을 사용하여 해당 계정으로 로그인 합니다.   
위 과정에서 이미 존재하는 이름의 계정을 사용할 경우 유저생성에 실패하며 다른 이름을 사용해야하며, 로그인과정에서 비밀번호가 틀릴 경우 또한, 다시 로그인을 진행해야합니다.

### 로그인 후 첫 화면
![로그인후첫화면](https://github.com/jun1116/aib_section3_project/blob/main/imagesFolder/comp_1_%EB%A1%9C%EA%B7%B8%EC%9D%B8%ED%9B%84%EC%B2%AB%ED%99%94%EB%A9%B4.png){: width="200" height="400"){: .center}
현재 채팅이 가능한 회사들의 목록을 확인할 수 있으며, 해당 회사를 클릭하여 새로운 채팅을 진행할 수 있습니다.

#### 로그인 후, 회사 클릭을 통한 채팅 시작
첫화면 | 대화 및 답변 예시
:---:|:---:
![](https://github.com/jun1116/aib_section3_project/blob/main/imagesFolder/chatdetail_1_%EA%B0%95%EB%82%A8%EB%94%B0%EB%A6%891.png) | ![](https://github.com/jun1116/aib_section3_project/blob/main/imagesFolder/chatdetail_1_%EA%B0%95%EB%82%A8%EB%94%B0%EB%A6%891.png)

현재 자연어 처리 모델이 도입되지 않은 상황이라, 기능이 제한적입니다.   
임시로 구현해놓은 '강남따릉이' 의 경우 4가지 기능을 사용할 수 있으며, 각각의 입력에 따라, 실시간으로 서울시 API를 통하여, 
1. 현재 강남역 근처 5개 대여소의 주차된 따릉이 대수
2. 현재 날씨
3. 인근 코로나 확진자 수
4. 향후 1시간 동안 대여량 예측  

을 답변으로 받아볼 수 있습니다.  

위 화면에서 채팅창에 입력을 통하여 메시지를 주고받을 수 있으며, 대화를 마치고나면 뒤로가기버튼 (<) 또는 휴지통버튼을 통하여, 채팅목록으로 돌아가거나, 해당 채팅내역을 삭제할 수 있습니다. 

### 채팅방 목록
<center><img src="https://github.com/jun1116/aib_section3_project/blob/main/imagesFolder/chats_1_%EC%B1%84%ED%8C%85%EB%B0%A9%EB%AA%A9%EB%A1%9D.png" width="200" height="400"></center>
로그인한 계정을 기반으로, 해당 계정이 현재까지 나눈 대화목록과 마지막 메시지, 시간을 확인할 수 있습니다.  
기존에 대화를 마치고, 삭제한 경우 위 화면에 나타나지 않습니다.

### FIND 화면
해당 화면은 현재 기능이 구현되지 않은 페이지 입니다.   
향후, 대화를 나눈 회사들의 정보들이나, 공지사항 등을 모아볼 수 있는 기능으로 확장시킬 계획입니다. 

### SETTING페이지
<center><img src="https://github.com/jun1116/aib_section3_project/blob/main/imagesFolder/setting_1_.png" width="200" height="400"></center>
해당 페이지에서 로그아웃과, 계정 삭제를 진행할 수 있습니다. 
이외의 버튼들은 기능이 구현되지 않은 버튼들입니다.
