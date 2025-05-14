import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/data')))

from collector import collect_market_data
from preprocessor import clean_data, normalize_data
from db import save_data, load_data

def test_save_and_load():
    # 1. 데이터 수집 및 전처리
    data = collect_market_data(top_n=3)
    cleaned = clean_data(data)
    normed = normalize_data(cleaned)
    # 2. 저장
    ok = save_data(normed)
    assert ok, '데이터 저장 실패'
    print('[db] 데이터 저장 성공')
    # 3. 전체 조회
    all_data = load_data()
    print('전체 조회:', all_data)
    assert len(all_data) > 0
    # 4. 특정 마켓 조회
    if normed:
        market = normed[0]['market']
        one = load_data({'market': market})
        print(f'{market} 조회:', one)
        assert all(item['market'] == market for item in one)
    print('[db] 데이터 조회 테스트 통과')

if __name__ == '__main__':
    test_save_and_load() 