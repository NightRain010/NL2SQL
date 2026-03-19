import { describe, it, expect } from "vitest";
import { mount } from "@vue/test-utils";
import { createPinia } from "pinia";
import QueryInput from "../../components/QueryInput.vue";

function mountQueryInput(loading = false) {
  return mount(QueryInput, {
    props: { loading },
    global: { plugins: [createPinia()] },
  });
}

describe("QueryInput", () => {
  it("应渲染输入框和提交按钮", () => {
    const wrapper = mountQueryInput();
    expect(wrapper.find("input").exists()).toBe(true);
    expect(wrapper.find("button.ask-btn").exists()).toBe(true);
  });

  it("输入不足 2 字符时不应触发 submit 事件", async () => {
    const wrapper = mountQueryInput();
    await wrapper.find("input").setValue("a");
    await wrapper.find("button.ask-btn").trigger("click");
    expect(wrapper.emitted("submit")).toBeUndefined();
  });

  it("输入 >= 2 字符后点击按钮应触发 submit 事件", async () => {
    const wrapper = mountQueryInput();
    await wrapper.find("input").setValue("张三成绩");
    await wrapper.find("button.ask-btn").trigger("click");
    expect(wrapper.emitted("submit")).toBeTruthy();
    expect(wrapper.emitted("submit")![0]).toEqual(["张三成绩"]);
  });

  it("loading 为 true 时应显示加载动画", () => {
    const wrapper = mountQueryInput(true);
    expect(wrapper.find(".btn-spinner").exists()).toBe(true);
  });
});
