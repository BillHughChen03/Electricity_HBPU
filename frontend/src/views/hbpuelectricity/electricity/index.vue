<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="数据编号" prop="infoId">
        <el-input
          v-model="queryParams.infoId"
          placeholder="请输入数据编号"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="总用电" prop="total">
        <el-input
          v-model="queryParams.total"
          placeholder="请输入总用电"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="剩余电量" prop="remaining">
        <el-input
          v-model="queryParams.remaining"
          placeholder="请输入剩余电量"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="校区" prop="campus">
        <el-input
          v-model="queryParams.campus"
          placeholder="请输入校区"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="宿舍区" prop="buildingName">
        <el-input
          v-model="queryParams.buildingName"
          placeholder="请输入宿舍区"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="房间号" prop="roomName">
        <el-input
          v-model="queryParams.roomName"
          placeholder="请输入房间号"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="宿舍楼编号" prop="building">
        <el-input
          v-model="queryParams.building"
          placeholder="请输入宿舍楼编号"
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
      <el-form-item label="完成时间" prop="finishTime">
        <el-date-picker
          v-model="queryParams.finishTime"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择完成时间"
          clearable
          style="width: 240px"
        />
      </el-form-item>
      <el-form-item label="昨日剩余电量" prop="yesterdayRemaining">
        <el-input
          v-model="queryParams.yesterdayRemaining"
          placeholder="请输入昨日剩余电量"
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
          v-hasPermi="['hbpuelectricity:electricity:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['hbpuelectricity:electricity:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['hbpuelectricity:electricity:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['hbpuelectricity:electricity:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="electricityList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="数据编号" align="center" prop="infoId" />
      <el-table-column label="总用电" align="center" prop="total" />
      <el-table-column label="剩余电量" align="center" prop="remaining" />
      <el-table-column label="校区" align="center" prop="campus" />
      <el-table-column label="宿舍区" align="center" prop="buildingName" />
      <el-table-column label="房间号" align="center" prop="roomName" />
      <el-table-column label="宿舍楼编号" align="center" prop="building" />
      <el-table-column label="房间号" align="center" prop="room" />
      <el-table-column label="完成时间" align="center" prop="finishTime" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.finishTime, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="昨日剩余电量" align="center" prop="yesterdayRemaining" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['hbpuelectricity:electricity:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['hbpuelectricity:electricity:remove']">删除</el-button>
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

    <!-- 添加或修改电力对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="electricityRef" :model="form" :rules="rules" label-width="80px">
      <el-form-item v-if="renderField(true, true)" label="总用电" prop="total">
        <el-input v-model="form.total" placeholder="请输入总用电" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="剩余电量" prop="remaining">
        <el-input v-model="form.remaining" placeholder="请输入剩余电量" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="校区" prop="campus">
        <el-input v-model="form.campus" placeholder="请输入校区" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="宿舍区" prop="buildingName">
        <el-input v-model="form.buildingName" placeholder="请输入宿舍区" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="房间号" prop="roomName">
        <el-input v-model="form.roomName" placeholder="请输入房间号" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="宿舍楼编号" prop="building">
        <el-input v-model="form.building" placeholder="请输入宿舍楼编号" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="房间号" prop="room">
        <el-input v-model="form.room" placeholder="请输入房间号" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="完成时间" prop="finishTime">
        <el-date-picker clearable
          v-model="form.finishTime"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择完成时间">
        </el-date-picker>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="昨日剩余电量" prop="yesterdayRemaining">
        <el-input v-model="form.yesterdayRemaining" placeholder="请输入昨日剩余电量" />
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

<script setup name="Electricity">
import { listElectricity, getElectricity, delElectricity, addElectricity, updateElectricity } from "@/api/hbpuelectricity/electricity";

const { proxy } = getCurrentInstance();

const electricityList = ref([]);
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
    infoId: null,
    total: null,
    remaining: null,
    campus: null,
    buildingName: null,
    roomName: null,
    building: null,
    room: null,
    finishTime: null,
    yesterdayRemaining: null,
  },
  rules: {
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询电力列表 */
function getList() {
  loading.value = true;
  listElectricity(queryParams.value).then(response => {
    electricityList.value = response.rows;
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
    infoId: null,
    total: null,
    remaining: null,
    campus: null,
    buildingName: null,
    roomName: null,
    building: null,
    room: null,
    finishTime: null,
    yesterdayRemaining: null,
  };
  proxy.resetForm("electricityRef");
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
  ids.value = selection.map(item => item.infoId);
  single.value = selection.length != 1;
  multiple.value = !selection.length;
}

/** 新增按钮操作 */
function handleAdd() {
  reset();
  open.value = true;
  title.value = "添加电力";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const _infoId = row.infoId || ids.value;
  getElectricity(_infoId).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改电力";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["electricityRef"].validate(valid => {
    if (valid) {
      if (form.value.infoId != null) {
        updateElectricity(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addElectricity(form.value).then(response => {
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
  const _infoIds = row.infoId || ids.value;
  proxy.$modal.confirm('是否确认删除电力编号为"' + _infoIds + '"的数据项？').then(function() {
    return delElectricity(_infoIds);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}


/** 导出按钮操作 */
function handleExport() {
  proxy.download('hbpuelectricity/electricity/export', {
    ...queryParams.value
  }, `electricity_${new Date().getTime()}.xlsx`);
}

/** 是否渲染字段 */
function renderField(insert, edit) {
  return form.value.infoId == null ? insert : edit;
}

getList();
</script>