<template>
  <div class="main-container">
    <!-- 筛选区域 -->
    <el-card class="filter-container mb-4">
      <el-form :model="queryParams" label-width="100px">
        <el-row :gutter="20">
          <el-col :xs="24" :sm="12" :md="8" :lg="6">
            <el-form-item label="手机号码">
              <el-input
                v-model="queryParams.mobile"
                placeholder="请输入手机号码"
                clearable
              />
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="12" :md="8" :lg="6">
            <el-form-item label="性别">
              <el-select
                v-model="queryParams.gender"
                placeholder="请选择性别"
                clearable
                style="width: 100%"
              >
                <el-option label="男" :value="1" />
                <el-option label="女" :value="2" />
                <el-option label="未知" :value="0" />
              </el-select>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="12" :md="8" :lg="6">
            <el-form-item label="会员状态">
              <el-select
                v-model="queryParams.isMember"
                placeholder="请选择会员状态"
                clearable
                style="width: 100%"
              >
                <el-option label="是" :value="1" />
                <el-option label="否" :value="0" />
              </el-select>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="12" :md="8" :lg="6">
            <el-form-item label="微信昵称">
              <el-input
                v-model="queryParams.wechatName"
                placeholder="请输入微信昵称"
                clearable
              />
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="12" :md="8" :lg="6">
            <el-form-item label="微信备注">
              <el-input
                v-model="queryParams.wechatRemark"
                placeholder="请输入微信备注"
                clearable
              />
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="12" :md="12" :lg="8">
            <el-form-item label="交易次数">
              <div class="trade-count-container">
                <el-input-number
                  v-model="queryParams.minTradeCount"
                  placeholder="最小"
                  :min="0"
                  controls-position="right"
                  :precision="0"
                  style="width: 45%"
                />
                <span class="mx-2">-</span>
                <el-input-number
                  v-model="queryParams.maxTradeCount"
                  placeholder="最大"
                  :min="0"
                  controls-position="right"
                  :precision="0"
                  style="width: 45%"
                />
              </div>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="24" :md="12" :lg="8">
            <el-form-item label="注册时间">
              <el-date-picker
                v-model="queryParams.dateRange"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="12" :md="8" :lg="6">
            <el-form-item label="标签">
              <el-select
                v-model="queryParams.tags"
                multiple
                collapse-tags
                placeholder="请选择标签"
                clearable
                style="width: 100%"
              >
                <el-option
                  v-for="tag in tagOptions"
                  :key="tag.value"
                  :label="tag.label"
                  :value="tag.value"
                />
              </el-select>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="24" :md="24" :lg="24" class="flex-end">
            <el-form-item>
              <el-button type="primary" @click="handleQuery">查询</el-button>
              <el-button @click="resetQuery">重置</el-button>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </el-card>

    <!-- 表格区域 -->
    <el-card>
      <div class="toolbar mb-4">
        <el-button type="primary" @click="handleExport">导出</el-button>
      </div>

      <el-table
        v-loading="loading"
        :data="userList"
        border
        stripe
        style="width: 100%"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="user_id" label="ID" width="80" />
        <el-table-column prop="mobile" label="手机号码" width="120" />
        <el-table-column prop="yz_show_name" label="用户名" width="120" />
        <el-table-column label="性别" width="80">
          <template #default="{ row }">
            <span v-if="row.yz_gender === 1">男</span>
            <span v-else-if="row.yz_gender === 2">女</span>
            <span v-else>未知</span>
          </template>
        </el-table-column>
        <el-table-column label="会员状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.yz_is_member ? 'success' : 'info'">
              {{ row.yz_is_member ? "是" : "否" }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="yz_trade_count" label="交易次数" width="100" />
        <el-table-column prop="yz_points" label="积分" width="100" />
        <el-table-column label="手机认证" width="100">
          <template #default="{ row }">
            <el-tag :type="row.yz_is_mobile_auth ? 'success' : 'info'">
              {{ row.yz_is_mobile_auth ? "已认证" : "未认证" }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="wechat_name" label="微信昵称" width="120" />
        <el-table-column prop="wechat_remark" label="微信备注" width="120" />
        <el-table-column label="所在地区" width="150">
          <template #default="{ row }">
            {{ row.wechat_province }} {{ row.wechat_city }}
          </template>
        </el-table-column>
        <el-table-column label="标签" min-width="200">
          <template #default="{ row }">
            <el-tag
              v-for="(tag, index) in getTagsArray(row.wechat_labels)"
              :key="index"
              class="mx-1"
              size="small"
            >
              {{ tag }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="yz_created_at" label="注册时间" width="180" />
        <el-table-column fixed="right" label="操作" width="150">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleView(row)"
              >查看</el-button
            >
            <el-button link type="primary" @click="handleEdit(row)"
              >编辑</el-button
            >
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { getUserList, exportUsers } from "@/api/user";

// 定义用户类型
interface User {
  user_id: number;
  mobile: string;
  yz_gender: number;
  yz_is_member: number;
  yz_trade_count: number;
  yz_show_name: string;
  yz_is_mobile_auth: boolean;
  yz_open_id: string;
  yz_created_at: string;
  yz_points: number;
  wechat_name: string;
  wechat_friend_record_id: string;
  wechat_remark: string;
  wechat_gender: number;
  wechat_province: string;
  wechat_city: string;
  wechat_account_id: string;
  wechat_labels: string;
  wechat_extend_fileds: string;
  wechat_system_tags: string;
}

// 查询参数
const queryParams = reactive({
  mobile: "",
  gender: null as number | null,
  isMember: null as number | null,
  minTradeCount: null as number | null,
  maxTradeCount: null as number | null,
  wechatName: "",
  wechatRemark: "",
  dateRange: [] as string[],
  tags: [] as string[]
});

// 标签选项
const tagOptions = ref([
  { label: "新客户", value: "新客户" },
  { label: "老客户", value: "老客户" },
  { label: "VIP", value: "VIP" },
  { label: "高消费", value: "高消费" },
  { label: "流失客户", value: "流失客户" }
]);

// 分页参数
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
});

// 原始用户数据（全部数据）
const allUsers = ref<User[]>([]);
// 过滤后的用户列表数据（显示数据）
const userList = computed(() => {
  // 先过滤
  const filteredUsers = allUsers.value.filter(user => {
    // 手机号筛选
    if (queryParams.mobile && !user.mobile.includes(queryParams.mobile)) {
      return false;
    }

    // 性别筛选
    if (queryParams.gender !== null && user.yz_gender !== queryParams.gender) {
      return false;
    }

    // 会员状态筛选
    if (
      queryParams.isMember !== null &&
      user.yz_is_member !== queryParams.isMember
    ) {
      return false;
    }

    // 微信昵称筛选
    if (
      queryParams.wechatName &&
      !user.wechat_name.includes(queryParams.wechatName)
    ) {
      return false;
    }

    // 微信备注筛选
    if (
      queryParams.wechatRemark &&
      !user.wechat_remark.includes(queryParams.wechatRemark)
    ) {
      return false;
    }

    // 注册时间范围筛选
    if (queryParams.dateRange && queryParams.dateRange.length === 2) {
      const startDate = new Date(
        queryParams.dateRange[0] + " 00:00:00"
      ).getTime();
      const endDate = new Date(
        queryParams.dateRange[1] + " 23:59:59"
      ).getTime();
      const registerDate = new Date(user.yz_created_at).getTime();

      if (registerDate < startDate || registerDate > endDate) {
        return false;
      }
    }

    // 交易次数范围筛选
    if (
      queryParams.minTradeCount !== null &&
      user.yz_trade_count < queryParams.minTradeCount
    ) {
      return false;
    }
    if (
      queryParams.maxTradeCount !== null &&
      user.yz_trade_count > queryParams.maxTradeCount
    ) {
      return false;
    }

    // 标签筛选
    if (queryParams.tags.length > 0) {
      const userTags = getTagsArray(user.wechat_labels);
      // 检查是否有交集
      const hasMatchingTag = queryParams.tags.some(tag =>
        userTags.includes(tag)
      );
      if (!hasMatchingTag) {
        return false;
      }
    }

    return true;
  });

  // 计算总数
  pagination.total = filteredUsers.length;

  // 然后分页
  const start = (pagination.currentPage - 1) * pagination.pageSize;
  const end = start + pagination.pageSize;
  return filteredUsers.slice(start, end);
});

const loading = ref(false);

// 请求用户列表数据
const fetchUserList = async () => {
  loading.value = true;
  try {
    // 准备查询参数
    const params = {
      page: pagination.currentPage - 1, // 后端从0开始计数
      limit: pagination.pageSize,
      mobile: queryParams.mobile || undefined,
      gender: queryParams.gender ?? undefined,
      isMember: queryParams.isMember ?? undefined,
      minTradeCount: queryParams.minTradeCount ?? undefined,
      maxTradeCount: queryParams.maxTradeCount ?? undefined,
      wechatName: queryParams.wechatName || undefined,
      wechatRemark: queryParams.wechatRemark || undefined,
      startDate: queryParams.dateRange?.[0] || undefined,
      endDate: queryParams.dateRange?.[1] || undefined,
      tags: queryParams.tags.length
        ? JSON.stringify(queryParams.tags)
        : undefined
    };

    // 调用API
    const response = await getUserList(params);

    if (response.success) {
      // 使用后端返回的数据
      allUsers.value = response.data;
      pagination.total = response.total;
    } else {
      ElMessage.error("获取用户列表失败");
    }

    loading.value = false;
  } catch (error) {
    console.error("获取用户列表失败:", error);
    ElMessage.error("获取用户列表失败");
    loading.value = false;
  }
};

// 查询按钮点击事件
const handleQuery = () => {
  pagination.currentPage = 1;
  // 使用计算属性自动过滤
};

// 重置查询条件
const resetQuery = () => {
  queryParams.mobile = "";
  queryParams.gender = null;
  queryParams.isMember = null;
  queryParams.minTradeCount = null;
  queryParams.maxTradeCount = null;
  queryParams.wechatName = "";
  queryParams.wechatRemark = "";
  queryParams.dateRange = [];
  queryParams.tags = [];
  pagination.currentPage = 1;
};

// 分页大小改变
const handleSizeChange = (size: number) => {
  pagination.pageSize = size;
  // 使用计算属性自动分页
};

// 当前页改变
const handleCurrentChange = (page: number) => {
  pagination.currentPage = page;
  // 使用计算属性自动分页
};

// 查看用户详情
const handleView = (row: User) => {
  ElMessage.info(`查看用户: ${row.user_id}`);
  // 在此处实现查看逻辑或跳转到详情页
};

// 编辑用户
const handleEdit = (row: User) => {
  ElMessage.info(`编辑用户: ${row.user_id}`);
  // 在此处实现编辑逻辑或打开编辑对话框
};

// 导出用户数据
const handleExport = () => {
  ElMessageBox.confirm("确认导出所选用户数据?", "提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning"
  })
    .then(() => {
      // 实际导出代码
      // const params = { ...queryParams };
      // exportUsers(params).then(res => {
      //   const blob = new Blob([res.data]);
      //   const fileName = `用户数据_${new Date().getTime()}.xlsx`;
      //   const link = document.createElement("a");
      //   link.href = URL.createObjectURL(blob);
      //   link.download = fileName;
      //   link.click();
      //   URL.revokeObjectURL(link.href);
      // });

      ElMessage.success("导出成功");
    })
    .catch(() => {
      // 取消导出
    });
};

// 解析JSON标签数组
const getTagsArray = (tagsJson: string): string[] => {
  if (!tagsJson) return [];
  try {
    return JSON.parse(tagsJson);
  } catch (e) {
    return [];
  }
};

// 生命周期钩子
onMounted(() => {
  fetchUserList();
});
</script>

<style scoped>
.main-container {
  padding: 20px;
  height: auto;
  min-height: 100%;
  overflow-y: auto;
}

.filter-container {
  margin-bottom: 20px;
}

.mb-4 {
  margin-bottom: 16px;
}

.mx-1 {
  margin: 0 4px;
}

.mx-2 {
  margin: 0 8px;
}

.toolbar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 16px;
}

.pagination-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
  margin-bottom: 20px;
}

.flex-between {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.flex-end {
  display: flex;
  justify-content: flex-end;
}

.trade-count-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

/* 添加下面这些样式确保页面可滚动 */
:deep(.el-card__body) {
  height: auto;
  overflow: visible;
}

:deep(.el-table) {
  max-height: calc(100vh - 300px);
  overflow-y: auto;
}
</style>
