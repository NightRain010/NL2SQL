import { describe, it, expect, beforeEach } from "vitest";
import { setActivePinia, createPinia } from "pinia";
import axios from "axios";
import request from "../../api/request";

describe("Axios request 实例", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it("baseURL 应为 /api", () => {
    expect(request.defaults.baseURL).toBe("/api");
  });

  it("timeout 应为 30000ms", () => {
    expect(request.defaults.timeout).toBe(30000);
  });

  it("应配置了请求拦截器", () => {
    const interceptors = (request.interceptors.request as any).handlers;
    expect(interceptors.length).toBeGreaterThan(0);
  });

  it("应配置了响应拦截器", () => {
    const interceptors = (request.interceptors.response as any).handlers;
    expect(interceptors.length).toBeGreaterThan(0);
  });
});
