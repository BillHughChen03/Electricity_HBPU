import request from '@/utils/request'

// 查询寝室查询表列表
export function listHbpudept(query) {
  return request({
    url: '/hbpudept/hbpudept/list',
    method: 'get',
    params: query
  })
}

// 查询寝室查询表详细
export function getHbpudept(school) {
  return request({
    url: '/hbpudept/hbpudept/' + school,
    method: 'get'
  })
}

// 新增寝室查询表
export function addHbpudept(data) {
  return request({
    url: '/hbpudept/hbpudept',
    method: 'post',
    data: data
  })
}

// 修改寝室查询表
export function updateHbpudept(data) {
  return request({
    url: '/hbpudept/hbpudept',
    method: 'put',
    data: data
  })
}

// 删除寝室查询表
export function delHbpudept(school) {
  return request({
    url: '/hbpudept/hbpudept/' + school,
    method: 'delete'
  })
}

/**
 * 分级查询接口调用封装
 * @param {Object} query - 查询参数，可能包含 school, area, building_name, floor, room_num
 * @returns {Promise<Array|Object>} - 中间级别返回数组选项，最后一级返回详细对象 { Dept: {...} }
 */
export function cascadeOptions(query = {}) {
  return request({
    url: '/hbpudept/hbpudept/cascade_options',
    method: 'get',
    params: query
  }).then(res => {
    if (res.code === 200) {
      // 返回结果有两种格式，统一处理下：
      if (Array.isArray(res.data)) {
        // 中间级，返回数组
        return res.data
      } else if (res.data && res.data.Dept) {
        // 最后一级，返回对象
        return res.data
      }
    }
    return []
  })
}

export function loadcurrentroom(room) {
  return request({
    url: '/hbpudept/hbpudept/getroomdetails/' + room,
    method: 'get'
  })
}
