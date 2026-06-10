"""
数据库配置模块
"""
import os
from dotenv import load_dotenv
import pymysql
from pymysql.cursors import DictCursor
from typing import Optional, Dict, Any
from contextlib import contextmanager

# 加载环境变量
load_dotenv()

# 数据库配置
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'xinysoft'),
    'charset': 'utf8mb4',
    'cursorclass': DictCursor
}


def get_connection() -> pymysql.Connection:
    """
    获取数据库连接

    Returns:
        pymysql.Connection: 数据库连接对象
    """
    return pymysql.connect(**DB_CONFIG)


@contextmanager
def get_db():
    """
    数据库连接上下文管理器

    Yields:
        pymysql.Connection: 数据库连接对象
    """
    conn = None
    try:
        conn = get_connection()
        yield conn
    finally:
        if conn:
            conn.close()


def execute_query(sql: str, params: Optional[tuple] = None) -> Optional[Dict[str, Any]]:
    """
    执行查询语句，返回单条结果

    Args:
        sql: SQL 查询语句
        params: 查询参数

    Returns:
        查询结果字典，如果没有结果返回 None
    """
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()


def execute_query_all(sql: str, params: Optional[tuple] = None) -> list:
    """
    执行查询语句，返回所有结果列表

    Args:
        sql: SQL 查询语句
        params: 查询参数

    Returns:
        查询结果列表，如果没有结果返回空列表
    """
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()