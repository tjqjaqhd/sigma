"""
simulator.py
실시간/가상 시뮬레이션 모듈
"""

from src.strategy.arbitrage_signal import arbitrage_signal_strategy
from src.execution.executor import execute_order
from src.strategy.feedback import collect_feedback
from src.strategy.monitoring import analyze_performance
from src.utils.error_handling import handle_error

def run_simulation(strategy_func, data_stream, mode='simulation', initial_balance=1000000, fee=0.001):
    """
    전략 시뮬레이션 실행 함수 (통합 루프)
    :param strategy_func: 전략 함수
    :param data_stream: 실시간/가상 데이터 제너레이터
    :param mode: 'simulation', 'live', 'backtest' 중 선택
    :param initial_balance: 시작 자산
    :param fee: 거래 수수료 비율
    :return: 전체 실행 결과/이력 리스트, 성과 분석 결과, 최종 잔고, 거래내역, 수익률
    """
    results = []
    feedback_data = []
    trades = []
    balance = initial_balance
    try:
        for i, data in enumerate(data_stream):
            try:
                # 1. 전략 신호 생성
                event = data
                context = data
                strategy = strategy_func(event, context)
                # 2. 주문 실행
                order_dict = {
                    'symbol': data.get('symbol', 'UNKNOWN'),
                    'action': 'buy' if strategy and '매수' in strategy else ('sell' if strategy and '매도' in strategy else 'hold'),
                    'amount': data.get('amount', 0.5),
                    'type': 'spot'
                }
                if order_dict['action'] == 'hold':
                    continue
                order_result = execute_order(order_dict, mode=mode)
                # 3. 피드백 기록
                feedback = collect_feedback(order_result)
                feedback_data.append(feedback)
                # 4. 거래내역 및 잔고 반영
                price = data.get('trade_price', 0)
                if order_dict['action'] == 'buy':
                    cost = price * order_dict['amount'] * (1 + fee)
                    balance -= cost
                    trades.append({'i': i, 'action': 'buy', 'price': price, 'amount': order_dict['amount'], 'cost': cost})
                elif order_dict['action'] == 'sell':
                    revenue = price * order_dict['amount'] * (1 - fee)
                    balance += revenue
                    trades.append({'i': i, 'action': 'sell', 'price': price, 'amount': order_dict['amount'], 'revenue': revenue})
                results.append({
                    'i': i,
                    'data': data,
                    'strategy': strategy,
                    'order': order_result,
                    'feedback': feedback
                })
            except Exception as e:
                handle_error(e)
                results.append({'i': i, 'data': data, 'error': str(e)})
        # 5. 성과 분석
        performance = analyze_performance(feedback_data)
        total_invested = initial_balance
        final_balance = balance
        ret = ((final_balance - total_invested) / total_invested * 100) if total_invested > 0 else 0
        return {
            'results': results,
            'performance': performance,
            'final_balance': final_balance,
            'trades': trades,
            'return': ret
        }
    except Exception as e:
        handle_error(e)
        return {'results': results, 'performance': {}, 'final_balance': balance, 'trades': trades, 'return': 0}

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
    print(f"성과분석: {sim_result['performance']}") 