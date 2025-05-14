"""
local_engine.py
로컬 전략 엔진 모듈 (단순/반복 전략 처리)
"""

def process_simple_strategy(event, context):
    """
    단순/반복 전략 처리 함수 (예: 이동평균)
    :param event: 감지된 이벤트(딕셔너리/리스트)
    :param context: 시장 컨텍스트(딕셔너리)
    :return: 생성된 전략(텍스트)
    """
    try:
        # 예시: 단순 이동평균 전략
        price = context.get('trade_price')
        ma5 = context.get('ma5')
        ma20 = context.get('ma20')
        if price and ma5 and ma20:
            if ma5 > ma20 and price > ma5:
                return '매수: 단기 상승 추세. 진입 신호.'
            elif ma5 < ma20 and price < ma5:
                return '매도: 단기 하락 추세. 청산 신호.'
            else:
                return '관망: 명확한 신호 없음.'
        return '관망: 데이터 부족.'
    except Exception as e:
        print(f'[local_engine] 전략 처리 실패: {e}')
        return None 