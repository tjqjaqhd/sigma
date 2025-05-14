import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/strategy')))

from gpt_controller import generate_strategy
from local_engine import process_simple_strategy

def test_generate_strategy():
    event = {'market': 'KRW-BTC', 'trade_price_norm': 1.0}
    context = {'trade_price': 100, 'ma5': 105, 'ma20': 90}
    result = generate_strategy(event, context)
    print('GPT 전략:', result)
    assert result is None or isinstance(result, str)
    print('[gpt_controller] 전략 생성 테스트 통과')

def test_process_simple_strategy():
    event = {'market': 'KRW-BTC', 'trade_price_norm': 1.0}
    context = {'trade_price': 100, 'ma5': 105, 'ma20': 90}
    result = process_simple_strategy(event, context)
    print('로컬 전략:', result)
    assert isinstance(result, str)
    print('[local_engine] 전략 생성 테스트 통과')

if __name__ == '__main__':
    test_generate_strategy()
    test_process_simple_strategy() 