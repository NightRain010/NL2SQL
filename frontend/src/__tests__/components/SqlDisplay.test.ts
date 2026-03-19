import { describe, it, expect } from "vitest";
import { mount } from "@vue/test-utils";
import SqlDisplay from "../../components/SqlDisplay.vue";

function mountSqlDisplay(sql: string, status: string) {
  return mount(SqlDisplay, { props: { sql, status } });
}

describe("SqlDisplay", () => {
  it("应渲染 SQL 文本", () => {
    const wrapper = mountSqlDisplay("SELECT * FROM students", "success");
    expect(wrapper.find("code").text()).toBe("SELECT * FROM students");
  });

  it("应显示状态标签", () => {
    const wrapper = mountSqlDisplay("SELECT 1", "success");
    const badge = wrapper.find(".status-badge");
    expect(badge.exists()).toBe(true);
    expect(badge.text()).toBe("成功");
  });

  it("success 状态标签应有 success class", () => {
    const wrapper = mountSqlDisplay("SELECT 1", "success");
    expect(wrapper.find(".status-badge").classes()).toContain("success");
  });

  it("rejected 状态标签应有 rejected class", () => {
    const wrapper = mountSqlDisplay("SELECT 1", "rejected");
    expect(wrapper.find(".status-badge").classes()).toContain("rejected");
  });
});
