<template>
  <div id="main">
    <!-- 一卡通绑定卡片 -->
    <el-card class="mb-4">
      <template #header>
        <div class="card-header">一卡通绑定</div>
      </template>
      <el-form :model="cardForm" label-width="100px">
        <div class="info">
          <p >当前登录的账户：{{ userName }}，ID：{{ userId }}</p>
        </div>
          <div class="ecardform">
            <el-form-item label="一卡通账号">
              <el-input v-model="cardForm.ecardUsername" placeholder="请输入一卡通账号"></el-input>
            </el-form-item>
            <el-form-item label="一卡通密码">
              <el-input v-model="cardForm.ecardPassword" placeholder="请输入一卡通密码" show-password></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="verifyCard">验证</el-button>
              <el-button type="success" @click="CardSave" :disabled="!accountVerified">绑定</el-button>
            </el-form-item>
          </div>
        <el-alert v-if="cardStatus" :title="cardStatus" :type="cardVerified ? 'success' : 'error'" show-icon />
      </el-form>
    </el-card>

    <!-- 动态联动选择卡片 -->
    <div class="room" :class="{ 'is-disabled': !cardVerified }">
      <el-card class="mb-4">
        <template #header>
          <div class="card-header">寝室绑定</div>
        </template>
        <el-form :model="query" label-width="80px">
          <el-form-item label="校区">
            <el-select v-model="query.school" placeholder="选择校区" @change="onSchoolChange">
              <el-option v-for="item in options.schools" :key="item" :label="item" :value="item" />
            </el-select>
          </el-form-item>
          <el-form-item label="公寓区">
            <el-select v-model="query.area" placeholder="选择公寓区" @change="onAreaChange">
              <el-option v-for="item in options.areas" :key="item" :label="item" :value="item" />
            </el-select>
          </el-form-item>
          <el-form-item label="楼栋">
            <el-select v-model="query.building_name" placeholder="选择楼栋" @change="onBuildingChange">
              <el-option v-for="item in options.buildings" :key="item" :label="item" :value="item" />
            </el-select>
          </el-form-item>
          <el-form-item label="楼层">
            <el-select v-model="query.floor" placeholder="选择楼层" @change="onFloorChange">
              <el-option v-for="item in options.floors" :key="item" :label="item" :value="item" />
            </el-select>
          </el-form-item>
          <el-form-item label="房间号">
            <el-select v-model="query.room_num" placeholder="选择房间号" @change="onRoomChange">
              <el-option v-for="item in options.rooms" :key="item" :label="item" :value="item" />
            </el-select>
          </el-form-item>
        </el-form>
        <div class="bottons">
          <div v-if="!queryDetail">
            <p class="choiceRoom">{{ displayRoom1 }}</p>
            <p class="choiceRoom">详细信息：{{ displayRoom2 }}</p>
            <div v-if="fee" class="fee">
              <h4>查询结果：</h4>
              <p>校区：{{ feefrom.campus }}</p>
              <p>楼宇名称：{{ feefrom.building_name }}</p>
              <p>房间名称：{{ feefrom.room_name }}</p>
              <p>总电量：{{ feefrom.total_electricity }}</p>
              <p>剩余电量：{{ feefrom.remaining_electricity }}</p>
              <p>更新时间：{{ feefrom.finish_time }}</p>
              <p>此处查询不存入数据库。</p>
            </div>
            <el-button v-if="query2button" type="primary" @click="queryfee2">查询</el-button>
          </div>
          <div v-if="queryDetail">
            <p class="choiceRoom">已选择：{{ displayRoom }}</p>
            <div v-if="fee" class="fee">
              <h4>查询结果：</h4>
              <p>校区：{{ feefrom.campus }}</p>
              <p>楼宇名称：{{ feefrom.building_name }}</p>
              <p>房间名称：{{ feefrom.room_name }}</p>
              <p>总电量：{{ feefrom.total_electricity }}</p>
              <p>剩余电量：{{ feefrom.remaining_electricity }}</p>
              <p>更新时间：{{ feefrom.finish_time }}</p>
              <p>此处查询不存入数据库。</p>
            </div>
            <el-button type="primary" @click="bindRoom">绑定</el-button>
            <el-button type="primary" @click="queryfee">查询</el-button>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 原有通知配置部分 -->
    <div class="notification-section" :class="{ 'is-disabled': !cardVerified }">
      <el-card class="mb-4">
        <template #header>
          <div class="card-header">通知配置</div>
        </template>
        <el-tabs type="border-card">
          <el-tab-pane label="邮箱配置">
            <div class="tab-content-container" >
              <el-form ref="emailForm" :model="emailData" label-width="100px" class="centered-form" disabled>
                <p> 还没有接入邮箱系统，懒得写了有心情再说吧。</p>
                <el-form-item label="邮箱">
                  <el-input v-model="emailData.email" placeholder="邮箱地址" disabled></el-input>
                </el-form-item>
                <el-form-item label="验证码">
                  <el-input v-model="emailData.verificationCode" placeholder="请输入验证码" disabled></el-input>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="verifyEmail" :disabled="emailVerified">认证邮箱</el-button>
                </el-form-item>
              </el-form>
            </div>
          </el-tab-pane>
          <el-tab-pane label="微信推送">
            <div class="tab-content-container">
              <el-form ref="wechatForm" :model="wechatData" label-width="100px" class="centered-form">
                <el-form-item label="SendKey">
                  <el-input v-model="wechatData.sendKey" :placeholder="PushKey.value"></el-input>
                </el-form-item>
                <el-button type="success" @click="saveSendKey">保存</el-button>
                <el-button @click="SendTest">测试</el-button>
                <el-button @click="getKey">点击此处获得key</el-button>
              </el-form>
            </div>
          </el-tab-pane>
          <el-tab-pane label="推送配置">
            <div class="tab-content-container">
              <el-form ref="notificationForm" :model="notificationData" label-width="100px" class="centered-form">
                <el-form-item label="通知方式">
