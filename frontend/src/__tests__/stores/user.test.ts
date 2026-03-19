import { describe, it, expect, beforeEach, vi } from "vitest";
import { setActivePinia, createPinia } from "pinia";
import { useUserStore } from "../../stores/user";

const localStorageMock = (() => {
  let store: Record<string, string> = {};
  return {
    getItem: vi.fn((key: string) => store[key] ?? null),
    setItem: vi.fn((key: string, val: string) => { store[key] = val; }),
    removeItem: vi.fn((key: string) => { delete store[key]; }),
    clear: vi.fn(() => { store = {}; }),
  };
})();
Object.defineProperty(globalThis, "localStorage", { value: localStorageMock });

describe("useUserStore", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    localStorageMock.clear();
    vi.clearAllMocks();
  });

  it("初始状态 token 为空，未登录", () => {
    const store = useUserStore();
    expect(store.token).toBe("");
    expect(store.isLoggedIn).toBe(false);
    expect(store.userInfo).toBeNull();
  });

  it("setToken 应更新 token 并写入 localStorage", () => {
    const store = useUserStore();
    store.setToken("abc123");
    expect(store.token).toBe("abc123");
    expect(store.isLoggedIn).toBe(true);
    expect(localStorageMock.setItem).toHaveBeenCalledWith("token", "abc123");
  });

  it("setUserInfo 应正确保存用户信息", () => {
    const store = useUserStore();
    const info = { id: 1, username: "admin", email: "a@b.com", is_active: true };
    store.setUserInfo(info);
    expect(store.userInfo).toEqual(info);
  });

  it("logout 应清空 token、用户信息和 localStorage", () => {
    const store = useUserStore();
    store.setToken("abc");
    store.setUserInfo({ id: 1, username: "u", email: "e", is_active: true });
    store.logout();
    expect(store.token).toBe("");
    expect(store.isLoggedIn).toBe(false);
    expect(store.userInfo).toBeNull();
    expect(localStorageMock.removeItem).toHaveBeenCalledWith("token");
  });
});
