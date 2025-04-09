/*
 * @Aut{ baseUrlApi } from "./utils";hor: Mrasamu
 * @Date: 2025-04-09 10:12:39
 * @LastEditors: Mrasamu
 * @LastEditTime: 2025-04-09 21:07:35
 * @description: file content
 * @FilePath: /pure-admin-thin/src/api/user.ts
 */
import { http } from "@/utils/http";
import { baseUrlApi, backendUrl } from "./utils";

export type UserResult = {
  success: boolean;
  data: {
    /** 头像 */
    avatar: string;
    /** 用户名 */
    username: string;
    /** 昵称 */
    nickname: string;
    /** 当前登录用户的角色 */
    roles: Array<string>;
    /** 按钮级别权限 */
    permissions: Array<string>;
    /** `token` */
    accessToken: string;
    /** 用于调用刷新`accessToken`的接口时所需的`token` */
    refreshToken: string;
    /** `accessToken`的过期时间（格式'xxxx/xx/xx xx:xx:xx'） */
    expires: Date;
  };
};

export type RefreshTokenResult = {
  success: boolean;
  data: {
    /** `token` */
    accessToken: string;
    /** 用于调用刷新`accessToken`的接口时所需的`token` */
    refreshToken: string;
    /** `accessToken`的过期时间（格式'xxxx/xx/xx xx:xx:xx'） */
    expires: Date;
  };
};

/** 登录 */
export const getLogin = (data?: object) => {
  return http.request<UserResult>("post", baseUrlApi("login"), { data });
};

/** 刷新`token` */
export const refreshTokenApi = (data?: object) => {
  return http.request<RefreshTokenResult>("post", "/refresh-token", { data });
};

// // 获取用户列表
// export const getUserList = (params: any) => {
//   return http.request<any>("get", "/api/users", { params });
// };

// // 获取用户详情
// export const getUserDetail = (id: number) => {
//   return http.request<any>("get", `/api/users/${id}`);
// };

// // 更新用户信息
// export const updateUser = (id: number, data: any) => {
//   return http.request<any>("put", `/api/users/${id}`, { data });
// };

// // 导出用户数据
// export const exportUsers = (params: any) => {
//   return http.request<any>("get", "/api/users/export", { 
//     params,
//     responseType: "blob" 
//   });
// };

// 获取用户列表
export const getUserList = (params: any) => {
  return http.request<any>("get", `${backendUrl}/api/users`, { params });
};

// 获取用户详情
export const getUserDetail = (id: number) => {
  return http.request<any>("get", `${backendUrl}/api/users/${id}`);
};

// 更新用户信息
export const updateUser = (id: number, data: any) => {
  return http.request<any>("put", `${backendUrl}/api/users/${id}`, { data });
};

// 导出用户数据
export const exportUsers = (params: any) => {
  return http.request<any>("get", `${backendUrl}/api/users/export`, { 
    params,
    responseType: "blob" 
  });
};