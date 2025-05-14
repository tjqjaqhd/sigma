"""
gpt_controller.py
GPT 기반 전략 컨트롤러 모듈
"""

import os
import openai
from utils.config import get_config

def generate_strategy(event, context):
    """
    GPT를 활용한 전략 생성 함수
    :param event: 감지된 이벤트(딕셔너리/리스트)
    :param context: 시장 컨텍스트(딕셔너리)
    :return: 생성된 전략(텍스트)
    """
    try:
        openai.api_key = get_config('OPENAI_API_KEY')
        prompt = f"""
        다음은 자동화 트레이딩 전략 생성 요청입니다.
        [이벤트]: {event}
        [시장상황]: {context}
        위 정보를 바탕으로 매매 전략을 한글로 간결하게 제안해 주세요.
        - 진입/청산 조건
        - 리스크 관리
        - 간단한 설명
        """
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "당신은 트레이딩 전략가입니다."},
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f'[gpt_controller] 전략 생성 실패: {e}')
        return None 