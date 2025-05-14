"""
executor.py
전략 실행(주문, 포트폴리오 관리) 모듈
"""

from src.utils.error_handling import handle_error
import os
import requests

BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
BINANCE_BASE_URL = os.getenv('BINANCE_BASE_URL', 'https://api.binance.com')  # 실거래 기본값

def execute_order(strategy, mode='simulation'):
    """
    전략에 따른 주문 실행 함수
    :param strategy: dict (예: {'symbol': 'BTCUSDT', 'action': 'sell', 'amount': 0.1, 'type': 'spot'/'margin'/'arbitrage'})
    :param mode: 'simulation', 'live', 'backtest' 중 선택
    :return: 실행 결과 dict (예: {'status': 'simulated', ...} 또는 {'status': 'failed', 'reason': ...})
    """
    result = {
        'status': None,
        'order': None,
        'reason': None
    }
    try:
        if not isinstance(strategy, dict):
            result['status'] = 'failed'
            result['reason'] = 'strategy must be dict'
            return result
        symbol = strategy.get('symbol')
        action = strategy.get('action')
        amount = strategy.get('amount')
        order_type = strategy.get('type', 'spot')
        if not symbol or not action or not amount:
            result['status'] = 'failed'
            result['reason'] = 'missing required fields'
            return result
        if mode == 'simulation':
            # 임의 체결 결과 반환
            result['status'] = 'simulated'
            result['order'] = {
                'symbol': symbol,
                'action': action,
                'amount': amount,
                'type': order_type,
                'price': 10000  # 예시값
            }
        elif mode == 'live':
            # 실제 바이낸스 spot 시장가 주문 (실거래)
            try:
                if order_type != 'spot':
                    result['status'] = 'failed'
                    result['reason'] = 'only spot live order supported'
                    return result
                side = 'BUY' if action == 'buy' else 'SELL'
                endpoint = f"{BINANCE_BASE_URL}/api/v3/order"
                headers = {
                    'X-MBX-APIKEY': BINANCE_API_KEY
                }
                params = {
                    'symbol': symbol,
                    'side': side,
                    'type': 'MARKET',
                    'quantity': amount,
                    'timestamp': int(__import__('time').time() * 1000)
                }
                import hmac, hashlib, urllib.parse
                query_string = urllib.parse.urlencode(params)
                signature = hmac.new(BINANCE_API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()
                params['signature'] = signature
                response = requests.post(endpoint, headers=headers, params=params)
                response.raise_for_status()
                order_resp = response.json()
                result['status'] = 'executed'
                result['order'] = {
                    'symbol': symbol,
                    'action': action,
                    'amount': amount,
                    'type': order_type,
                    'price': order_resp.get('fills', [{}])[0].get('price', 0) if 'fills' in order_resp else 0,
                    'binance_response': order_resp
                }
            except Exception as e:
                handle_error(e)
                result['status'] = 'failed'
                result['reason'] = str(e)
        elif mode == 'backtest':
            # 과거 데이터 기반 체결 시뮬레이션 (여기선 임의 처리)
            result['status'] = 'backtested'
            result['order'] = {
                'symbol': symbol,
                'action': action,
                'amount': amount,
                'type': order_type,
                'price': 10000  # 예시값
            }
        else:
            result['status'] = 'failed'
            result['reason'] = f'Unknown mode: {mode}'
    except Exception as e:
        handle_error(e)
        result['status'] = 'failed'
        result['reason'] = str(e)
    return result

portfolio_state = {}

def update_portfolio(order_result):
    """
    포트폴리오 상태 업데이트 함수
    :param order_result: 실행 결과 dict
    :return: 상태 저장 성공 여부(bool)
    """
    try:
        if not isinstance(order_result, dict):
            print('[portfolio] 입력이 dict가 아님')
            return False
        order = order_result.get('order')
        if not order:
            print('[portfolio] order 정보 없음')
            return False
        symbol = order.get('symbol')
        amount = order.get('amount')
        action = order.get('action')
        if not symbol or not amount or not action:
            print('[portfolio] 필수 정보 누락')
            return False
        # 단순 메모리 상태 저장 (실제 확장 시 DB 등으로 대체)
        if symbol not in portfolio_state:
            portfolio_state[symbol] = 0
        if action == 'buy':
            portfolio_state[symbol] += amount
        elif action == 'sell':
            portfolio_state[symbol] -= amount
        print(f'[portfolio] {symbol} 잔고: {portfolio_state[symbol]}')
        return True
    except Exception as e:
        handle_error(e)
        return False

def execute_arbitrage(upbit_price, binance_price, amount, mode='simulation', logger=None):
    """
    업비트 현물-바이낸스 1배 공매도 차익거래 전략 실행 함수
    :param upbit_price: 업비트 현물 가격
    :param binance_price: 바이낸스 선물 가격
    :param amount: 거래 수량
    :param mode: 'real', 'simulation', 'backtest' 중 선택
    :param logger: 로깅 함수 또는 객체
    :return: 거래 결과(dict)
    """
    result = {
        'upbit_order': None,
        'binance_order': None,
        'arbitrage_profit': 0,
        'status': 'init',
        'error': None
    }
    try:
        # 1. 진입 조건(가격차 등)은 외부에서 판단했다고 가정
        # 2. 실전/시뮬/백테스트 모드 분기
        if mode == 'real':
            # TODO: 실제 업비트/바이낸스 API 연동 주문
            # upbit_result = upbit_api.buy(...)
            # binance_result = binance_api.short(...)
            result['upbit_order'] = {'price': upbit_price, 'amount': amount, 'status': 'mock_real'}
            result['binance_order'] = {'price': binance_price, 'amount': amount, 'status': 'mock_real'}
            result['status'] = 'executed'
        else:
            # 시뮬/백테스트: 가상 주문 처리
            result['upbit_order'] = {'price': upbit_price, 'amount': amount, 'status': 'simulated'}
            result['binance_order'] = {'price': binance_price, 'amount': amount, 'status': 'simulated'}
            # 단순 차익 계산(수수료/슬리피지 등은 추후 반영)
            result['arbitrage_profit'] = (binance_price - upbit_price) * amount
            result['status'] = 'simulated'
        if logger:
            logger.info(f"[arbitrage] upbit: {upbit_price}, binance: {binance_price}, amount: {amount}, mode: {mode}")
    except Exception as e:
        result['status'] = 'error'
        result['error'] = str(e)
        if logger:
            logger.error(f"[arbitrage][error] {e}")
    return result 