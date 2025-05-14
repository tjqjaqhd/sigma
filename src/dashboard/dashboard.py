"""
dashboard.py
웹 대시보드(실시간 시각화/모니터링) 모듈
"""

def run_dashboard(feedback_data, performance):
    """
    콘솔 기반 대시보드: 피드백/모니터링 데이터 시각화 예시
    :param feedback_data: 피드백 데이터 리스트
    :param performance: 성과 분석 결과(dict)
    """
    print("\n===== SIGMA 대시보드(콘솔) =====")
    print("[거래별 피드백]")
    for i, f in enumerate(feedback_data):
        print(f"{i+1}. 상태: {f['status']}, 수익: {f['profit']}, 에러: {f['error']}")
    print("\n[전체 성과 요약]")
    for k, v in performance.items():
        print(f"{k}: {v}")
    print("==============================\n")

if __name__ == "__main__":
    # 예시 데이터 (피드백/모니터링 모듈에서 가져온다고 가정)
    feedback_data = [
        {'status': 'simulated', 'profit': 50, 'error': None},
        {'status': 'simulated', 'profit': -25, 'error': None},
        {'status': 'error', 'profit': 0, 'error': 'API fail'},
        {'status': 'simulated', 'profit': 20, 'error': None},
    ]
    performance = {
        'total_profit': 45,
        'total_trades': 4,
        'success': 3,
        'fail': 1,
        'success_rate': 75.0
    }
    run_dashboard(feedback_data, performance) 