/*
 * @Author: Mrasamu
 * @Date: 2025-04-09 10:12:39
 * @LastEditors: Mrasamu
 * @LastEditTime: 2025-04-09 13:58:06
 * @description: file content
 * @FilePath: /pure-admin-thin/mock/asyncRoutes.ts
 */
// 模拟后端动态生成路由
import { defineFakeRoute } from "vite-plugin-fake-server/client";

/**
 * roles：页面级别权限，这里模拟二种 "admin"、"common"
 * admin：管理员角色
 * common：普通角色
 */
const permissionRouter = {
  path: "/permission",
  meta: {
    title: "权限管理",
    icon: "ep:lollipop",
    rank: 10
  },
  children: [
    {
      path: "/permission/page/index",
      name: "PermissionPage",
      meta: {
        title: "页面权限",
        roles: ["admin", "common"]
      }
    },
    {
      path: "/permission/button",
      meta: {
        title: "按钮权限",
        roles: ["admin", "common"]
      },
      children: [
        {
          path: "/permission/button/router",
          component: "permission/button/index",
          name: "PermissionButtonRouter",
          meta: {
            title: "路由返回按钮权限",
            auths: [
              "permission:btn:add",
              "permission:btn:edit",
              "permission:btn:delete"
            ]
          }
        },
        {
          path: "/permission/button/login",
          component: "permission/button/perms",
          name: "PermissionButtonLogin",
          meta: {
            title: "登录接口返回按钮权限"
          }
        }
      ]
    }
  ]
};

const customerRouter = {
  path: "/customer",
  redirect: "/customer/index",
  meta: {
    icon: "twemoji:billed-cap",
    // showLink: false,
    title: "用户界面目录",
    rank: 9
  },
  children: [
    {
      path: "/customer/index",
      name: "customerIndex",
      // component: () => import("@/views/customer/index.vue"),
      meta: {
        title: "用户界面",
        showParent: true
      }
    }
  ]
};

export default defineFakeRoute([
  {
    url: "/get-async-routes",
    method: "get",
    response: () => {
      return {
        success: true,
        data: [permissionRouter, customerRouter]
      };
    }
  }
]);
