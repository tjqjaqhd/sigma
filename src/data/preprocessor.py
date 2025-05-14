"""
preprocessor.py
수집된 데이터의 전처리 및 정제 모듈
"""

import math

def clean_data(raw_data):
    """
    데이터 정제 함수
    - 결측치(None, NaN) 및 음수/비정상 값 제거
    :param raw_data: 수집된 원시 데이터(리스트/딕셔너리)
    :return: 정제된 데이터(리스트)
    """
    if not isinstance(raw_data, list):
        raise ValueError('입력 데이터는 리스트여야 합니다.')
    cleaned = []
    for item in raw_data:
        if not isinstance(item, dict):
            continue
        # 결측치/NaN/음수 필터링 (예: trade_price, acc_trade_price_24h)
        if any(
            v is None or (isinstance(v, float) and math.isnan(v)) or (isinstance(v, (int, float)) and v < 0)
            for k, v in item.items() if k in ['trade_price', 'acc_trade_price_24h']
        ):
            continue
        cleaned.append(item)
    return cleaned

def normalize_data(cleaned_data):
    """
    데이터 정규화 함수 (0~1 스케일)
    :param cleaned_data: 정제된 데이터(리스트)
    :return: 정규화된 데이터(리스트)
    """
    if not cleaned_data:
        return []
    # trade_price, acc_trade_price_24h만 0~1 정규화
    prices = [item['trade_price'] for item in cleaned_data]
    vols = [item['acc_trade_price_24h'] for item in cleaned_data]
    min_p, max_p = min(prices), max(prices)
    min_v, max_v = min(vols), max(vols)
    def norm(val, minv, maxv):
        if maxv == minv:
            return 0.0
        return (val - minv) / (maxv - minv)
    result = []
    for item in cleaned_data:
        norm_item = item.copy()
        norm_item['trade_price_norm'] = norm(item['trade_price'], min_p, max_p)
        norm_item['acc_trade_price_24h_norm'] = norm(item['acc_trade_price_24h'], min_v, max_v)
        result.append(norm_item)
    return result 