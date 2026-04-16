/*
 * 功能：在每个请求头里自动添加`access token`。
 * 然后拦截请求结果，如果返回结果是身份认证失败（401），
 * 则说明`access_token`过期了，
 * 那么先用`cookie`中的`refresh_token`刷新`access_token`。
 * 如果刷新失败则说明`refreh_token`也过期了，
 * 则调用`user.logout()`在浏览器内存中删除登录状态；
 * 如果刷新成功，则重新发送原请求。
*/

import axios from "axios";
// 注意：下面这些纯类型导入，必须加 type 关键字
import type {
    AxiosInstance,
    InternalAxiosRequestConfig,
    AxiosResponse,
    AxiosError
} from "axios";
import { useUserStore } from "@/stores/user";
import CONFIG_API from "@/js/config/config.ts";

// 1. 定义后端返回的 Token 数据结构
interface TokenResponse {
    access: string;
    refresh?: string;
}

// 2. 扩展 AxiosRequestConfig 以包含自定义的 _retry 属性
// 这样在写 originalRequest._retry 时就不会报类型错误
interface CustomAxiosRequestConfig extends InternalAxiosRequestConfig {
    _retry?: boolean;
}

const BASE_URL = CONFIG_API.HTTP_URL

const api: AxiosInstance = axios.create({
    baseURL: BASE_URL,
    withCredentials: true,
});

// 请求拦截器
api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
    const user = useUserStore();
    if (user.accessToken && config.headers) {
        config.headers.Authorization = `Bearer ${user.accessToken}`;
    }
    return config;
});

// 3. 刷新 Token 的订阅器逻辑（增加类型支持）
let isRefreshing = false;
type RefreshCallback = (token: string | null, error?: any) => void;
let refreshSubscribers: RefreshCallback[] = [];

function subscribeTokenRefresh(callback: RefreshCallback) {
    refreshSubscribers.push(callback);
}

function onRefreshed(token: string) {
    refreshSubscribers.forEach(cb => cb(token));
    refreshSubscribers = [];
}

function onRefreshFailed(err: any) {
    refreshSubscribers.forEach(cb => cb(null, err));
    refreshSubscribers = [];
}

// 响应拦截器
api.interceptors.response.use(
    (response: AxiosResponse) => response,
    async (error: AxiosError) => {
        const user = useUserStore();
        // 强制断言为我们自定义的配置类型
        const originalRequest = error?.config as CustomAxiosRequestConfig;

        if (!originalRequest) {
            return Promise.reject(error);
        }

        // 如果返回 401 且该请求未重试过
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            return new Promise((resolve, reject) => {
                // 将当前请求挂起，等待 token 刷新
                subscribeTokenRefresh((token, err) => {
                    if (err) {
                        reject(err);
                    } else {
                        if (originalRequest.headers) {
                            originalRequest.headers.Authorization = `Bearer ${token}`;
                        }
                        resolve(api(originalRequest));
                    }
                });

                if (!isRefreshing) {
                    isRefreshing = true;
                    // 使用 axios 原生实例去请求刷新，避免进入拦截器死循环
                    axios.post<TokenResponse>(
                        `${BASE_URL}/api/user/account/refresh_token/`,
                        {},
                        { withCredentials: true, timeout: 5000 }
                    ).then(res => {
                        const newAccessToken = res.data.access;
                        user.setAccessToken(newAccessToken);
                        onRefreshed(newAccessToken);
                    }).catch(err => {
                        user.logout();
                        onRefreshFailed(err);
                        reject(err);
                    }).finally(() => {
                        isRefreshing = false;
                    });
                }
            });
        }

        return Promise.reject(error);
    }
);

export default api;