"""
config.py
시스템 설정/환경변수 관리 모듈
"""

import os

def get_config(key, default=None):
    """
    환경변수 또는 설정값 조회 함수
    """
    return os.environ.get(key, default) 