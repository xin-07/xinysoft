# API 接口文档

## 1. 概述

### 1.1 基本信息

| 项目 | 说明 |
|------|------|
| **项目名称** | xinysoft 个人作品集 API |
| **版本** | 1.3.0 |
| **Base URL** | `http://127.0.0.1:8000` |
| **API 文档** | `http://127.0.0.1:8000/docs` (Swagger UI) |
| **字符编码** | UTF-8 (utf8mb4_unicode_ci) |
| **协议** | HTTP |

### 1.2 接口概览

| 接口名称 | 方法 | 路径 | 说明 |
|---------|------|------|------|
| 根路径测试 | GET | `/` | 测试服务是否正常运行 |
| Hello 测试接口 | GET | `/hello/{name}` | 测试动态路由功能 |
| 获取个人资料 | GET | `/api/profile` | 获取个人资料信息 |
| 获取头像图片 | GET | `/api/avatar/{file_path:path}` | 获取头像图片资源 |
| 获取项目图片文件 | GET | `/api/files/{file_path:path}` | 获取项目封面图、截图等图片资源 |
| 获取项目列表 | GET | `/api/projects` | 获取项目作品集列表（支持分页和筛选） |
| 获取项目详情 | GET | `/api/projects/{id}` | 获取单个项目的详细信息 |
| 管理员登录 | POST | `/api/admin/login` | 管理员登录，获取 JWT Token |
| 验证 Token | POST | `/api/admin/verify` | 验证 JWT Token 有效性 |
| 获取项目列表（管理） | GET | `/api/admin/projects` | 获取所有项目（含草稿），支持分页 |
| 获取项目详情（管理） | GET | `/api/admin/projects/{id}` | 获取单个项目详情（含草稿） |
| 新增项目 | POST | `/api/admin/projects` | 创建新项目 |
| 编辑项目 | PUT | `/api/admin/projects/{id}` | 更新项目信息 |
| 删除项目 | DELETE | `/api/admin/projects/{id}` | 删除项目 |
| 切换项目状态 | PATCH | `/api/admin/projects/{id}/status` | 切换项目发布/草稿状态 |
| 获取个人资料（管理） | GET | `/api/admin/profile` | 获取个人资料信息 |
| 更新个人资料 | PUT | `/api/admin/profile` | 更新个人资料 |
| 上传文件 | POST | `/api/admin/upload` | 上传图片文件（封面/截图） |

---

## 2. 通用说明

### 2.1 响应格式

#### 成功响应

```json
{
  "code": 200,
  "message": "success",
  "data": { ... }
}
```

#### 错误响应

```json
{
  "code": 400,
  "message": "错误描述",
  "data": null
}
```

### 2.2 错误码说明

| 错误码 | 说明 | 处理建议 |
|--------|------|----------|
| 200 | 成功 | - |
| 400 | 请求参数错误 | 检查请求参数格式和类型 |
| 401 | 未认证/Token 无效 | 重新登录获取有效 Token |
| 403 | 无权访问 | 检查访问权限或路径是否合法 |
| 404 | 资源不存在 | 检查请求路径和资源ID |
| 429 | 操作过于频繁 | 稍后重试 |
| 500 | 服务器内部错误 | 联系管理员或稍后重试 |

### 2.3 性能要求

- API 响应时间 < 100ms
- 数据库异常时返回默认数据，保证前端可用

### 2.4 安全措施

- 防止 SQL 注入（使用参数化查询）
- 防止 XSS 攻击
- CORS 配置支持跨域访问
- 文件访问路径限制（防止路径遍历攻击）

---

## 3. 接口详情

### 3.1 根路径测试

测试服务是否正常运行。

**基本信息**

| 项目 | 说明 |
|------|------|
| **接口路径** | `GET /` |
| **接口说明** | 测试服务是否正常运行 |
| **认证方式** | 无需认证 |

**请求参数**

无

**响应示例**

```json
{
  "code": 200,
  "message": "Welcome to xinysoft API",
  "data": null
}
```

---

### 3.2 Hello 测试接口

测试动态路由功能。

**基本信息**

