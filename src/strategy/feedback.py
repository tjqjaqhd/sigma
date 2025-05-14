"""
feedback.py
실행 결과 피드백 및 모니터링 모듈
"""

from src.utils.error_handling import handle_error

def collect_feedback(order_result):
    """
    주문 결과 피드백 수집 함수
    :param order_result: 주문/전략 실행 결과(dict)
    :return: 피드백 데이터(dict)
    """
    try:
        feedback = {
            'status': order_result.get('status', 'unknown'),
            'profit': order_result.get('arbitrage_profit', 0),
            'error': order_result.get('error', None),
            'upbit_order': order_result.get('upbit_order'),
            'binance_order': order_result.get('binance_order')
        }
        return feedback
    except Exception as e:
        handle_error(e)
        return {'status': 'error', 'profit': 0, 'error': str(e)}

def analyze_performance(feedback_data):
    """
    전략 성과 분석 함수
    :param feedback_data: 피드백 데이터 리스트
    :return: 전체 성과(총 수익, 성공률 등)
    """
    try:
        total_profit = sum(f.get('profit', 0) for f in feedback_data)
        total = len(feedback_data)
        success = sum(1 for f in feedback_data if f.get('status') == 'simulated' or f.get('status') == 'executed')
        fail = sum(1 for f in feedback_data if f.get('status') == 'error')
        success_rate = (success / total * 100) if total > 0 else 0
        return {
            'total_profit': total_profit,
            'total_trades': total,
            'success': success,
            'fail': fail,
            'success_rate': success_rate
        }
    except Exception as e:
        handle_error(e)
        return {'total_profit': 0, 'total_trades': 0, 'success': 0, 'fail': 0, 'success_rate': 0, 'error': str(e)}

def save_feedback_to_file(feedback_data, filename='feedback_log.jsonl'):
    """
    피드백 데이터 리스트를 파일(jsonl)로 저장
    :param feedback_data: 리스트[dict]
    :param filename: 저장 파일명
    :return: 저장 성공 여부(bool)
    """
    import json
    try:
        with open(filename, 'a', encoding='utf-8') as f:
            for item in feedback_data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        return True
    except Exception as e:
        handle_error(e)
        return False

if __name__ == "__main__":
    # 예시 주문/전략 실행 결과 리스트
    order_results = [
        {'status': 'simulated', 'arbitrage_profit': 50, 'error': None, 'upbit_order': {}, 'binance_order': {}},
        {'status': 'simulated', 'arbitrage_profit': -25, 'error': None, 'upbit_order': {}, 'binance_order': {}},
        {'status': 'error', 'arbitrage_profit': 0, 'error': 'API fail', 'upbit_order': None, 'binance_order': None},
        {'status': 'simulated', 'arbitrage_profit': 20, 'error': None, 'upbit_order': {}, 'binance_order': {}},
    ]
    feedback_data = [collect_feedback(r) for r in order_results]
    print("[피드백 데이터]")
    for f in feedback_data:
        print(f)
    perf = analyze_performance(feedback_data)
    print("[성과 분석 결과]")
    print(perf)
    # 파일 저장 테스트
    ok = save_feedback_to_file(feedback_data, 'feedback_log_test.jsonl')
    print(f"[파일 저장 결과] {ok}") 