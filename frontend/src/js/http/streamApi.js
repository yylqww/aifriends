import { fetchEventSource } from '@microsoft/fetch-event-source';
import { useUserStore } from "@/stores/user.js";
import api from "./api.js";
import CONFIG_API from "@/js/config/config.ts";

const BASE_URL = CONFIG_API.HTTP_URL

export default async function streamApi(url, options = {}) {
    const userStore = useUserStore();

    const controller = new AbortController();

    const startFetch = async () => {
        try {
            await fetchEventSource(BASE_URL + url, {
                method: options.method || 'POST',

                signal: controller.signal, 
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${userStore.accessToken}`,
                    ...options.headers,
                },
                body: JSON.stringify(options.body || {}),
                openWhenHidden: true,
                
                async onopen(response) {
                    if (response.status === 401) {
                        await api.post('/api/user/account/refresh_token/', {});
                        throw new Error("TOKEN_REFRESHED");
                    }
                    if (!response.ok || !response.headers.get('content-type')?.includes('text/event-stream')) {
                        const errorData = await response.json().catch(() => ({}));
                        throw new Error(errorData.detail || `请求失败: ${response.status}`);
                    }
                },

                onmessage(msg) {
                    if (msg.data === '[DONE]') {
                        if (options.onmessage) options.onmessage('', true);
                        return;
                    }
                    try {
                        const json = JSON.parse(msg.data);
                        if (options.onmessage) options.onmessage(json, false);
                    } catch (e) {
                        console.error("流解析失败:", e);
                    }
                },

                onerror(err) {
                    if (err.name === 'AbortError') {
                        throw err; 
                    }
                    if (err.message === "TOKEN_REFRESHED") {
                        return startFetch();
                    }
                    if (options.onerror) options.onerror(err);
                    throw err;
                },
                onclose: options.onclose,
            });
        } catch (err) {
            if (err.name !== 'AbortError') throw err;
        }
    };

    startFetch();

    return () => controller.abort();
}