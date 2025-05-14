"""
collector.py
시장, 뉴스, 소셜, 외부 API 등 다양한 데이터 수집 모듈
"""

import requests
from src.data.preprocessor import clean_data, normalize_data, create_features
from src.data.db import save_data
from src.utils.error_handling import handle_error
import os
import time

BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
BINANCE_BASE_URL = 'https://api.binance.com'

def collect_market_data(top_n=10):
    """
    업비트 API를 활용해 거래량 상위 top_n개 종목(코인)을 수집한다.
    :param top_n: 상위 몇 개 종목을 반환할지 지정 (기본 10개)
    :return: [{'market': 마켓코드, 'korean_name': 한글명, 'trade_price': 현재가, 'acc_trade_price_24h': 24시간 누적 거래대금} ...]
    """
    try:
        # 1. 전체 마켓 코드 조회
        market_url = 'https://api.upbit.com/v1/market/all'
        market_res = requests.get(market_url, params={'isDetails': 'false'})
        market_res.raise_for_status()
        markets = [m['market'] for m in market_res.json() if m['market'].startswith('KRW-')]

        # 2. 시세/거래량 데이터 조회
        ticker_url = 'https://api.upbit.com/v1/ticker'
        batch_size = 100  # 업비트 API는 최대 100개까지 조회 가능
        all_tickers = []
        for i in range(0, len(markets), batch_size):
            batch = markets[i:i+batch_size]
            res = requests.get(ticker_url, params={'markets': ','.join(batch)})
            res.raise_for_status()
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
    except Exception as e:
        handle_error(e)
        return []


def collect_news_data():
    """
    뉴스 데이터 수집 함수 (스켈레톤)
    """
    pass

def collect_social_data():
    """
    소셜 데이터 수집 함수 (스켈레톤)
    """
    pass

def run_data_pipeline(top_n=10):
    """
    시장 데이터 수집 → 정제 → 정규화 → 피처 생성 → DB 저장까지 한 번에 처리하는 파이프라인 함수
    :param top_n: 상위 N개 종목
    :return: 저장 성공 여부
    """
    try:
        raw = collect_market_data(top_n=top_n)
        cleaned = clean_data(raw)
        normalized = normalize_data(cleaned)
        featured = create_features(normalized)
        result = save_data(featured)
        return result
    except Exception as e:
        handle_error(e)
        return False

def get_top_liquid_symbols(limit=5):
    """
    바이낸스에서 거래량 상위(유동성 높은) 심볼을 조회한다.
    :param limit: 상위 몇 개 심볼을 반환할지 지정
    :return: ['BTCUSDT', 'ETHUSDT', ...]
    """
    try:
        url = f"{BINANCE_BASE_URL}/api/v3/ticker/24hr"
        res = requests.get(url)
        res.raise_for_status()
        tickers = res.json()
        # USDT 마켓만, 거래량 기준 정렬
        usdt_tickers = [t for t in tickers if t['symbol'].endswith('USDT')]
        sorted_tickers = sorted(usdt_tickers, key=lambda x: float(x['quoteVolume']), reverse=True)
        return [t['symbol'] for t in sorted_tickers[:limit]]
    except Exception as e:
        handle_error(e)
        return ['BTCUSDT', 'ETHUSDT']


def collect_binance_spot_data(symbols=None):
    """
    바이낸스 spot 데이터 수집 함수 (실제 API 연동)
    :param symbols: 조회할 심볼 리스트(예: ['BTCUSDT', 'ETHUSDT'])
    :return: [{'symbol': 심볼, 'price': 현재가, 'volume': 거래량, 'bid': 매수호가, 'ask': 매도호가, ...}]
    """
    try:
        if symbols is None:
            symbols = get_top_liquid_symbols()
        result = []
        for symbol in symbols:
            # 현재가, 거래량
            url = f"{BINANCE_BASE_URL}/api/v3/ticker/24hr?symbol={symbol}"
            res = requests.get(url)
            res.raise_for_status()
            data = res.json()
            # 호가(오더북)
            orderbook_url = f"{BINANCE_BASE_URL}/api/v3/depth?symbol={symbol}&limit=5"
            ob_res = requests.get(orderbook_url)
            ob_res.raise_for_status()
            ob = ob_res.json()
            bid = float(ob['bids'][0][0]) if ob['bids'] else None
            ask = float(ob['asks'][0][0]) if ob['asks'] else None
            result.append({
                'symbol': symbol,
                'price': float(data['lastPrice']),
                'volume': float(data['volume']),
                'bid': bid,
                'ask': ask,
                'timestamp': int(time.time())
            })
        return result
    except Exception as e:
        handle_error(e)
        return []


def collect_binance_margin_data(symbols=None):
    """
    바이낸스 margin 데이터 수집 함수 (실제 API 연동)
    :param symbols: 조회할 심볼 리스트
    :return: [{...}]
    """
    try:
        if symbols is None:
            symbols = get_top_liquid_symbols()
        result = []
        for symbol in symbols:
            # margin price: 바이낸스 margin은 별도 엔드포인트가 있으나, 현물과 유사하게 ticker/24hr로 접근 가능
            url = f"{BINANCE_BASE_URL}/api/v3/ticker/24hr?symbol={symbol}"
            res = requests.get(url)
            res.raise_for_status()
            data = res.json()
            # 호가(오더북)
            orderbook_url = f"{BINANCE_BASE_URL}/api/v3/depth?symbol={symbol}&limit=5"
            ob_res = requests.get(orderbook_url)
            ob_res.raise_for_status()
            ob = ob_res.json()
            bid = float(ob['bids'][0][0]) if ob['bids'] else None
            ask = float(ob['asks'][0][0]) if ob['asks'] else None
            result.append({
                'symbol': symbol,
                'price': float(data['lastPrice']),
                'volume': float(data['volume']),
                'bid': bid,
                'ask': ask,
                'timestamp': int(time.time()),
                'type': 'margin'
            })
        return result
    except Exception as e:
        handle_error(e)
        return []


def collect_binance_arbitrage_data():
    """
    spot/margin 간 가격차(차익거래) 데이터 수집
    :return: [{'symbol': 심볼, 'spot_price': spot가격, 'margin_price': margin가격, 'spread': 가격차, ...}]
    """
    try:
        symbols = get_top_liquid_symbols()
        spot_data = collect_binance_spot_data(symbols)
        margin_data = collect_binance_margin_data(symbols)
        result = []
        for s, m in zip(spot_data, margin_data):
            spread = m['price'] - s['price']
            result.append({
                'symbol': s['symbol'],
                'spot_price': s['price'],
                'margin_price': m['price'],
                'spread': spread,
                'spot_bid': s['bid'],
                'spot_ask': s['ask'],
                'margin_bid': m['bid'],
                'margin_ask': m['ask'],
                'timestamp': s['timestamp']
            })
        return result
    except Exception as e:
        handle_error(e)
        return []

# 확장: 새로운 거래소/데이터 소스 함수는 아래와 같이 추가만 하면 됨
# def collect_kraken_spot_data(...): ... 