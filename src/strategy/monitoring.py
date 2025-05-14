"""
monitoring.py
전략 성과 모니터링 및 분석 모듈
"""

def analyze_performance(feedback_data):
    """
    전략 성과 분석 함수 (모니터링)
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
        return {'total_profit': 0, 'total_trades': 0, 'success': 0, 'fail': 0, 'success_rate': 0, 'error': str(e)} 