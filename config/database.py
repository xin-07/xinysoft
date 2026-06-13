"""
数据库配置模块
"""
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, Dict, Any
from contextlib import contextmanager

# 加载环境变量
load_dotenv()

# 数据库配置
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', ''),
    'dbname': os.getenv('DB_NAME', 'xinysoftdb'),
    'cursor_factory': RealDictCursor
}


def get_connection() -> psycopg2.extensions.connection:
    """
    获取数据库连接

    Returns:
        psycopg2.extensions.connection: 数据库连接对象
    """
    return psycopg2.connect(**DB_CONFIG)


@contextmanager
def get_db():
    """
    数据库连接上下文管理器

    Yields:
        psycopg2.extensions.connection: 数据库连接对象
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