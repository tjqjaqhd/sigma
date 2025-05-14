"""
db.py
DB/메모리 캐시 연동 및 데이터 저장/조회 모듈
"""

import sqlite3
import os
from src.utils.config import get_config
from src.utils.error_handling import handle_error

def get_db_path():
    return get_config('DB_PATH', './db.sqlite')

def save_data(data):
    """
    데이터 저장 함수 (SQLite)
    :param data: 저장할 데이터(리스트[dict])
    :return: 저장 성공(True)/실패(False)
    """
    if not data:
        return False
    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        # 테이블 생성(없으면)
        c.execute('''CREATE TABLE IF NOT EXISTS market_data (
            market TEXT, korean_name TEXT, trade_price REAL, acc_trade_price_24h REAL,
            trade_price_norm REAL, acc_trade_price_24h_norm REAL, ts DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        # 데이터 저장
        for item in data:
            c.execute('''INSERT INTO market_data (market, korean_name, trade_price, acc_trade_price_24h, trade_price_norm, acc_trade_price_24h_norm)
                         VALUES (?, ?, ?, ?, ?, ?)''',
                      (
                        item.get('market'),
                        item.get('korean_name'),
                        item.get('trade_price'),
                        item.get('acc_trade_price_24h'),
                        item.get('trade_price_norm'),
                        item.get('acc_trade_price_24h_norm')
                      ))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        handle_error(e)
        return False

def load_data(query=None):
    """
    데이터 조회 함수 (SQLite)
    :param query: 조회 조건(딕셔너리, 예: {'market': 'KRW-BTC'})
    :return: 조회된 데이터(리스트[dict])
    """
    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        sql = 'SELECT market, korean_name, trade_price, acc_trade_price_24h, trade_price_norm, acc_trade_price_24h_norm, ts FROM market_data'
        params = []
        if query and 'market' in query:
            sql += ' WHERE market = ?'
            params.append(query['market'])
        c.execute(sql, params)
        rows = c.fetchall()
        conn.close()
        result = []
        for row in rows:
            result.append({
                'market': row[0],
                'korean_name': row[1],
                'trade_price': row[2],
                'acc_trade_price_24h': row[3],
                'trade_price_norm': row[4],
                'acc_trade_price_24h_norm': row[5],
                'ts': row[6]
            })
        return result
    except Exception as e:
        handle_error(e)
        return [] 