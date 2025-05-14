"""
test_e2e.py
SIGMA 전체 파이프라인 End-to-End 통합 테스트
"""
from src.strategy.simulator import run_simulation
from src.strategy.arbitrage_signal import arbitrage_signal_strategy
from src.execution.executor import execute_arbitrage
from src.strategy.feedback import collect_feedback, analyze_performance
from src.dashboard.dashboard import run_dashboard
from src.utils.error_handling import handle_error

def main():
    # 1. 샘플 데이터(업비트/바이낸스 가격 스트림)
    data_stream = [
        {'upbit_price': 10000, 'binance_price': 10100, 'trade_price': 10000, 'amount': 0.5},
        {'upbit_price': 10200, 'binance_price': 10150, 'trade_price': 10200, 'amount': 0.5},
        {'upbit_price': 9900, 'binance_price': 9950, 'trade_price': 9900, 'amount': 0.5},
        {'upbit_price': 10050, 'binance_price': 10040, 'trade_price': 10050, 'amount': 0.5},
    ]
    # 2. 전략 신호 생성 및 시뮬레이션
    sim_result = run_simulation(
        lambda event, context: arbitrage_signal_strategy(event, context, threshold=50),
        data_stream,
        initial_balance=1000000,
        fee=0.001
    )
    print("[1] 시뮬레이터 결과:")
    print(sim_result)
    # 3. 주문 실행 결과(여기서는 시뮬레이션 결과를 그대로 사용)
    order_results = []
    for data in data_stream:
        order_results.append(execute_arbitrage(
            upbit_price=data['upbit_price'],
            binance_price=data['binance_price'],
            amount=data['amount'],
            mode='simulation'
        ))
    # 4. 피드백 수집
    feedback_data = [collect_feedback(r) for r in order_results]
    print("[2] 피드백 데이터:")
    for f in feedback_data:
        print(f)
    # 5. 성과 분석
    performance = analyze_performance(feedback_data)
    print("[3] 성과 분석 결과:")
    print(performance)
    # 6. 대시보드 출력
    run_dashboard(feedback_data, performance)

def test_basic_strategy_e2e():
    """
    전체 전략 파이프라인 E2E 테스트 (pytest용)
    """
    try:
        data_stream = [
            {'upbit_price': 10000, 'binance_price': 10100, 'trade_price': 10000, 'amount': 0.5},
            {'upbit_price': 10200, 'binance_price': 10150, 'trade_price': 10200, 'amount': 0.5},
            {'upbit_price': 9900, 'binance_price': 9950, 'trade_price': 9900, 'amount': 0.5},
            {'upbit_price': 10050, 'binance_price': 10040, 'trade_price': 10050, 'amount': 0.5},
        ]
        sim_result = run_simulation(
            lambda event, context: arbitrage_signal_strategy(event, context, threshold=50),
            data_stream,
            initial_balance=1000000,
            fee=0.001
        )
        assert 'results' in sim_result or 'final_balance' in sim_result
        order_results = []
        for data in data_stream:
            order_results.append(execute_arbitrage(
                upbit_price=data['upbit_price'],
                binance_price=data['binance_price'],
                amount=data['amount'],
                mode='simulation'
            ))
        feedback_data = [collect_feedback(r) for r in order_results]
        assert all('status' in f for f in feedback_data)
        performance = analyze_performance(feedback_data)
        assert 'total_profit' in performance
        run_dashboard(feedback_data, performance)
    except Exception as e:
        handle_error(e)
        assert False, f"E2E 테스트 실패: {e}"

if __name__ == "__main__":
    main() 