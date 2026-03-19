import { describe, it, expect } from "vitest";
import { mount } from "@vue/test-utils";
import ElementPlus from "element-plus";
import ResultTable from "../../components/ResultTable.vue";
import type { TableData } from "../../types";

function mountResultTable(data: TableData) {
  return mount(ResultTable, {
    props: { data },
    global: { plugins: [ElementPlus] },
  });
}

describe("ResultTable", () => {
  const mockData: TableData = {
    columns: [
      { key: "name", label: "姓名", align: "left", sortable: true },
      { key: "score", label: "分数", align: "right", sortable: true },
    ],
    rows: [
      { name: "张三", score: 85 },
      { name: "李四", score: 92 },
    ],
    total_count: 2,
  };

  it("应显示总记录数", () => {
    const wrapper = mountResultTable(mockData);
    expect(wrapper.text()).toContain("2");
  });

  it("应渲染 el-table 组件", () => {
    const wrapper = mountResultTable(mockData);
    expect(wrapper.find(".el-table").exists()).toBe(true);
  });

  it("空数据时应显示 0", () => {
    const empty: TableData = { columns: [], rows: [], total_count: 0 };
    const wrapper = mountResultTable(empty);
    expect(wrapper.find(".result-count").text()).toContain("0");
  });
});