| 项目 | 说明 |
|------|------|
| **接口路径** | `GET /hello/{name}` |
| **接口说明** | 测试动态路由功能 |
| **认证方式** | 无需认证 |

**请求参数**

| 参数名 | 类型 | 必填 | 位置 | 说明 |
|--------|------|------|------|------|
| name | string | 是 | Path | 用户名 |

**响应示例**

**成功响应 (200)**

```json
{
  "code": 200,
  "message": "Hello xiny",
  "data": null
}
```

---

### 3.3 获取个人资料

获取个人资料信息，用于前端 Hero 区域展示。

**基本信息**

| 项目 | 说明 |
|------|------|
| **接口路径** | `GET /api/profile` |
| **接口说明** | 获取个人资料信息，用于前端 Hero 区域展示 |
| **认证方式** | 无需认证 |

**请求参数**

无

**响应参数**

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键ID |
| name | string | 姓名 |
| avatar_url | string | 头像访问 URL（已转换为可访问的 API URL） |
| title | string | 头衔/职位 |
| bio | string | 个人简介 |
| tech_tags | array | 技术标签数组 |
| github | string | GitHub 链接 |
| gitee | string | Gitee 链接 |
| wechat | string | 微信号 |
| qq | string | QQ号 |
| email | array | 邮箱列表 |
| created_at | datetime | 创建时间 |
| updated_at | datetime | 更新时间 |

**头像 URL 说明**

- `avatar_url` 字段返回的是可直接访问的 API URL
- 前端可以直接使用该 URL 加载图片：`<img src="/api/avatar/D:/File/photos/%E8%90%BD%E6%97%A5.jpg" />`
- 本地路径会自动转换为 URL 格式并进行 URL 编码

**响应示例**

**成功响应 (200)**

```json
{
  "id": 1,
  "name": "xiny",
  "avatar_url": "/api/avatar/D:/File/photos/%E8%90%BD%E6%97%A5.jpg",
  "title": "全栈开发工程师 · AI Agent 探索者",
  "bio": "持续追踪 AI Agent 前沿技术，通过实践快速掌握。具备跨专业协作能力，坚持每周技术复盘。",
  "tech_tags": ["Vue3", "FastAPI", "MySQL", "OpenClaw", "HarmonyOS", "ECharts"],
  "github": "https://github.com/xin-07",
  "gitee": "https://gitee.com/xin-keep-going",
  "wechat": "Yyk-293342",
  "qq": "2074835619",
  "email": ["2074835619@qq.com", "xin_y0607@outlook.com", "xiny0607.23@gmail.com"],
  "created_at": "2026-06-09 18:50:32",
  "updated_at": "2026-06-09 18:54:38"
}
```

**异常响应**

当数据库连接异常时，接口会返回默认数据，保证前端可用：

```json
{
  "id": 1,
  "name": "xiny",
  "avatar_url": null,
  "title": "全栈开发工程师 · AI Agent 探索者",
  "bio": "持续追踪 Vue3 与 AI Agent 前沿技术，通过实践快速掌握。具备跨专业协作能力，坚持每周技术复盘。",
  "tech_tags": ["Vue3", "FastAPI", "MySQL", "OpenClaw", "HarmonyOS", "ECharts"],
  "github": "https://github.com/xin-07",
  "gitee": "https://gitee.com/xin-keep-going",
  "wechat": "Yyk-293342",
  "qq": "2074835619",
  "email": ["2074835619@qq.com", "xin_y0607@outlook.com", "xiny0607.23@gmail.com"],
  "created_at": null,
  "updated_at": null
}
```

---

### 3.4 获取头像图片

将本地头像文件路径转换为可访问的 URL，供前端加载图片。

**基本信息**

