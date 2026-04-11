import { defineStore } from "pinia";
import { ref } from "vue";

// 定义用户信息接口
interface UserInfo {
    user_id: number;
    username: string;
    photo: string;
    profile: string;
}

export const useUserStore = defineStore('user', () => {
    // --- 状态 (State) ---

    // 关键：初始化时直接从本地存储读取 Token，防止刷新页面后 accessToken 重置为字符串
    const accessToken = ref<string>(localStorage.getItem('access_token') || '');

    const id = ref<number>(0);
    const username = ref<string>('');
    const photo = ref<string>('');
    const profile = ref<string>('');

    // 状态锁：用于记录是否已经从后端拉取过完整的用户信息
    const hasPulledUserInfo = ref(false);

    // --- 获取器 (Getters/Functions) ---

    // 判断是否登录：只要有 Token 就认为在“登录状态”
    const isLogin = (): boolean => {
        return !!accessToken.value;
    };

    // --- 动作 (Actions) ---

    // 设置 token 并同步到本地存储
    const setAccessToken = (token: string): void => {
        accessToken.value = token;
        localStorage.setItem('access_token', token);
    };

    // 设置用户信息
    const setUserInfo = (data: UserInfo): void => {
        id.value = data.user_id;
        username.value = data.username;
        photo.value = data.photo;
        profile.value = data.profile;
        // 只要成功设置了用户信息，就自动标记为“已拉取”
        hasPulledUserInfo.value = true;
    };

    // 登出：清空内存并抹除本地存储的 Token
    const logout = (): void => {
        id.value = 0;
        username.value = '';
        photo.value = '';
        profile.value = '';
        accessToken.value = '';
        hasPulledUserInfo.value = false;
        localStorage.removeItem('access_token');
    };

    // 手动设置拉取状态（可选）
    const setHasPulledUserInfo = (newStatus: boolean) => {
        hasPulledUserInfo.value = newStatus;
    };

    return {
        id,
        username,
        photo,
        profile,
        accessToken,
        hasPulledUserInfo,
        isLogin,
        setAccessToken,
        setUserInfo,
        logout,
        setHasPulledUserInfo,
    };
});