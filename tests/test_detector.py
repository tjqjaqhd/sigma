import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/data')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/event')))

from collector import collect_market_data
from preprocessor import clean_data, normalize_data
from detector import detect_event

def test_detect_event():
    data = collect_market_data(top_n=10)
    cleaned = clean_data(data)
    normed = normalize_data(cleaned)
    events = detect_event(normed, price_threshold=0.9, volume_threshold=0.9)
    print('감지된 이벤트:', events)
    assert isinstance(events, list)
    print('[detector] 이벤트 감지 테스트 통과')

if __name__ == '__main__':
    test_detect_event() 