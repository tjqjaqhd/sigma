"""
collector.py
시장, 뉴스, 소셜, 외부 API 등 다양한 데이터 수집 모듈
"""

import requests

def collect_market_data(top_n=10):
    """
    업비트 API를 활용해 거래량 상위 top_n개 종목(코인)을 수집한다.
    :param top_n: 상위 몇 개 종목을 반환할지 지정 (기본 10개)
    :return: [{'market': 마켓코드, 'korean_name': 한글명, 'trade_price': 현재가, 'acc_trade_price_24h': 24시간 누적 거래대금} ...]
    """
    # 1. 전체 마켓 코드 조회
    market_url = 'https://api.upbit.com/v1/market/all'
    market_res = requests.get(market_url, params={'isDetails': 'false'})
    markets = [m['market'] for m in market_res.json() if m['market'].startswith('KRW-')]

    # 2. 시세/거래량 데이터 조회
    ticker_url = 'https://api.upbit.com/v1/ticker'
    batch_size = 100  # 업비트 API는 최대 100개까지 조회 가능
    all_tickers = []
    for i in range(0, len(markets), batch_size):
        batch = markets[i:i+batch_size]
        res = requests.get(ticker_url, params={'markets': ','.join(batch)})
        all_tickers.extend(res.json())

    # 3. 거래량 기준 정렬 및 상위 N개 추출
    sorted_tickers = sorted(
        all_tickers,
        key=lambda x: x['acc_trade_price_24h'],
        reverse=True
    )
    top_tickers = sorted_tickers[:top_n]

    # 4. 종목명 매핑
    market_info = {m['market']: m['korean_name'] for m in market_res.json()}
    result = []
    for t in top_tickers:
        result.append({
            'market': t['market'],
            'korean_name': market_info.get(t['market'], t['market']),
            'trade_price': t['trade_price'],
            'acc_trade_price_24h': t['acc_trade_price_24h']
        })
    return result


def collect_news_data():
    """
    뉴스 데이터 수집 함수
    """
    pass

def collect_social_data():
    """
    소셜 데이터 수집 함수
    """
    pass 