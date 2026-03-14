<script setup lang="ts">
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { useSchemaStore } from "../stores/schema";
import { getTableList, getTableDetail, refreshMetadata } from "../api/schema";
import SchemaTree from "../components/SchemaTree.vue";
import { ElMessage } from "element-plus";

const router = useRouter();
const schemaStore = useSchemaStore();

async function fetchTables() {
  schemaStore.setLoading(true);
  try {
    const res = await getTableList();
    schemaStore.setTables(res.data.tables);
  } catch {
    /* 错误已在拦截器中处理 */
  } finally {
    schemaStore.setLoading(false);
  }
}

async function handleSelectTable(tableName: string) {
  try {
    const res = await getTableDetail(tableName);
    schemaStore.setCurrentTable(res.data);
  } catch {
    /* 错误已在拦截器中处理 */
  }
}

async function handleRefresh() {
  try {
    await refreshMetadata();
    ElMessage.success("元数据已刷新");
    await fetchTables();
  } catch {
    /* 错误已在拦截器中处理 */
  }
}

onMounted(fetchTables);
</script>

<template>
  <div class="min-h-screen">
    <header class="bg-white shadow-sm border-b border-gray-200">
      <div class="page-container flex items-center gap-4 py-4">
        <el-button @click="router.push('/')" text>← 返回查询</el-button>
        <h1 class="text-xl font-bold text-gray-800 m-0">数据库结构</h1>
        <el-button type="primary" size="small" @click="handleRefresh">刷新元数据</el-button>
      </div>
    </header>

    <main class="page-container">
      <div class="flex gap-6">
        <div class="w-280px shrink-0">
          <SchemaTree
            :tables="schemaStore.tables"
            :loading="schemaStore.loading"
            @select="handleSelectTable"
          />
        </div>

        <div class="flex-1">
          <el-card v-if="schemaStore.currentTable">
            <template #header>
              <span class="font-bold">{{ schemaStore.currentTable.table_name }}</span>
            </template>
            <el-table :data="schemaStore.currentTable.columns" stripe size="small">
              <el-table-column prop="name" label="字段名" width="160" />
              <el-table-column prop="type" label="类型" width="140" />
              <el-table-column prop="comment" label="注释" min-width="200" />
              <el-table-column label="主键" width="80">
                <template #default="{ row }">
                  <el-tag v-if="row.is_primary" type="warning" size="small">PK</el-tag>
                </template>
              </el-table-column>
              <el-table-column label="可空" width="80">
                <template #default="{ row }">
                  {{ row.is_nullable ? "是" : "否" }}
                </template>
              </el-table-column>
            </el-table>
          </el-card>

          <el-empty v-else description="请从左侧选择一张表" />
        </div>
      </div>
    </main>
  </div>
</template>
