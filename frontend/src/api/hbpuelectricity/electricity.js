import request from '@/utils/request'

// 查询电力列表
export function listElectricity(query) {
  return request({
    url: '/hbpuelectricity/electricity/list',
    method: 'get',
    params: query
  })
}

// 查询电力详细
export function getElectricity(infoId) {
  return request({
    url: '/hbpuelectricity/electricity/' + infoId,
    method: 'get'
  })
}

// 新增电力
export function addElectricity(data) {
  return request({
    url: '/hbpuelectricity/electricity',
    method: 'post',
    data: data
  })
}

// 修改电力
export function updateElectricity(data) {
  return request({
    url: '/hbpuelectricity/electricity',
    method: 'put',
    data: data
  })
}

// 删除电力
export function delElectricity(infoId) {
  return request({
    url: '/hbpuelectricity/electricity/' + infoId,
    method: 'delete'
  })
}

export function listRoomTime(query) {
  return request({
    url: '/hbpuelectricity/electricity/room/list',
    method: 'get',
    params: query
  })
}
