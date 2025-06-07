<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="湖北理工username" prop="husername">
        <el-input
          v-model="queryParams.husername"
          placeholder="请输入湖北理工username"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="湖北理工password" prop="hpassword">
        <el-input
          v-model="queryParams.hpassword"
          placeholder="请输入湖北理工password"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="湖北理工access_token" prop="accessToken">
        <el-input
          v-model="queryParams.accessToken"
          placeholder="请输入湖北理工access_token"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="湖北理工refresh_token" prop="refreshToken">
        <el-input
          v-model="queryParams.refreshToken"
          placeholder="请输入湖北理工refresh_token"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="获取token的时间" prop="tokenTime">
        <el-date-picker
          v-model="queryParams.tokenTime"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择获取token的时间"
          clearable
          style="width: 240px"
        />
      </el-form-item>
      <el-form-item label="Token Type" prop="tokenType">
        <el-select v-model="queryParams.tokenType" placeholder="请选择Token Type" clearable style="width: 240px">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item label="SNO学号" prop="sno">
        <el-input
          v-model="queryParams.sno"
          placeholder="请输入SNO学号"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="姓名" prop="name">
        <el-input
          v-model="queryParams.name"
          placeholder="请输入姓名"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="楼栋号" prop="building">
        <el-input
          v-model="queryParams.building"
          placeholder="请输入楼栋号"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="房间号" prop="room">
        <el-input
          v-model="queryParams.room"
          placeholder="请输入房间号"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="微信推送send_key" prop="sendky">
        <el-input
          v-model="queryParams.sendky"
          placeholder="请输入微信推送send_key"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="邮件推送" prop="email">
        <el-input
          v-model="queryParams.email"
          placeholder="请输入邮件推送"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="邮箱认证" prop="accessEmail">
        <el-input
          v-model="queryParams.accessEmail"
          placeholder="请输入邮箱认证"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="推送时间" prop="psuhTime">
        <el-date-picker
          v-model="queryParams.psuhTime"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择推送时间"
          clearable
          style="width: 240px"
        />
      </el-form-item>
      <el-form-item label="微信推送Key" prop="pushkey">
        <el-input
          v-model="queryParams.pushkey"
          placeholder="请输入微信推送Key"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
          type="primary"
          plain
          icon="Plus"
          @click="handleAdd"
          v-hasPermi="['hbpuuser:hbpuuser:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['hbpuuser:hbpuuser:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['hbpuuser:hbpuuser:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['hbpuuser:hbpuuser:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="hbpuuserList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="用户id" align="center" prop="uid" />
      <el-table-column label="湖北理工username" align="center" prop="husername" />
      <el-table-column label="湖北理工password" align="center" prop="hpassword" />
      <el-table-column label="湖北理工access_token" align="center" prop="accessToken" />
      <el-table-column label="湖北理工refresh_token" align="center" prop="refreshToken" />
      <el-table-column label="获取token的时间" align="center" prop="tokenTime" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.tokenTime, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Token Type" align="center" prop="tokenType" />
      <el-table-column label="SNO学号" align="center" prop="sno" />
      <el-table-column label="姓名" align="center" prop="name" />
      <el-table-column label="楼栋号" align="center" prop="building" />
      <el-table-column label="房间号" align="center" prop="room" />
      <el-table-column label="微信推送send_key" align="center" prop="sendky" />
      <el-table-column label="邮件推送" align="center" prop="email" />
      <el-table-column label="邮箱认证" align="center" prop="accessEmail" />
      <el-table-column label="推送时间" align="center" prop="psuhTime" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.psuhTime, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="微信推送Key" align="center" prop="pushkey" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['hbpuuser:hbpuuser:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['hbpuuser:hbpuuser:remove']">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-show="total>0"
      :total="total"
      v-model:page="queryParams.pageNum"
      v-model:limit="queryParams.pageSize"
      @pagination="getList"
    />

    <!-- 添加或修改湖北理工用户对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="hbpuuserRef" :model="form" :rules="rules" label-width="80px">
      <el-form-item v-if="renderField(true, true)" label="湖北理工username" prop="husername">
        <el-input v-model="form.husername" placeholder="请输入湖北理工username" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="湖北理工password" prop="hpassword">
        <el-input v-model="form.hpassword" placeholder="请输入湖北理工password" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="湖北理工access_token" prop="accessToken">
        <el-input v-model="form.accessToken" placeholder="请输入湖北理工access_token" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="湖北理工refresh_token" prop="refreshToken">
        <el-input v-model="form.refreshToken" placeholder="请输入湖北理工refresh_token" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="获取token的时间" prop="tokenTime">
        <el-date-picker clearable
          v-model="form.tokenTime"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择获取token的时间">
        </el-date-picker>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="Token Type" prop="tokenType">
        <el-select v-model="form.tokenType" placeholder="请选择Token Type">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="SNO学号" prop="sno">
        <el-input v-model="form.sno" placeholder="请输入SNO学号" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="姓名" prop="name">
        <el-input v-model="form.name" placeholder="请输入姓名" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="楼栋号" prop="building">
        <el-input v-model="form.building" placeholder="请输入楼栋号" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="房间号" prop="room">
        <el-input v-model="form.room" placeholder="请输入房间号" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="微信推送send_key" prop="sendky">
        <el-input v-model="form.sendky" placeholder="请输入微信推送send_key" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="邮件推送" prop="email">
        <el-input v-model="form.email" placeholder="请输入邮件推送" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="邮箱认证" prop="accessEmail">
        <el-input v-model="form.accessEmail" placeholder="请输入邮箱认证" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="推送时间" prop="psuhTime">
        <el-date-picker clearable
          v-model="form.psuhTime"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择推送时间">
        </el-date-picker>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="微信推送Key" prop="pushkey">
        <el-input v-model="form.pushkey" placeholder="请输入微信推送Key" />
      </el-form-item>

      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="submitForm">确 定</el-button>
          <el-button @click="cancel">取 消</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="Hbpuuser">
import { listHbpuuser, getHbpuuser, delHbpuuser, addHbpuuser, updateHbpuuser } from "@/api/hbpuuser/hbpuuser";

const { proxy } = getCurrentInstance();

const hbpuuserList = ref([]);
const open = ref(false);
const loading = ref(true);
const showSearch = ref(true);
const ids = ref([]);
const single = ref(true);
const multiple = ref(true);
const total = ref(0);
const title = ref("");

const data = reactive({
  form: {},
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    husername: null,
    hpassword: null,
    accessToken: null,
    refreshToken: null,
    tokenTime: null,
    tokenType: null,
    sno: null,
    name: null,
    building: null,
    room: null,
    sendky: null,
    email: null,
    accessEmail: null,
    psuhTime: null,
    pushkey: null,
  },
  rules: {
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询湖北理工用户列表 */
function getList() {
  loading.value = true;
  listHbpuuser(queryParams.value).then(response => {
    hbpuuserList.value = response.rows;
    total.value = response.total;
    loading.value = false;
  });
}

/** 取消按钮 */
function cancel() {
  open.value = false;
  reset();
}

/** 表单重置 */
function reset() {
  form.value = {
    uid: null,
    husername: null,
    hpassword: null,
    accessToken: null,
    refreshToken: null,
    tokenTime: null,
    tokenType: null,
    sno: null,
    name: null,
    building: null,
    room: null,
    sendky: null,
    email: null,
    accessEmail: null,
    psuhTime: null,
    pushkey: null,
  };
  proxy.resetForm("hbpuuserRef");
}

/** 搜索按钮操作 */
function handleQuery() {
  queryParams.value.pageNum = 1;
  getList();
}

/** 重置按钮操作 */
function resetQuery() {
  proxy.resetForm("queryRef");
  handleQuery();
}

/** 多选框选中数据  */
function handleSelectionChange(selection) {
  ids.value = selection.map(item => item.uid);
  single.value = selection.length != 1;
  multiple.value = !selection.length;
}

/** 新增按钮操作 */
function handleAdd() {
  reset();
  open.value = true;
  title.value = "添加湖北理工用户";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const _uid = row.uid || ids.value;
  getHbpuuser(_uid).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改湖北理工用户";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["hbpuuserRef"].validate(valid => {
    if (valid) {
      if (form.value.uid != null) {
        updateHbpuuser(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addHbpuuser(form.value).then(response => {
          proxy.$modal.msgSuccess("新增成功");
          open.value = false;
          getList();
        });
      }
    }
  });
}

/** 删除按钮操作 */
function handleDelete(row) {
  const _uids = row.uid || ids.value;
  proxy.$modal.confirm('是否确认删除湖北理工用户编号为"' + _uids + '"的数据项？').then(function() {
    return delHbpuuser(_uids);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}


/** 导出按钮操作 */
function handleExport() {
  proxy.download('hbpuuser/hbpuuser/export', {
    ...queryParams.value
  }, `hbpuuser_${new Date().getTime()}.xlsx`);
}

/** 是否渲染字段 */
function renderField(insert, edit) {
  return form.value.uid == null ? insert : edit;
}

getList();
</script>