<!--                  <el-checkbox-group v-model="notificationData.methods">-->
<!--                    <el-checkbox label="邮箱" value="email" disabled></el-checkbox>-->
<!--                    <el-checkbox label="微信推送" value="wechat"></el-checkbox>-->
<!--                  </el-checkbox-group>-->
                  <el-checkbox label="邮箱" v-model="email" disabled></el-checkbox>
                  <el-checkbox label="微信推送" v-model="wechat"></el-checkbox>
                </el-form-item>
                <el-form-item label="每天推送时间">
<!--                  <el-time-select-->
<!--                      v-model="notificationData.time"-->
<!--                      :picker-options="timePickerOptions"-->
<!--                      placeholder="选择时间"-->
<!--                  ></el-time-select>-->
                  每天8:00自动依次开始。
                </el-form-item>
                <el-form-item>
                  <el-button type="success" @click="saveNotificationWays">保存</el-button>
                </el-form-item>
              </el-form>
            </div>
          </el-tab-pane>
        </el-tabs>
      </el-card>
    </div>
  </div>
  <el-backtop v-if="isMobile" :right="20" :bottom="60" />
</template>

<script setup>
import { ref, reactive, watch, computed,onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import useUserStore from "@/store/modules/user.js";
const cardForm = reactive({ ecardUsername: '', ecardPassword: '' })
const accountVerified = ref(false)
import { ElLoading } from 'element-plus'
const cardVerified = ref(false)
const cardStatus = ref('')
const isMobile = ref(window.innerWidth < 768)
import {
  getHbpuuser,
  ecardVerify,
  ecardSave,
  updateUserRoomInfo,
  getRoomfee,
  savesendkey,
  saveways, sendtest
} from "@/api/hbpuuser/hbpuuser.js";
import {cascadeOptions, loadcurrentroom} from "@/api/hbpudept/hbpudept.js";
const displayRoom1 =ref();
const userStore = useUserStore();
const userName = ref('');
const userId = ref('');
let fee = ref(false);
const PushKey = ref('')
const UserInfo = ref(null);
const wechat = ref(false);
const email = ref(false);
// 通知设置数据
const emailData = reactive({ email: '', verificationCode: '' })
// 初始化用户信息
userName.value = userStore.name;
userId.value = userStore.id;
emailData.email = userStore.email;
const detailedDept = ref(null)
const queryDetail = ref(null)
const displayRoom2 = ref('')
let displayRoom = computed(() => {
  if (!queryDetail.value || !detailedDept.value) return "还未绑定寝室！"
  const d = detailedDept.value
  return `${d.school} - ${d.area}${d.building_name}号楼 - ${d.floor}楼 - ${d.room_num}室 | 楼编：${d.building} 房编：${d.room}`
})

console.log("当前登录的账户是:", userName.value, " ID是:", userId.value);

const cardFormSave = reactive({ ecardUsername: '', ecardPassword: '', uid:'' })

const buildforfee2 = ref('')
const roomforfee2 = ref('')
const query2button = ref(false)

const showFullScreenLoading = () => {
  return ElLoading.service({
    fullscreen: true,
    text: '数据加载中，请稍候...',
    spinner: 'el-icon-loading',
    background: 'rgba(0, 0, 0, 0.7)',
  })
}


onMounted(() => {
  getHbpuuser(userId.value).then(response => {
    UserInfo.value = response.data;
    if(response.data.uid === null || response.data.husername === null || response.data.hpassword === null) {
      PushKey.value = "未绑定ID";
      console.log("未绑定！");
    }
    else {
      cardForm.ecardUsername = response.data.husername;
      cardForm.ecardPassword = response.data.hpassword;
      wechatData.sendKey = response.data.sendky;
      if (response.data.pushkey === null){
        PushKey.value = "未输入PushKey！"
      }
      cardFormSave.ecardPassword = cardForm.ecardPassword;
      cardFormSave.ecardUsername = cardForm.ecardUsername;
      cardVerified.value = true;
      const { ymdHms } = convertDateTimeFormat(response.data.tokenTime);
      // 更新 cardStatus 的值
      cardStatus.value = `已绑定！上次获取token时间为：${ymdHms}，请自己确保时间是否有效。`;
    }

    if(response.data.room != null && response.data.building != null){
      // console.log(response.data.room)
      // console.log(response.data.building)
      displayRoom1.value = `已绑定寝室 —— 楼编：${response.data.building} 房编：${response.data.room}`
      buildforfee2.value =  response.data.building;
      roomforfee2.value = response.data.room;
      query2button.value = true;
      loadcurrentroom(response.data.room).then(res => {
        let d = res.data;
        // `${d.school} - ${d.area}${d.building_name}号楼 - ${d.floor}楼 - ${d.room_num}室 `
        displayRoom2.value = `${d.school} - ${d.area}${d.buildingName}号楼 - ${d.floor}楼 - ${d.roomNum}室`

      });
    }

    if(response.data.pushkey !== null){
      if(response.data.pushkey === "3"){
        wechat.value = true;
        email.value = true;
      }
      if(response.data.pushkey === "2"){
        wechat.value = true;
        email.value =  false;
      }
      if(response.data.pushkey === "1"){
        wechat.value = false;
        email.value = true;
      }
      if(response.data.pushkey === "0"){
        wechat.value = false;
        email.value = false;
      }
    }
  }).catch(error => {
    console.error("获取用户信息失败:", error);
    UserInfo.value = null;
  });
});

const getKey =() =>{
  window.open('https://sct.ftqq.com/sendkey', '_blank')
}

// 转换 tokenTime 为友好的格式（修复时区问题）
const convertDateTimeFormat = (dateTimeStr) => {
  const dateTimeObj = new Date(dateTimeStr);

  // 使用东八区时间格式化为 YYYY-MM-DD HH:mm:ss
  const year = dateTimeObj.getFullYear();
  const month = String(dateTimeObj.getMonth() + 1).padStart(2, '0');
  const date = String(dateTimeObj.getDate()).padStart(2, '0');
  const hours = String(dateTimeObj.getHours()).padStart(2, '0');
  const minutes = String(dateTimeObj.getMinutes()).padStart(2, '0');
  const seconds = String(dateTimeObj.getSeconds()).padStart(2, '0');

  const ymdHms = `${year}-${month}-${date} ${hours}:${minutes}:${seconds}`;

  // 原本的本地格式也保留
  const localFormat = `${year}年${month}月${date}日 ${hours}时${minutes}分${seconds}秒`;

  return {
    ymdHms,
    localFormat
  };
};

const query = reactive({
  school: '',
  area: '',
  building_name: '',
  floor: '',
  room_num: ''
})

const feefrom = reactive({
  total_electricity: '',
  remaining_electricity: '',
  building_name: '',
  room_name: '',
  finish_time: '',
  campus: ''
})

const options = reactive({
  schools: [],
  areas: [],
  buildings: [],
  floors: [],
  rooms: []
})
// 页面加载时拿所有校区（无参数调用接口）
async function loadSchools() {
  const res = await cascadeOptions()
  options.schools = Array.isArray(res) ? res : []
}
function resetOptions(level) {
  switch(level) {
    case 'school':
      query.area = ''
      query.building_name = ''
      query.floor = ''
      query.room_num = ''
      options.areas = []
      options.buildings = []
      options.floors = []
      options.rooms = []
      detailedDept.value = null
      queryDetail.value = false
      break;
    case 'area':
      query.building_name = ''
      query.floor = ''
      query.room_num = ''
      options.buildings = []
      options.floors = []
      options.rooms = []
      detailedDept.value = null
      queryDetail.value = false
      break;
    case 'building_name':
      query.floor = ''
      query.room_num = ''
      options.floors = []
      options.rooms = []
      detailedDept.value = null
      queryDetail.value = false
      break;
    case 'floor':
      query.room_num = ''
      options.rooms = []
      detailedDept.value = null
      queryDetail.value = false
      break;
    case 'room_num':
      detailedDept.value = null
      queryDetail.value = false
      break;
  }
}

// 校区变化
async function onSchoolChange() {
  resetOptions('school')
  if (!query.school) {
    options.areas = []
    return
  }
  const res = await cascadeOptions({ school: query.school })
  options.areas = Array.isArray(res) ? res : []
}

// 公寓区变化
async function onAreaChange() {
  resetOptions('area')
  if (!query.school || !query.area) {
    options.buildings = []
    return
  }
  const res = await cascadeOptions({ school: query.school, area: query.area })
  options.buildings = Array.isArray(res) ? res : []
}

// 楼栋变化
async function onBuildingChange() {
  resetOptions('building_name')
  if (!query.school || !query.area || !query.building_name) {
    options.floors = []
    return
  }
  const res = await cascadeOptions({ school: query.school, area: query.area, building_name: query.building_name })
  options.floors = Array.isArray(res) ? res : []
}

// 楼层变化
async function onFloorChange() {
  resetOptions('floor')
  if (!query.school || !query.area || !query.building_name || !query.floor) {
    options.rooms = []
    return
  }
  const res = await cascadeOptions({ school: query.school, area: query.area, building_name: query.building_name, floor: query.floor })
  options.rooms = Array.isArray(res) ? res : []
}

// 房间号变化，调用接口拿详细信息（接口返回对象）
async function onRoomChange() {
  resetOptions('room_num')
  if (!query.school || !query.area || !query.building_name || !query.floor || !query.room_num) {
    queryDetail.value = false
    detailedDept.value = null
    return
  }
  const res = await cascadeOptions({ ...query })
  if (res && res.Dept) {
    detailedDept.value = res.Dept
    queryDetail.value = true
    displayRoom.value = `${res.Dept.school} / ${res.Dept.area} / ${res.Dept.building_name} / ${res.Dept.floor} / ${res.Dept.room_num}`
  } else {
    queryDetail.value = false
    detailedDept.value = null
  }
}

// 详细房间信息（当选到最后一级接口返回对象时存放）


const fetchOptions = async (level) => {
  const res = await getCascadeOptionsApi({ level, ...query })
  if (res.code === 200) {
    options[level + 's'] = res.data || []
  }
}

const wechatData = reactive({ sendKey: '' })
const notificationData = reactive({ methods: [], time: '' })
const emailVerified = ref(false)
const timePickerOptions = {
  start: '06:00',
  end: '23:00',
  step: '00:30'
}

const verifyEmail = () => {
  ElMessage.success('说了还没写，别点。')
  emailVerified.value = true
}

// 初始化加载校区
fetchOptions('school')

// 验证一卡通账号
const verifyCard = async () => {
  const loading = showFullScreenLoading()
  try {
    const res = await ecardVerify(cardForm)
    if (res.status_code === 200 && res.data) {
      cardVerified.value = true
      cardStatus.value = '验证成功' + ' 姓名：' + res.data.name + ' 学号:' + res.data.sno
      accountVerified.value = true
      ElMessage.success('一卡通验证成功')
    } else {
      cardVerified.value = false
      cardStatus.value = '验证失败，请检查账号密码'
      ElMessage.error('一卡通验证失败')
    }
  } finally {
    loading.close()
  }
}

// 绑定一卡通
const CardSave = async () => {
  const loading = showFullScreenLoading()
  try {
    cardFormSave.uid = userId.value
    cardFormSave.ecardPassword = cardForm.ecardPassword
    cardFormSave.ecardUsername = cardForm.ecardUsername
    const res = await ecardSave(cardFormSave)
    if (res.code === 200) {
      ElMessage.success('绑定成功')
    } else {
      ElMessage.error(res.msg || '绑定失败')
    }
  } finally {
    loading.close()
  }
}
// 页面加载调用
loadSchools()

const bindRoom = async () => {
  const loading = showFullScreenLoading()
  try {
    let building = detailedDept.value.building
    let room = detailedDept.value.room
    let uid = userStore.id
    if (!uid || !building || !room) {
      ElMessage.warning('请先选择完整的寝室信息')
      return
    }
    const res = await updateUserRoomInfo({ uid, building, room })
    if (res.code === 200) {
      ElMessage.success('寝室信息绑定成功')
      window.location.reload()
    } else {
      ElMessage.error(res.message || '绑定失败')
    }
  } finally {
    loading.close()
  }
}

const loading = ref(false)
const showFeeResult = ref(false)

const queryfee = async () => {
  const loading = showFullScreenLoading()
  try {
    const { building, room } = detailedDept.value
    const uid = userStore.id
    const res = await getRoomfee({ uid, building, room })
    if (res.code === 200) {
      ElMessage.success('查询成功！')
      feefrom.total_electricity = res.data.total_electricity
      feefrom.remaining_electricity = res.data.remaining_electricity
      feefrom.building_name = res.data.building_name
      feefrom.room_name = res.data.room_name
      feefrom.finish_time = res.data.finish_time
      feefrom.campus = res.data.campus
      showFeeResult.value = true
      fee.value = true
    } else {
      ElMessage.error(res.message || '查询失败！')
    }
  } catch (error) {
    ElMessage.error('网络异常，请稍后再试')
  } finally {
    loading.close()
  }
}
const queryfee2 = async () => {
  const loading = showFullScreenLoading()
  try {
    let building = buildforfee2.value
    let room = roomforfee2.value
    const uid = userStore.id
    const res = await getRoomfee({ uid, building, room })
    if (res.code === 200) {
      ElMessage.success('查询成功！')
      feefrom.total_electricity = res.data.total_electricity
      feefrom.remaining_electricity = res.data.remaining_electricity
      feefrom.building_name = res.data.building_name
      feefrom.room_name = res.data.room_name
      feefrom.finish_time = res.data.finish_time
      feefrom.campus = res.data.campus
      showFeeResult.value = true
      fee.value = true
      queryDetail.value = false
    } else {
      ElMessage.error(res.message || '查询失败！')
    }
  } catch (error) {
    ElMessage.error('网络异常，请稍后再试')
  } finally {
    loading.close()
  }
}

const saveSendKey = async () =>{
  try{
    let uid = userId.value;
    let sendkey = wechatData.sendKey
    const res = await savesendkey({uid, sendkey})
    if(res.code === 200){
      ElMessage.success('保存成功！')
    }
    else {
      ElMessage.error(res.message || '更新失败!')
    }
  }catch (error) {
    ElMessage.error('异常！'+error)
  }
}

const saveNotificationWays = async () =>{
  try{
    let uid = userId.value;
    let pushkey = "";
    if(wechat.value === false && email.value === false) pushkey = "0";
    if(wechat.value === false && email.value === true) pushkey = "1";
    if(wechat.value === true && email.value === false) pushkey = "2";
    if(wechat.value === true && email.value === true) pushkey = "3";
    const res = await saveways({uid, pushkey})
    if(res.code === 200){
      ElMessage.success('保存成功！')
    }
    else {
      ElMessage.error(res.message || '更新失败!')
    }
  }catch (error) {
    ElMessage.error('异常！'+error)
  }
}

const SendTest = async () => {
  const loading = showFullScreenLoading()
  try {
    let sendky = wechatData.sendKey
    const res = await sendtest({ sendky })
    if (res.code === 200) {
      ElMessage.success('发送成功！')
      if (res.msg.code === 40001) {
        ElMessage.error("发送失败！" + res.msg.message)
      } else if (res.msg.code === 0) {
        ElMessage.success('推送成功！推送ID是：' + res.msg.data.pushid)
      }
    } else {
      ElMessage.error(res.message || '发送失败!')
    }
  } catch (error) {
    ElMessage.error('异常！' + error)
  } finally {
    loading.close()
  }
}

</script>

<style scoped>
.mb-4 {
  margin-bottom: 1rem;
}
.is-disabled {
  pointer-events: none;
  opacity: 0.5;
}
#main {
  max-width: 90vh;       /* 最大宽度 */
  width: 100%;            /* 宽度自适应父容器或屏幕 */
  margin: 10px auto;         /* 左右居中 */
  padding: 0 16px;        /* 水平内边距，防止内容紧贴屏幕边缘 */
  box-sizing: border-box; /* 包含padding在宽度内 */
}

.tab-content-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%; /* 确保容器高度占满整个tab内容区域 */
  padding: 20px; /* 可选：添加一些内边距 */
}

.centered-form {
  width: 100%; /* 表单宽度占满容器 */
  max-width: 600px; /* 设置最大宽度，避免表单过宽 */
  margin: 0 auto; /* 水平居中 */
}

.centered-form .el-form-item {
  margin-bottom: 20px; /* 增加表单项之间的间距 */
}

.info{
  margin-left: 20px;
}
.ecardform{
  margin-top: 5px;
}
.choiceRoom{
  margin-top: 20px;
}

.bottons{
  margin-left: 20px;
}

/* 可选，手机端字体、间距等微调 */
@media (max-width: 480px) {
  #main {
    padding: 0 12px;
  }
}

</style>
