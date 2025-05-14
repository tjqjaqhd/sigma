"""
simulator.py
실시간/가상 시뮬레이션 모듈
"""

def run_simulation(strategy_func, data_stream, initial_balance=1000000, fee=0.001):
    """
    전략 시뮬레이션 실행 함수
    :param strategy_func: 전략 함수
    :param data_stream: 실시간/가상 데이터 제너레이터
    :param initial_balance: 시작 자산
    :param fee: 거래 수수료 비율
    :return: 실시간 포지션/잔고 변화, 거래 로그 등
    """
    balance = initial_balance
    position = 0
    trade_log = []
    for i, data in enumerate(data_stream):
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
        balance = position * data['trade_price'] * (1 - fee)
        trade_log.append({'type': 'final_sell', 'price': data['trade_price'], 'qty': position, 'i': i})
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
    # 진입: 바이낸스-업비트 가격차가 threshold 이상이면 진입(매수/공매도)
    if (binance - upbit) >= threshold:
        return '매수'
    # 청산: 가격차가 0 이하로 수렴하면 청산
    elif (binance - upbit) <= 0:
        return '매도'
    else:
        return '관망'

if __name__ == "__main__":
    from src.execution.executor import execute_arbitrage
    # 예시 데이터: 업비트/바이낸스 가격 스트림
    data_stream = [
        {'upbit_price': 10000, 'binance_price': 10100, 'trade_price': 10000, 'amount': 0.5},
        {'upbit_price': 10200, 'binance_price': 10150, 'trade_price': 10200, 'amount': 0.5},
        {'upbit_price': 9900, 'binance_price': 9950, 'trade_price': 9900, 'amount': 0.5},
        {'upbit_price': 10050, 'binance_price': 10040, 'trade_price': 10050, 'amount': 0.5},
    ]
    print("[단순 차익 누적 예시]")
    results = []
    for data in data_stream:
        result = execute_arbitrage(
            upbit_price=data['upbit_price'],
            binance_price=data['binance_price'],
            amount=data['amount'],
            mode='simulation'
        )
        print(f"[SIM] upbit: {data['upbit_price']}, binance: {data['binance_price']}, amount: {data['amount']} => result: {result}")
        results.append(result)
    total_profit = sum(r['arbitrage_profit'] for r in results)
    print(f"총 차익(누적): {total_profit}\n")

    print("[실제 투자 흐름(잔고/포지션/거래내역) 시뮬레이션]")
    # run_simulation에 차익거래 신호 전략 연동
    sim_result = run_simulation(
        lambda event, context: arbitrage_signal_strategy(event, context, threshold=50),
        data_stream,
        initial_balance=1000000,
        fee=0.001
    )
    print(f"최종 잔고: {sim_result['final_balance']}")
    print(f"거래내역: {sim_result['trades']}")
    print(f"수익률(%): {sim_result['return']}") 