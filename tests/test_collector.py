import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.data.collector import collect_market_data
from src.data.collector import collect_binance_spot_data, collect_binance_margin_data, collect_binance_arbitrage_data

def test_collect_market_data():
    data = collect_market_data(top_n=5)
    print('수집된 데이터:', data)
    assert isinstance(data, list)
    assert len(data) > 0, '데이터가 수집되지 않음'
    print('[collector] 시장 데이터 수집 테스트 통과')

def test_collect_binance_spot_data():
    data = collect_binance_spot_data()
    print('바이낸스 spot 데이터:', data)
    assert isinstance(data, list)
    assert len(data) > 0, 'spot 데이터 없음'
    for d in data:
        assert 'symbol' in d and 'price' in d and 'volume' in d
    print('[collector] 바이낸스 spot 데이터 수집 테스트 통과')

def test_collect_binance_margin_data():
    data = collect_binance_margin_data()
    print('바이낸스 margin 데이터:', data)
    assert isinstance(data, list)
    assert len(data) > 0, 'margin 데이터 없음'
    for d in data:
        assert 'symbol' in d and 'price' in d and 'volume' in d and d.get('type') == 'margin'
    print('[collector] 바이낸스 margin 데이터 수집 테스트 통과')

def test_collect_binance_arbitrage_data():
    data = collect_binance_arbitrage_data()
    print('바이낸스 arbitrage 데이터:', data)
    assert isinstance(data, list)
    assert len(data) > 0, 'arbitrage 데이터 없음'
    for d in data:
        assert 'symbol' in d and 'spot_price' in d and 'margin_price' in d and 'spread' in d
    print('[collector] 바이낸스 arbitrage 데이터 수집 테스트 통과')

if __name__ == '__main__':
    test_collect_market_data()
    test_collect_binance_spot_data()
    test_collect_binance_margin_data()
    test_collect_binance_arbitrage_data() 