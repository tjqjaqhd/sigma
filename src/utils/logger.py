"""
logger.py
공통 로깅 모듈
"""

import logging

def get_logger(name='SIGMA'):
    """
    로거 인스턴스 반환 함수
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    # TODO: 필요시 외부 모니터링/알림(Grafana, Slack 등) 연동 확장 가능
    return logger 