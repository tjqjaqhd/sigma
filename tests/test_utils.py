import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/utils')))

from config import get_config
from logger import get_logger
from error_handling import SigmaError, handle_error

# config 테스트
def test_config():
    os.environ['TEST_KEY'] = 'test_value'
    assert get_config('TEST_KEY') == 'test_value'
    assert get_config('NOT_EXIST', 'default') == 'default'
    print('[config] 테스트 통과')

# logger 테스트
def test_logger():
    logger = get_logger('TEST')
    logger.info('info 메시지')
    logger.error('error 메시지')
    print('[logger] 테스트 통과')

# error_handling 테스트
def test_error_handling():
    try:
        raise SigmaError('테스트 에러')
    except SigmaError as e:
        handle_error(e)
        print('[error_handling] 테스트 통과')

if __name__ == '__main__':
    test_config()
    test_logger()
    test_error_handling() 