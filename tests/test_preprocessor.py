import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/data')))

from preprocessor import clean_data, normalize_data
from collector import collect_market_data

def test_clean_data():
    # 결측치/이상치 포함 샘플
    raw = [
        {'market': 'KRW-BTC', 'trade_price': 100, 'acc_trade_price_24h': 1000},
        {'market': 'KRW-ETH', 'trade_price': None, 'acc_trade_price_24h': 2000},
        {'market': 'KRW-XRP', 'trade_price': float('nan'), 'acc_trade_price_24h': 3000},
        {'market': 'KRW-DOGE', 'trade_price': -1, 'acc_trade_price_24h': 4000},
        {'market': 'KRW-KLAY', 'trade_price': 200, 'acc_trade_price_24h': 0},
    ]
    cleaned = clean_data(raw)
    print('cleaned:', cleaned)
    assert all(item['trade_price'] is not None and item['trade_price'] >= 0 for item in cleaned)
    print('[preprocessor] clean_data 테스트 통과')

def test_normalize_data():
    # collector에서 실제 데이터 수집
    data = collect_market_data(top_n=5)
    cleaned = clean_data(data)
    normed = normalize_data(cleaned)
    print('normalized:', normed)
    assert all('trade_price_norm' in item and 'acc_trade_price_24h_norm' in item for item in normed)
    print('[preprocessor] normalize_data 테스트 통과')

if __name__ == '__main__':
    test_clean_data()
    test_normalize_data() 