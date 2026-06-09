"""Cloudflare Workers 入口文件"""
import sys
import os

# 添加项目根目录到 Python 路径，使 main.py 可被导入
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from main import app
