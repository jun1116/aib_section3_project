#회사의 답변에 대한 기능을 하는 func
from func.func_gangnamBike import gangnamBike

#회사들의 답변을 처음 여기서 나눠서 진행합니다.

def company_answer(company_id, text=None):
    if company_id==1:
        return gangnamBike(text)
    elif company_id==2:
        return f"죄송합니다. 현재 '{text}' 에 대한 회사의 답변리스트 작성중입니다."
