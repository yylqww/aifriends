import { defineStore } from "pinia";
import { ref, type Ref } from "vue";

// 定义类型
interface UserInfo {
    user_id: number;
    username: string;
    photo: string;
    profile: string;
}

interface UserState {
    id: Ref<number>;
    username: Ref<string>;
    photo: Ref<string>;
    profile: Ref<string>;
    accessToken: Ref<string>;
}

export const useUserStore = defineStore('user', () => {
    // 状态
    const id = ref<number>(1);
    const username = ref<string>('qww');
    const photo = ref<string>('http://127.0.0.1:8000/media/user/photos/default.png');
    const profile = ref<string>('1');
    const accessToken = ref<string>('1');

    // 判断是否登录
    const isLogin = (): boolean => {
        return !!accessToken.value;
    };

    // 设置 token
    const setAccessToken = (token: string): void => {
        accessToken.value = token;
    };

    // 设置用户信息
    const setUserInfo = (data: UserInfo): void => {
        id.value = data.user_id;
        username.value = data.username;
        photo.value = data.photo;
        profile.value = data.profile;
    };

    // 登出
    const logout = (): void => {
        id.value = 0;
        username.value = '';
        photo.value = '';
        profile.value = '';
        accessToken.value = '';
    };

    return {
        id,
        username,
        photo,
        profile,
        accessToken,
        isLogin,
        setAccessToken,
        setUserInfo,
        logout,
    };
});