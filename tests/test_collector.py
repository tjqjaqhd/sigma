import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/data')))

from collector import collect_market_data

def test_collect_market_data():
    data = collect_market_data(top_n=5)
    print('수집된 데이터:', data)
    assert isinstance(data, list)
    assert len(data) > 0, '데이터가 수집되지 않음'
    print('[collector] 시장 데이터 수집 테스트 통과')

if __name__ == '__main__':
    test_collect_market_data() 