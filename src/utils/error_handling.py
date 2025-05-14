"""
error_handling.py
공통 에러/예외 처리 모듈
"""

class SigmaError(Exception):
    """
    SIGMA 시스템 공통 예외 클래스
    """
    pass

def handle_error(e):
    """
    예외 처리 및 로깅 함수
    """
    # TODO: 로깅 및 알림 연동
    print(f"[ERROR] {e}") 