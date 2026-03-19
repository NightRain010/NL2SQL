# 前端：页面与路由

## 模块位置

`frontend/src/views/` + `frontend/src/router/`

## 路由配置

| 路径 | 页面 | 需要认证 |
|------|------|---------|
| /login | LoginView.vue | 否 |
| / | QueryView.vue | 是 |
| /history | HistoryView.vue | 是 |
| /schema | SchemaView.vue | 是 |

路由守卫：`beforeEach` 检查 `userStore.token`，未登录重定向 `/login`。

## 页面说明

### LoginView — 登录/注册页
- 深蓝渐变背景 + 3 个流动光斑动画（blob CSS animation）
- 毛玻璃卡片（backdrop-filter: blur(24px)）
- Logo 弹入动画（scale + rotate）
- 登录/注册模式切换（isRegister ref 控制，邮箱字段用 Transition fade-up）
- 表单提交调用 `api/auth.ts` 的 login/register
- 成功后 `userStore.setToken()` + `router.push("/")`

### QueryView — 主查询页
- 粘性毛玻璃顶栏（position: sticky + backdrop-filter）
- Hero 区域：渐变文字标题（-webkit-background-clip: text）
- QueryInput 组件：搜索式输入框 + 圆形发送按钮
- 查询结果区域：SqlDisplay → summary 卡片 → ResultTable → 耗时显示
- 页面内容用 `<Transition name="fade-up">` 包裹

### HistoryView — 查询历史
- 返回按钮 + 标题顶栏
- 历史列表：状态圆点 + 问题文本 + 状态/意图标签
- 每张卡片有交错滑入动画（animationDelay）
- 空状态：图标 + 提示 + "去提问"按钮
- 底部分页器

### SchemaView — 数据库结构
- 左右分栏布局（grid: 280px 1fr）
- 左侧：SchemaTree 组件（表列表 + 骨架屏加载）
- 右侧：表详情（紫色渐变表头 + 字段列表 + PK 徽章）
- 刷新元数据按钮
- 响应式：768px 以下单列

## UI 设计体系

- CSS 变量：`--primary: #4f46e5`、`--accent: #06b6d4`
- 全局路由过渡：`<Transition name="page" mode="out-in">`
- 卡片悬浮：`.card-hover` class（translateY + shadow）
- 毛玻璃：`.glass` class
