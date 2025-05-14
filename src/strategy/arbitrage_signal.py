"""
arbitrage_signal.py
업비트-바이낸스 가격차 기반 차익거래 신호 전략 함수 모듈
"""

def arbitrage_signal_strategy(event, context, threshold=50):
    """
    업비트-바이낸스 가격차 기반 차익거래 신호 전략
    :param event: {'upbit_price': float, 'binance_price': float, ...}
    :param context: 동일
    :param threshold: 진입 임계값(가격차)
    :return: '매수'(진입), '매도'(청산), '관망'
    """
    upbit = event.get('upbit_price')
    binance = event.get('binance_price')
    if upbit is None or binance is None:
        return '관망'
    # 진입: 바이낸스-업비트 가격차가 threshold 이상이면 진입(매수/공매도)
    if (binance - upbit) >= threshold:
        return '매수'
    # 청산: 가격차가 0 이하로 수렴하면 청산
    elif (binance - upbit) <= 0:
        return '매도'
    else:
        return '관망' 