| 项目 | 说明 |
|------|------|
| **接口路径** | `GET /api/avatar/{file_path:path}` |
| **接口说明** | 将本地头像文件路径转换为可访问的 URL，供前端加载图片 |
| **认证方式** | 无需认证 |
| **响应类型** | image/* |

**请求参数**

| 参数名 | 类型 | 必填 | 位置 | 说明 |
|--------|------|------|------|------|
| file_path | string | 是 | Path | 本地文件路径（URL 编码后的） |

**路径格式说明**

- Windows 路径需要转换为 URL 格式：`D:\File\photos\落日.jpg` → `D:/File/photos/落日.jpg`
- 特殊字符（如中文）会自动进行 URL 编码
- 示例：`/api/avatar/D:/File/photos/%E8%90%BD%E6%97%A5.jpg`

**响应示例**

**成功响应 (200)**

返回图片文件，Content-Type 根据图片类型自动设置：

| 文件扩展名 | Content-Type |
|-----------|--------------|
| .jpg / .jpeg | image/jpeg |
| .png | image/png |
| .gif | image/gif |
| .webp | image/webp |

**错误响应**

**文件不存在 (404)**

```json
{
  "detail": "文件不存在"
}
```

**无权访问 (403)**

```json
{
  "detail": "无权访问此文件"
}
```

**安全限制**

- 只允许访问特定目录（当前配置：`D:\File\photos`）
- 防止路径遍历攻击
- 自动验证文件路径是否在允许范围内

**使用示例**

前端可以直接使用返回的 URL：

```html
<img src="/api/avatar/D:/File/photos/%E8%90%BD%E6%97%A5.jpg" alt="头像" />
```

---

### 3.5 获取项目图片文件

将本地项目图片文件路径转换为可访问的 URL，供前端加载封面图和截图。

**基本信息**

| 项目 | 说明 |
|------|------|
| **接口路径** | `GET /api/files/{file_path:path}` |
| **接口说明** | 将本地项目图片文件路径转换为可访问的 URL，供前端加载封面图和截图 |
| **认证方式** | 无需认证 |
| **响应类型** | image/* |

**请求参数**

| 参数名 | 类型 | 必填 | 位置 | 说明 |
|--------|------|------|------|------|
| file_path | string | 是 | Path | 本地文件路径（URL 编码后的） |

**路径格式说明**

- Windows 路径需要转换为 URL 格式：`D:\Project\web\xinysoft_Vite\public\鲜途智送.png` → `D:/Project/web/xinysoft_Vite/public/鲜途智送.png`
- 特殊字符（如中文）会自动进行 URL 编码
- 示例：`/api/files/D:/Project/web/xinysoft_Vite/public/%E9%B2%9C%E9%80%94%E6%99%BA%E9%80%81.png`

**响应示例**

**成功响应 (200)**

返回图片文件，Content-Type 根据图片类型自动设置：

| 文件扩展名 | Content-Type |
|-----------|--------------|
| .jpg / .jpeg | image/jpeg |
| .png | image/png |
| .gif | image/gif |
| .webp | image/webp |

**错误响应**

**文件不存在 (404)**

```json
{
  "detail": "文件不存在"
}
```

**无权访问 (403)**

```json
{
  "detail": "无权访问此文件"
}
```

**安全限制**

- 只允许访问特定目录（当前配置：`D:\Project\web\xinysoft_Vite\public`、`D:\File\photos`）
- 防止路径遍历攻击
- 自动验证文件路径是否在允许范围内

**使用示例**

前端可以直接使用返回的 URL：

```html
<img src="/api/files/D:/Project/web/xinysoft_Vite/public/%E9%B2%9C%E9%80%94%E6%99%BA%E9%80%81.png" alt="鲜途智送" />
```

---
### 3.6 获取项目列表

获取项目作品集列表，支持分页和筛选功能。

**基本信息**

| 项目 | 说明 |
|------|------|
| **接口路径** | `GET /api/projects` |
| **接口说明** | 获取项目作品集列表，支持分页和筛选功能 |
| **认证方式** | 无需认证 |

**请求参数**

| 参数名 | 类型 | 必填 | 位置 | 默认值 | 说明 |
|--------|------|------|------|--------|------|
| page | int | 否 | Query | 1 | 页码 |
| page_size | int | 否 | Query | 10 | 每页条数 |
| featured | bool | 否 | Query | false | 是否只返回精选项目 |

**响应参数**

| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| message | string | 响应消息 |
| data | object | 响应数据 |
| data.total | int | 项目总数 |
| data.page | int | 当前页码 |
| data.page_size | int | 每页条数 |
| data.items | array | 项目列表 |
| items[].id | int | 项目ID |
| items[].title | string | 项目名称 |
| items[].subtitle | string | 项目副标题 |
| items[].description | string | 项目描述 |
| items[].tech_stack | array | 技术栈数组 |
| items[].cover_url | string | 封面图 URL（已自动转换为 /api/files/ 可访问链接） |
| items[].screenshots | array | 截图 URL 列表（已自动转换为 /api/files/ 可访问链接） |
| items[].live_url | string | 线上地址 |
| items[].repo_url | string | 源码地址 |
| items[].is_featured | bool | 是否精选 |
| items[].sort_order | int | 排序权重 |
| items[].created_at | datetime | 创建时间 |
| items[].updated_at | datetime | 更新时间 |

**排序规则**

- 按 `sort_order` 降序排列（数值越大越靠前）
- 只返回 `status='published'` 的项目

**图片 URL 说明**

- `cover_url` 和 `screenshots` 中返回的是可直接访问的 `/api/files/` 格式 URL
- 数据库存储原始本地路径（如 `D:\Project\web\...\xxx.png`），接口层自动转换
- 前端可以直接使用：`<img :src="item.cover_url" />`

**响应示例**

**成功响应 (200)**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 3,
    "page": 1,
    "page_size": 10,
    "items": [
      {
        "id": 1,
        "title": "智能路径规划与物流配送系统",
        "subtitle": "鲜途智送 · 物流配送智能管理平台",
        "description": "基于 Vue 3 的智能路径优化与物流配送管理系统...",
        "tech_stack": ["Vue 3", "Vite", "Three.js", "天地图 API", "ECharts", "Flask", "MySQL", "Redis", "蚂蚁群+粒子群混合算法"],
        "cover_url": null,
        "screenshots": [
          "/api/files/D:/Project/web/xinysoft_Vite/public/鲜途智送-首页.png",
          "/api/files/D:/Project/web/xinysoft_Vite/public/鲜途智送-主页.png",
          "/api/files/D:/Project/web/xinysoft_Vite/public/鲜途智送-底部订单管理.png"
        ],
        "live_url": "https://smile050417.site/",
        "repo_url": null,
        "is_featured": true,
        "sort_order": 3,
        "created_at": "2026-06-10 18:50:40",
        "updated_at": "2026-06-10 18:50:40"
      }
    ]
  }
}
```

**筛选精选项目**

请求 `GET /api/projects?featured=true` 只返回 `is_featured=true` 的项目：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 3,
    "page": 1,
    "page_size": 10,
    "items": [
      {
        "id": 1,
        "title": "智能路径规划与物流配送系统",
        "subtitle": "鲜途智送 · 物流配送智能管理平台",
        ...
      },
      {
        "id": 2,
        "title": "昕悦读 分布式小说阅读系统",
        "subtitle": "HarmonyOS 原生小说阅读应用",
        ...
      },
      {
        "id": 3,
        "title": "xinysoft 个人作品集",
        "subtitle": "Vue 3 + FastAPI 全栈个人网站",
        ...
      }
    ]
  }
}
```

**异常响应**

当数据库连接异常时，接口会返回空列表，保证前端可用：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 0,
    "page": 1,
    "page_size": 10,
    "items": []
  }
}
```

---

### 3.7 获取项目详情

获取单个项目的详细信息。

**基本信息**

| 项目 | 说明 |
|------|------|
| **接口路径** | `GET /api/projects/{id}` |
| **接口说明** | 获取单个项目的详细信息 |
| **认证方式** | 无需认证 |

**请求参数**

| 参数名 | 类型 | 必填 | 位置 | 说明 |
|--------|------|------|------|------|
| id | int | 是 | Path | 项目ID |

**响应参数**

| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| message | string | 响应消息 |
| data | object | 项目详情数据 |
| data.id | int | 项目ID |
| data.title | string | 项目名称 |
| data.subtitle | string | 项目副标题 |
| data.description | string | 项目描述 |
| data.tech_stack | array | 技术栈数组 |
| data.cover_url | string | 封面图 URL（已自动转换为 /api/files/ 可访问链接） |
| data.screenshots | array | 截图 URL 列表（已自动转换为 /api/files/ 可访问链接） |
| data.live_url | string | 线上地址 |
| data.repo_url | string | 源码地址 |
| data.is_featured | bool | 是否精选 |
| data.sort_order | int | 排序权重 |
| data.created_at | datetime | 创建时间 |
| data.updated_at | datetime | 更新时间 |

**响应示例**

**成功响应 (200)**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "title": "智能路径规划与物流配送系统",
    "subtitle": "鲜途智送 · 物流配送智能管理平台",
    "description": "基于 Vue 3 的智能路径优化与物流配送管理系统，集成天地图 API，提供路径规划、团队协作、仓库管理、大屏数据可视化等功能。后端采用 Flask 框架，使用混合蚁群-粒子群优化算法解决车辆路径问题(VRP)，实现高效的配送路线规划。",
    "tech_stack": ["Vue 3", "Vite", "Three.js", "天地图 API", "ECharts", "Flask", "MySQL", "Redis", "蚂蚁群+粒子群混合算法"],
    "cover_url": null,
    "screenshots": [
      "/api/files/D:/Project/web/xinysoft_Vite/public/鲜途智送-首页.png",
      "/api/files/D:/Project/web/xinysoft_Vite/public/鲜途智送-主页.png",
      "/api/files/D:/Project/web/xinysoft_Vite/public/鲜途智送-底部订单管理.png"
    ],
    "live_url": "https://smile050417.site/",
    "repo_url": null,
    "is_featured": true,
    "sort_order": 3,
    "created_at": "2026-06-10 18:50:40",
    "updated_at": "2026-06-10 18:50:40"
  }
}
```

**项目不存在 (404)**

```json
{
  "code": 404,
  "message": "项目不存在",
  "data": null
}
```

---

---

## 4. 管理后台 API

管理后台接口需要 Bearer Token 认证，除 `/api/admin/login` 外所有接口都需要在请求头中携带 Token：
```
Authorization: Bearer <jwt_token>
```

---

### 4.1 管理员登录

管理员登录，获取 JWT Token。

**基本信息**

| 项目 | 说明 |
|------|------|
| **接口路径** | `POST /api/admin/login` |
| **接口说明** | 管理员登录，验证用户名密码，返回 JWT Token |
| **认证方式** | 无需认证 |

**请求参数**

| 参数名 | 类型 | 必填 | 位置 | 说明 |
|--------|------|------|------|------|
| username | string | 是 | Body | 管理员用户名 |
| password | string | 是 | Body | 管理员密码 |

**响应示例**

**成功响应 (200)**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
}
```

**错误响应**

用户名或密码错误 (401):
```json
{
  "code": 401,
  "message": "用户名或密码错误",
  "data": null
}
```

操作过于频繁 (429):
```json
{
  "code": 429,
  "message": "操作过于频繁，请稍后再试",
  "data": null
}
```

---

### 4.2 验证 Token

验证 JWT Token 有效性。

**基本信息**

| 项目 | 说明 |
|------|------|
| **接口路径** | `POST /api/admin/verify` |
| **接口说明** | 验证 JWT Token 是否有效 |
| **认证方式** | Bearer Token |

**请求参数**

无（Token 在请求头中）

**响应示例**

**成功响应 (200)**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "username": "admin"
  }
}
```

**错误响应** (401):
```json
{
  "detail": "未认证或Token已过期"
}
```

---

### 4.3 获取项目列表（管理端）

获取所有项目列表，包含已发布和草稿。

**基本信息**

| 项目 | 说明 |
|------|------|
| **接口路径** | `GET /api/admin/projects` |
| **接口说明** | 获取所有项目列表（不限状态），支持分页 |
| **认证方式** | Bearer Token |

**请求参数**

| 参数名 | 类型 | 必填 | 位置 | 默认值 | 说明 |
|--------|------|------|------|--------|------|
| page | int | 否 | Query | 1 | 页码 |
| page_size | int | 否 | Query | 10 | 每页条数 |

**响应参数**

| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| message | string | 响应消息 |
| data | object | 响应数据 |
| data.total | int | 项目总数 |
| data.page | int | 当前页码 |
| data.page_size | int | 每页条数 |
| data.items | array | 项目列表（格式同公开接口） |

---

### 4.4 获取项目详情（管理端）

获取单个项目详情，包含已发布和草稿。

**基本信息**

| 项目 | 说明 |
|------|------|
| **接口路径** | `GET /api/admin/projects/{id}` |
| **接口说明** | 获取单个项目详情（不限状态） |
| **认证方式** | Bearer Token |

**请求参数**

| 参数名 | 类型 | 必填 | 位置 | 说明 |
|--------|------|------|------|------|
| id | int | 是 | Path | 项目ID |

**响应参数**

格式同公开接口 `/api/projects/{id}`。

**项目不存在 (404):**
```json
{
  "code": 404,
  "message": "项目不存在",
  "data": null
}
```

---

### 4.5 新增项目

创建新项目。

**基本信息**

| 项目 | 说明 |
|------|------|
| **接口路径** | `POST /api/admin/projects` |
| **接口说明** | 创建新项目 |
| **认证方式** | Bearer Token |

**请求参数 (JSON Body)**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| title | string | 是 | 项目标题（1-100 字符） |
| subtitle | string | 否 | 项目副标题 |
| description | string | 否 | 项目描述 |
| tech_stack | array[string] | 否 | 技术栈数组 |
| cover_url | string | 否 | 封面图本地路径 |
| screenshots | array[string] | 否 | 截图本地路径数组 |
| live_url | string | 否 | 在线演示地址 |
| repo_url | string | 否 | 仓库地址 |
| is_featured | bool | 否 | 是否精选项目，默认 false |
| sort_order | int | 否 | 排序权重，默认 0 |

**响应示例**

成功返回新项目完整数据（同获取项目详情）。

---

### 4.6 编辑项目

更新项目信息，仅更新提供的字段。

**基本信息**

| 项目 | 说明 |
|------|------|
| **接口路径** | `PUT /api/admin/projects/{id}` |
| **接口说明** | 编辑项目，未提供的字段保持原值 |
| **认证方式** | Bearer Token |

**请求参数**

参数同新增项目，但所有字段均为可选。

**响应示例**

成功返回更新后的项目完整数据。

**项目不存在 (404):**
```json
{
  "code": 404,
  "message": "项目不存在",
  "data": null
}
```

---

### 4.7 删除项目

物理删除项目。

**基本信息**

| 项目 | 说明 |
|------|------|
| **接口路径** | `DELETE /api/admin/projects/{id}` |
| **接口说明** | 物理删除项目 |
| **认证方式** | Bearer Token |

**请求参数**

| 参数名 | 类型 | 必填 | 位置 | 说明 |
|--------|------|------|------|------|
| id | int | 是 | Path | 项目ID |

**响应示例**

**成功响应 (200):**
```json
{
  "code": 200,
  "message": "删除成功",
  "data": null
}
```

---

### 4.8 切换项目状态

切换项目发布/草稿状态。

**基本信息**

| 项目 | 说明 |
|------|------|
| **接口路径** | `PATCH /api/admin/projects/{id}/status` |
| **接口说明** | 仅更新项目状态 |
| **认证方式** | Bearer Token |

**请求参数**

| 参数名 | 类型 | 必填 | 位置 | 说明 |
|--------|------|------|------|------|
| status | string | 是 | Body | 状态，必须是 `published` 或 `draft` |

**响应示例**

成功返回更新后的项目完整数据。

---

### 4.9 获取个人资料（管理端）

获取个人资料信息。

**基本信息**

| 项目 | 说明 |
|------|------|
| **接口路径** | `GET /api/admin/profile` |
| **接口说明** | 获取个人资料信息 |
| **认证方式** | Bearer Token |

**响应参数**

格式同公开接口 `/api/profile`。

---

### 4.10 更新个人资料

更新个人资料信息。

**基本信息**

| 项目 | 说明 |
|------|------|
| **接口路径** | `PUT /api/admin/profile` |
| **接口说明** | 更新个人资料（更新 id=1 记录） |
| **认证方式** | Bearer Token |

**请求参数 (JSON Body)**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| name | string | 否 | 姓名 |
| avatar_url | string | 否 | 头像本地路径 |
| title | string | 否 | 头衔 |
| bio | string | 否 | 个人简介 |
| tech_tags | array[string] | 否 | 技术标签数组 |
| github | string | 否 | GitHub 链接 |
| gitee | string | 否 | Gitee 链接 |
| wechat | string | 否 | 微信号 |
| qq | string | 否 | QQ号 |
| email | array[string] | 否 | 邮箱列表 |

所有字段均为可选，仅更新提供的字段。

**响应示例**

成功返回更新后的个人资料完整数据。

---

### 4.11 上传文件

上传图片文件（封面、截图、头像等）。

**基本信息**

| 项目 | 说明 |
|------|------|
| **接口路径** | `POST /api/admin/upload` |
| **接口说明** | 上传图片文件，支持 .jpg/.png/.webp，最大 5MB |
| **认证方式** | Bearer Token |

**请求参数**

| 参数名 | 类型 | 必填 | 位置 | 说明 |
|--------|------|------|------|------|
| file | file | 是 | Form-Data | 上传的图片文件 |

**响应示例**

**成功响应 (200):**
```json
{
  "code": 200,
  "message": "上传成功",
  "data": {
    "url": "/api/files/D:/File/photos/uploads/2026-06-12/abc12345.png"
  }
}
```

返回的 URL 可直接用于前端展示，也可以填入 `cover_url` / `avatar_url` 等字段。

**错误响应:**

文件大小超限 (400):
```json
{
  "code": 400,
  "message": "文件大小不能超过 5MB",
  "data": null
}
```

不支持的文件格式 (400):
```json
{
  "code": 400,
  "message": "不支持的文件格式，仅允许 .jpg .jpeg .png .webp",
  "data": null
}
```

---

## 5. 测试指南

### 5.1 使用 Swagger UI

访问 `http://127.0.0.1:8000/docs` 可以查看交互式 API 文档，并直接测试接口。

### 5.2 使用 curl

```bash
# 测试根路径
curl http://127.0.0.1:8000/

# 测试 Hello 接口
curl http://127.0.0.1:8000/hello/xiny

# 测试个人资料接口
curl http://127.0.0.1:8000/api/profile

# 测试头像接口
curl http://127.0.0.1:8000/api/avatar/D:/File/photos/%E8%90%BD%E6%97%A5.jpg

# 测试项目图片文件接口
curl http://127.0.0.1:8000/api/files/D:/Project/web/xinysoft_Vite/public/%E9%B2%9C%E9%80%94%E6%99%BA%E9%80%81.png

# 测试项目列表接口
curl http://127.0.0.1:8000/api/projects

# 测试项目列表接口（带分页参数）
curl http://127.0.0.1:8000/api/projects?page=1&page_size=5

# 测试项目列表接口（筛选精选项目）
curl http://127.0.0.1:8000/api/projects?featured=true

# 测试项目详情接口
curl http://127.0.0.1:8000/api/projects/1

# 管理员登录获取 Token
curl -X POST -H "Content-Type: application/json" -d '{"username":"admin","password":"admin123"}' http://127.0.0.1:8000/api/admin/login
```

### 5.3 使用浏览器

直接在浏览器中访问接口 URL 即可查看返回结果。

---

## 6. 更新日志

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0.0 | 2026-06-09 | 初始版本发布 |
| 1.1.0 | 2026-06-10 | 新增项目作品集 API：GET /api/projects（项目列表）、GET /api/projects/{id}（项目详情） |
| 1.2.0 | 2026-06-11 | 新增通用文件服务 API：GET /api/files/{file_path}；项目列表/详情接口自动转换 cover_url 和 screenshots 为可访问 URL |
| 1.3.0 | 2026-06-12 | 新增管理后台 API：11 个接口（登录、项目 CRUD、个人资料编辑、文件上传） |