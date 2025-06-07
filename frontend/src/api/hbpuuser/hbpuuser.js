import request from '@/utils/request'

// 查询湖北理工用户列表
export function listHbpuuser(query) {
  return request({
    url: '/hbpuuser/hbpuuser/list',
    method: 'get',
    params: query
  })
}

// 查询湖北理工用户详细
export function getHbpuuser(uid) {
  return request({
    url: '/hbpuuser/hbpuuser/' + uid,
    method: 'get'
  })
}

// 新增湖北理工用户
export function addHbpuuser(data) {
  return request({
    url: '/hbpuuser/hbpuuser',
    method: 'post',
    data: data
  })
}

// 修改湖北理工用户
export function updateHbpuuser(data) {
  return request({
    url: '/hbpuuser/hbpuuser',
    method: 'put',
    data: data
  })
}

// 删除湖北理工用户
export function delHbpuuser(uid) {
  return request({
    url: '/hbpuuser/hbpuuser/' + uid,
    method: 'delete'
  })
}

// 湖北理工用户登录验证
export function ecardVerify(data) {
  return request({
    url: '/hbpuuser/hbpuuser/ecardverify',
    method: 'post',
    data: data
  });
}

// 湖北理工用户信息保存
export function ecardSave(data) {
  return request({
    url: '/hbpuuser/hbpuuser/ecardsave',
    method: 'post',
    data: data
  });
}


// 更新用户寝室信息
export function updateUserRoomInfo(data) {
  return request({
    url: '/hbpuuser/hbpuuser/bind_room',
    method: 'post',
    data
  })
}

export function getRoomfee(data) {
  return request({
    url: '/hbpuuser/hbpuuser/getfee',
    method: 'post',
    data: data
  })
}

export function savesendkey(data) {
  return request({
    url: '/hbpuuser/hbpuuser/savekey',
    method: 'post',
    data: data
  })
}
export function saveways(data) {
  return request({
    url: '/hbpuuser/hbpuuser/saveways',
    method: 'post',
    data: data
  })
}

export function sendtest(data) {
  return request({
    url: '/hbpuuser/hbpuuser/sendtest',
    method: 'post',
    data: data
  })
}


