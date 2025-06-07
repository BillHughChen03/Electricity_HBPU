<template>
  <div class="dashboard-mask" v-if="loading"></div>
  <div class="dashboard">
    <!-- 时间选择和查询按钮 -->
    <el-row justify="space-between" class="toolbar">
      <el-date-picker
          v-model="timeRange"
          type="daterange"
          start-placeholder="开始时间"
          end-placeholder="结束时间"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
      />
<!--      <el-input v-model="room" placeholder="请输入房间号" style="width: 200px" />-->
      <el-button type="primary" @click="fetchData">查询</el-button>
    </el-row>

    <!-- 主体区域 -->
    <el-row
        :gutter="20"
        class="content"
        :class="{ mobile: isMobile }"
    >
      <!-- 左侧表格区域 -->
      <el-col :xs="24" :sm="11" v-if="!isMobile">
        <div class="table-container">
          <el-table
              :data="tableData"
              style="width: 100%"
              height="100%"
              class="small-table"
              border
              @sort-change="handleSortChange"
          >
            <el-table-column
                prop="infoId"
                label="编号"
                sortable="custom"
            />
            <el-table-column prop="campus" label="校区" />
            <el-table-column prop="buildingName" label="宿舍区" />
            <el-table-column prop="roomName" label="房间号" />
            <el-table-column prop="total" label="总用电" />
            <el-table-column prop="remaining" label="剩余电量" />
            <el-table-column
                prop="finishTime"
                label="查询时间"
                :formatter="convertDateTimeFormat"
            />
          </el-table>
        </div>
      </el-col>

      <!-- 图表区域（手机端显示在上方） -->
      <el-col :xs="24" :sm="13">
        <div ref="chartRef" class="chart"></div>
      </el-col>

      <!-- 手机端下方表格 -->
      <el-col :xs="24" v-if="isMobile">
        <el-table class="small-table" :data="tableData" style="width: 100%" border>
          <el-table-column prop="infoId" label="编号" width="45px" />
          <el-table-column prop="campus" label="校区" />
          <el-table-column prop="buildingName" label="宿舍区" />
          <el-table-column prop="roomName" label="房间号" />
          <el-table-column prop="total" label="总用电" />
          <el-table-column prop="remaining" label="剩余电量" />
          <el-table-column
              prop="finishTime"
              label="查询时间"
              :formatter="convertDateTimeFormat"
          />
        </el-table>
      </el-col>
    </el-row>

    <!-- 回到顶部按钮（仅手机端显示） -->
    <el-backtop v-if="isMobile" :right="20" :bottom="60" />
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import * as echarts from 'echarts'
import { ElMessage } from 'element-plus'
import { ElMessageBox } from 'element-plus'
import { listRoomTime } from '@/api/hbpuelectricity/electricity'
import {getHbpuuser} from "@/api/hbpuuser/hbpuuser.js";
import useUserStore from "@/store/modules/user.js";

const loading = ref(true)
const userStore = useUserStore();

const timeRange = ref([])
const room = ref('')
const tableData = ref([])
const chartRef = ref(null)
let chartInstance = null
const UserInfo = ref(null);
const userId = ref('');
const isMobile = ref(window.innerWidth < 768)
const originalData = ref([]) // 原始数据，用于图表

watch(
    () => room.value,
    (newRoomValue) => {
      if (newRoomValue) {
        fetchData()
      }
    },
    { immediate: false }
)

const convertDateTimeFormat = (row, column, cellValue) => {
  if (!cellValue) return '';
  const dateTimeObj = new Date(cellValue);
  const year = dateTimeObj.getFullYear();
  const month = String(dateTimeObj.getMonth() + 1).padStart(2, '0');
  const date = String(dateTimeObj.getDate()).padStart(2, '0');
  const hours = String(dateTimeObj.getHours()).padStart(2, '0');
  const minutes = String(dateTimeObj.getMinutes()).padStart(2, '0');
  const seconds = String(dateTimeObj.getSeconds()).padStart(2, '0');

  return `${year}-${month}-${date} ${hours}:${minutes}:${seconds}`;
};

userId.value = userStore.id;

onMounted(() => {
  getHbpuuser(userId.value).then(response => {
    UserInfo.value = response.data;
    if (
        response.data.uid == null ||
        response.data.husername == null ||
        response.data.hpassword == null ||
        (response.data.room == null || response.data.room === "")
    ) {
      ElMessageBox.alert('您未绑定', '错误', {
        confirmButtonText: 'OK',
    });
      console.log("未绑定！");
      router.push('/ele/userinfo')
    }
    else {
      loading.value = false
      room.value = response.data.room;
    }
  }).catch(error => {
    console.error("获取用户信息失败:", error);
    UserInfo.value = null;
  });
});

const fetchData = async () => {
  try {
    const params = {
      room: room.value,
      startTime: timeRange.value?.[0] || undefined,
      endTime: timeRange.value?.[1] || undefined
    }

    console.log('发送请求参数:', params)

    const res = await listRoomTime(params)
    if (res.success) {
      let rawData = res.msg.list || []

      // 反转为升序：5,4,3,2,1 → 1,2,3,4,5
      const sortedData = [...rawData].reverse()

      // 保存原始数据用于图表
      originalData.value = sortedData

      // 拷贝一份给表格，避免表格排序影响原始数据
      tableData.value = JSON.parse(JSON.stringify(sortedData))

      updateChart()
    } else {
      ElMessage.error('获取数据失败')
    }
  } catch (err) {
    ElMessage.error('请求异常')
    console.error('请求异常:', err)
  }
}

const updateChart = () => {
  if (!chartInstance) {
    chartInstance = echarts.init(chartRef.value)
  }

  const chartData = originalData.value // 始终使用原始数据绘图

  const option = {
    title: {
      text: '剩余电量变化'
    },
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: chartData.map(item => item.infoId),
      axisLabel: {
        interval: 0,
      }
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '剩余电量',
        type: 'line',
        data: chartData.map(item => parseFloat(item.remaining)),
        smooth: true,
        showSymbol: true
      }
    ],
    dataZoom: [{
      type: 'slider',
      start: 0,
      end: 100,
      xAxisIndex: 0,
      filterMode: 'filter'
    }]
  }

  chartInstance.setOption(option, true)
}

const handleSortChange = ({ column, prop, order }) => {
  if (prop === 'infoId') {
    tableData.value = [...tableData.value].sort((a, b) => {
      const idA = parseInt(a.infoId)
      const idB = parseInt(b.infoId)
      if (order === 'ascending') {
        return idA - idB
      } else if (order === 'descending') {
        return idB - idA
      }
      return 0
    })
  }
}

const handleResize = () => {
  isMobile.value = window.innerWidth < 768
  chartInstance && chartInstance.resize()
}

onMounted(() => {
  fetchData()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.toolbar {
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 10px;
}

.content {
  min-height: 400px;
}

.table-container {
  height: 100%;
  overflow-y: auto;
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 10px;
}

.chart {
  width: 100%;
  height: 400px;
}

@media (max-width: 767px) {
  .table-container {
    height: auto;
    overflow: visible;
    border: none;
    padding: 0;
  }

  .chart {
    height: 300px;
  }
}

/* 缩小字体并避免内容撑开列宽 */
:deep(.el-table .el-table__cell) {
  font-size: 12px;
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
}

/* 让表格在父容器内滚动，不撑出页面 */
.table-container {
  width: 100%;
  overflow-x: auto;
}

.dashboard-mask {
  position: absolute;
  z-index: 999;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(1px);
  pointer-events: all;
}


</style>
