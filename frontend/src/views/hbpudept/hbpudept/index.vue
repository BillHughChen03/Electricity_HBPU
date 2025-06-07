<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="校区" prop="school">
        <el-input
          v-model="queryParams.school"
          placeholder="请输入校区"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="公寓区" prop="area">
        <el-input
          v-model="queryParams.area"
          placeholder="请输入公寓区"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="楼栋号" prop="buildingName">
        <el-input
          v-model="queryParams.buildingName"
          placeholder="请输入楼栋号"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="楼层" prop="floor">
        <el-input
          v-model="queryParams.floor"
          placeholder="请输入楼层"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="房间号" prop="roomNum">
        <el-input
          v-model="queryParams.roomNum"
          placeholder="请输入房间号"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="房间id" prop="room">
        <el-input
          v-model="queryParams.room"
          placeholder="请输入房间id"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="楼栋id" prop="building">
        <el-input
          v-model="queryParams.building"
          placeholder="请输入楼栋id"
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
          v-hasPermi="['hbpudept:hbpudept:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['hbpudept:hbpudept:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['hbpudept:hbpudept:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['hbpudept:hbpudept:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="hbpudeptList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="校区" align="center" prop="school" />
      <el-table-column label="公寓区" align="center" prop="area" />
      <el-table-column label="楼栋号" align="center" prop="buildingName" />
      <el-table-column label="楼层" align="center" prop="floor" />
      <el-table-column label="房间号" align="center" prop="roomNum" />
      <el-table-column label="房间id" align="center" prop="room" />
      <el-table-column label="楼栋id" align="center" prop="building" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['hbpudept:hbpudept:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['hbpudept:hbpudept:remove']">删除</el-button>
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

    <!-- 添加或修改寝室查询表对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="hbpudeptRef" :model="form" :rules="rules" label-width="80px">
      <el-form-item v-if="renderField(true, true)" label="校区" prop="school">
        <el-input v-model="form.school" placeholder="请输入校区" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="公寓区" prop="area">
        <el-input v-model="form.area" placeholder="请输入公寓区" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="楼栋号" prop="buildingName">
        <el-input v-model="form.buildingName" placeholder="请输入楼栋号" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="楼层" prop="floor">
        <el-input v-model="form.floor" placeholder="请输入楼层" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="房间号" prop="roomNum">
        <el-input v-model="form.roomNum" placeholder="请输入房间号" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="房间id" prop="room">
        <el-input v-model="form.room" placeholder="请输入房间id" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="楼栋id" prop="building">
        <el-input v-model="form.building" placeholder="请输入楼栋id" />
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

<script setup name="Hbpudept">
import { listHbpudept, getHbpudept, delHbpudept, addHbpudept, updateHbpudept } from "@/api/hbpudept/hbpudept";

const { proxy } = getCurrentInstance();

const hbpudeptList = ref([]);
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
    school: null,
    area: null,
    buildingName: null,
    floor: null,
    roomNum: null,
    room: null,
    building: null,
  },
  rules: {
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询寝室查询表列表 */
function getList() {
  loading.value = true;
  listHbpudept(queryParams.value).then(response => {
    hbpudeptList.value = response.rows;
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
    school: null,
    area: null,
    buildingName: null,
    floor: null,
    roomNum: null,
    room: null,
    building: null,
  };
  proxy.resetForm("hbpudeptRef");
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
  ids.value = selection.map(item => item.school);
  single.value = selection.length != 1;
  multiple.value = !selection.length;
}

/** 新增按钮操作 */
function handleAdd() {
  reset();
  open.value = true;
  title.value = "添加寝室查询表";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const _school = row.school || ids.value;
  getHbpudept(_school).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改寝室查询表";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["hbpudeptRef"].validate(valid => {
    if (valid) {
      if (form.value.school != null) {
        updateHbpudept(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addHbpudept(form.value).then(response => {
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
  const _schools = row.school || ids.value;
  proxy.$modal.confirm('是否确认删除寝室查询表编号为"' + _schools + '"的数据项？').then(function() {
    return delHbpudept(_schools);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}


/** 导出按钮操作 */
function handleExport() {
  proxy.download('hbpudept/hbpudept/export', {
    ...queryParams.value
  }, `hbpudept_${new Date().getTime()}.xlsx`);
}

/** 是否渲染字段 */
function renderField(insert, edit) {
  return form.value.school == null ? insert : edit;
}

getList();
</script>