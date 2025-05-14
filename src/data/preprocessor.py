"""
preprocessor.py
수집된 데이터의 전처리 및 정제 모듈
"""

import math
from src.utils.error_handling import handle_error

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

def create_features(data, window=3):
    """
    전략용 피처(이동평균, 변동성 등) 생성 함수
    :param data: 정제/정규화된 데이터(리스트)
    :param window: 이동평균/변동성 계산 구간(기본 3)
    :return: 피처가 추가된 데이터(리스트)
    """
    try:
        if not data or len(data) < window:
            return data
        prices = [item['trade_price'] for item in data]
        result = []
        for i in range(len(data)):
            feat_item = data[i].copy()
            if i >= window - 1:
                window_prices = prices[i-window+1:i+1]
                # 이동평균
                feat_item['ma'] = sum(window_prices) / window
                # 변동성(표준편차)
                mean = feat_item['ma']
                feat_item['volatility'] = (sum((p-mean)**2 for p in window_prices) / window) ** 0.5
            else:
                feat_item['ma'] = None
                feat_item['volatility'] = None
            result.append(feat_item)
        return result
    except Exception as e:
        handle_error(e)
        return data 