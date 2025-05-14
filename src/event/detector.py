"""
detector.py
트리거/이벤트 감지 모듈
"""

def detect_event(processed_data, price_threshold=0.9, volume_threshold=0.9):
    """
    이벤트 감지 함수
    - 가격/거래량이 상위 10% 이상인 종목을 이벤트로 감지
    :param processed_data: 전처리/정규화된 데이터(리스트)
    :param price_threshold: 가격 정규화 임계값(기본 0.9)
    :param volume_threshold: 거래량 정규화 임계값(기본 0.9)
    :return: 감지된 이벤트(리스트[dict]) 또는 빈 리스트
    """
    if not processed_data:
        return []
    try:
        events = []
        for item in processed_data:
            if (
                item.get('trade_price_norm', 0) >= price_threshold or
                item.get('acc_trade_price_24h_norm', 0) >= volume_threshold
            ):
                events.append(item)
        return events
    except Exception as e:
        print(f'[detector] 이벤트 감지 실패: {e}')
        return [] 