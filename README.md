# xinysoft

个人作品集与项目管理网站。前台展示作品并支持项目详情浏览，后台提供作品与个人资料的管理能力。

## 技术栈

- **Vue 3** — 前端框架
- **Vite** — 构建工具
- **Vue Router** — 路由
- **Axios** — 网络请求
- **@iconify/vue** — 图标

## 功能特性

- 前台：首页、作品集列表、项目详情（含截图展示与边框特效）
- 后台：登录鉴权、仪表盘、项目增删改查、个人资料编辑
- 主题切换、Toast 提示、路由守卫

## 项目结构

```
src/
├── api/            # 接口封装（axios）
├── components/     # 通用组件与业务组件
├── composables/    # 组合式函数（鉴权、主题、Toast 等）
├── config/         # 常量配置
├── router/         # 路由与导航守卫
├── styles/         # 样式
├── utils/          # 工具函数
├── views/          # 页面视图
├── App.vue         # 根组件
├── main.js         # 应用入口
└── style.css       # 全局样式
```

## 开发命令

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview

# 代码检查
npm run lint

# 代码格式化
npm run format
```

## 提交规范

本项目所有 AI 辅助开发行为以根目录 [AI_CONSTITUTION.md](AI_CONSTITUTION.md) 为最高准则，动手前需先阅读。

提交信息受 `commit-msg` 门禁约束：

- `feat` / `fix` / `refactor` / `perf` / `test` 类型必须同时包含 `Why:` 与 `What:` 两行，否则提交被拦截
- `docs` / `chore` / `style` 类型豁免
- 无法识别的类型仅警告、不拦截（风格问题不阻塞提交）