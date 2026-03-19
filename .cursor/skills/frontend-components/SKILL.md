# 前端：组件与状态管理

## 组件位置

`frontend/src/components/`

### QueryInput.vue — 查询输入框
- Props：`loading: boolean`
- Emits：`submit(question: string)`
- 原生 `<input>` + 自定义样式（非 el-input，避免 v-model 兼容问题）
- 聚焦时：边框变紫 + 上浮 2px + 光环阴影
- 按钮：渐变圆角方形，loading 时显示旋转 spinner
- 最少输入 2 字符才可提交

### SqlDisplay.vue — SQL 展示
- Props：`sql: string, status: string`
- 深紫渐变代码块（JetBrains Mono 字体）
- 顶部 header 栏 + 状态徽章（success 绿/rejected 红/pending 黄）

### ResultTable.vue — 查询结果表格
- Props：`data: TableData`
- 自定义 header + el-table 渲染
- 空数据时显示搜索图标 + 提示文字

### LoadingState.vue — 加载状态
- 三色圆点旋转动画（indigo/cyan/violet）
- 打字机省略号效果

### SchemaTree.vue — 表结构树
- Props：`tables: TableSummary[], loading: boolean`
- Emits：`select(tableName: string)`
- 加载时显示 shimmer 骨架屏
- 每个表项有图标 + 名称 + 字段数

## 状态管理

`frontend/src/stores/`（Pinia composition API 风格）

### user.ts
- `token`：从 localStorage 初始化
- `userInfo`：用户信息
- `isLoggedIn`：computed
- `setToken() / setUserInfo() / logout()`

### query.ts
- `loading / currentResult / historyList / historyTotal`
- `setLoading() / setResult() / clearResult() / setHistory()`

### schema.ts
- `tables / currentTable / loading`
- `setTables() / setCurrentTable() / setLoading()`

## API 层

`frontend/src/api/`

### request.ts — Axios 实例
- baseURL: `/api`，timeout: 30s
- 请求拦截器：自动附加 Bearer token
- 响应拦截器：业务错误弹 ElMessage，401 自动登出跳转

### auth.ts / query.ts / schema.ts
- 对应后端各模块的 API 封装

## 测试

- `stores/user.test.ts`：4 个用例
- `stores/query.test.ts`：4 个用例
- `stores/schema.test.ts`：4 个用例
- `components/QueryInput.test.ts`：4 个用例
- `components/SqlDisplay.test.ts`：4 个用例
- `components/ResultTable.test.ts`：3 个用例
- `api/request.test.ts`：4 个用例
- `types.test.ts`：8 个用例
