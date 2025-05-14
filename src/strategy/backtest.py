"""
backtest.py
전략 백테스트 모듈
"""

def run_backtest(strategy_func, historical_data, initial_balance=1000000, fee=0.001):
    """
    전략 백테스트 실행 함수
    :param strategy_func: 전략 함수(이벤트, 컨텍스트 → 신호)
    :param historical_data: 과거 데이터(리스트)
    :param initial_balance: 시작 자산
    :param fee: 거래 수수료 비율
    :return: 거래 내역, 최종 잔고, 수익률 등
    """
    balance = initial_balance
    position = 0
    trade_log = []
    for i, data in enumerate(historical_data):
        event = data
        context = data
        signal = strategy_func(event, context)
        if signal and '매수' in signal and balance > 0:
            qty = balance / data['trade_price']
            balance = 0
            position = qty
            trade_log.append({'type': 'buy', 'price': data['trade_price'], 'qty': qty, 'i': i})
        elif signal and '매도' in signal and position > 0:
            balance = position * data['trade_price'] * (1 - fee)
            trade_log.append({'type': 'sell', 'price': data['trade_price'], 'qty': position, 'i': i})
            position = 0
    if position > 0:
        balance = position * historical_data[-1]['trade_price'] * (1 - fee)
        trade_log.append({'type': 'final_sell', 'price': historical_data[-1]['trade_price'], 'qty': position, 'i': len(historical_data)-1})
    result = {
        'final_balance': balance,
        'trades': trade_log,
        'return': (balance - initial_balance) / initial_balance * 100
    }
    return result 

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
    if (binance - upbit) >= threshold:
        return '매수'
    elif (binance - upbit) <= 0:
        return '매도'
    else:
        return '관망'

if __name__ == "__main__":
    # 예시 데이터: 업비트/바이낸스 과거 가격 스트림
    historical_data = [
        {'upbit_price': 10000, 'binance_price': 10100, 'trade_price': 10000, 'amount': 0.5},
        {'upbit_price': 10200, 'binance_price': 10150, 'trade_price': 10200, 'amount': 0.5},
        {'upbit_price': 9900, 'binance_price': 9950, 'trade_price': 9900, 'amount': 0.5},
        {'upbit_price': 10050, 'binance_price': 10040, 'trade_price': 10050, 'amount': 0.5},
    ]
    print("[차익거래 신호 기반 전략 백테스트]")
    backtest_result = run_backtest(
        lambda event, context: arbitrage_signal_strategy(event, context, threshold=50),
        historical_data,
        initial_balance=1000000,
        fee=0.001
    )
    print(f"최종 잔고: {backtest_result['final_balance']}")
    print(f"거래내역: {backtest_result['trades']}")
    print(f"수익률(%): {backtest_result['return']}") 