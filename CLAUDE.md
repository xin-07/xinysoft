# CLAUDE.md

## 项目概述

基于 FastAPI 的个人作品集网站后端项目，用于展示个人资料、技术栈、项目经历等信息。

## 技术栈

- FastAPI 0.136.3 + MySQL 8.4.9 + Python 3.10+
- 字符编码: UTF-8 (utf8mb4_unicode_ci)
- 环境管理: Miniforge (推荐)

## 快速启动

```bash
# 1. 创建并激活虚拟环境
conda create -n xinysoftenv python=3.13
conda activate xinysoftenv

# 2. 安装依赖
conda install -f requirements.txt

# 3. 配置数据库
mysql -u root -p xinysoft < xinysoft.sql

# 4. 运行项目
uvicorn main:app --reload
```

访问: http://127.0.0.1:8000 | API文档: http://127.0.0.1:8000/docs

## 项目结构

```
xinysoft_FastAPI/
├── config/          # 数据库配置
├── models/          # Pydantic 模型
├── routers/         # API 路由
├── main.py          # 应用入口
├── requirements.txt
└── xinysoft.sql     # 数据库脚本
```

## API 规范

**响应格式**：
```json
{
  "code": 200,
  "message": "success",
  "data": { ... }
}
```



---
name: karpathy-guidelines
description: Behavioral guidelines to reduce common LLM coding mistakes. Use when writing, reviewing, or refactoring code to avoid overcomplication, make surgical changes, surface assumptions, and define verifiable success criteria.
---

# Karpathy Guidelines

Behavioral guidelines to reduce common LLM coding mistakes, derived from [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) on LLM coding pitfalls.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.