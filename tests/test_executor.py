import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.execution.executor import execute_order, update_portfolio

def test_execute_order_simulation():
    strategy = {'symbol': 'BTCUSDT', 'action': 'buy', 'amount': 0.001, 'type': 'spot'}
    result = execute_order(strategy, mode='simulation')
    print('시뮬레이션 결과:', result)
    assert result['status'] == 'simulated'
    assert result['order']['symbol'] == 'BTCUSDT'
    assert result['order']['action'] == 'buy'
    assert result['order']['amount'] == 0.001
    print('[executor] 시뮬레이션 주문 테스트 통과')

def test_execute_order_backtest():
    strategy = {'symbol': 'BTCUSDT', 'action': 'sell', 'amount': 0.002, 'type': 'spot'}
    result = execute_order(strategy, mode='backtest')
    print('백테스트 결과:', result)
    assert result['status'] == 'backtested'
    assert result['order']['symbol'] == 'BTCUSDT'
    assert result['order']['action'] == 'sell'
    assert result['order']['amount'] == 0.002
    print('[executor] 백테스트 주문 테스트 통과')

# 실거래(live) 테스트는 실제 주문이 발생하므로, 기본적으로 주석 처리/경고 메시지와 함께 제공합니다.
# def test_execute_order_live():
#     strategy = {'symbol': 'BTCUSDT', 'action': 'buy', 'amount': 0.001, 'type': 'spot'}
#     result = execute_order(strategy, mode='live')
#     print('실거래 결과:', result)
#     assert result['status'] == 'executed'
#     print('[executor] 실거래 주문 테스트 통과')

def test_update_portfolio():
    order_result = {
        'order': {'symbol': 'BTCUSDT', 'action': 'buy', 'amount': 0.001}
    }
    assert update_portfolio(order_result) is True
    order_result = {
        'order': {'symbol': 'BTCUSDT', 'action': 'sell', 'amount': 0.001}
    }
    assert update_portfolio(order_result) is True
    print('[executor] 포트폴리오 업데이트 테스트 통과')

if __name__ == '__main__':
    test_execute_order_simulation()
    test_execute_order_backtest()
    # test_execute_order_live()  # 실거래는 주석 해제 시 실제 주문 발생
    test_update_portfolio() 