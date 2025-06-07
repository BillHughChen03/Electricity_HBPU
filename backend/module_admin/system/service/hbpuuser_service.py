from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.system.dao.hbpuuser_dao import HbpuuserDao
from module_admin.system.entity.do.hbpuuser_do import HbpuUser
from module_admin.system.entity.vo.hbpuuser_vo import DeleteHbpuuserModel, HbpuuserModel, HbpuuserPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class HbpuuserService:
    """
    湖北理工用户模块服务层
    """

    @classmethod
    async def get_hbpuuser_list_services(
            cls, query_db: AsyncSession, query_object: HbpuuserPageQueryModel, is_page: bool = False
    ):
        """
        获取湖北理工用户列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 湖北理工用户列表信息对象
        """
        hbpuuser_list_result = await HbpuuserDao.get_hbpuuser_list(query_db, query_object, is_page)

        return hbpuuser_list_result

    @classmethod
    async def add_hbpuuser_services(cls, query_db: AsyncSession, page_object: HbpuuserModel):
        """
        新增湖北理工用户信息service

        :param query_db: orm对象
        :param page_object: 新增湖北理工用户对象
        :return: 新增湖北理工用户校验结果
        """
        try:
            await HbpuuserDao.add_hbpuuser_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_hbpuuser_services(cls, query_db: AsyncSession, page_object: HbpuuserModel):
        """
        编辑湖北理工用户信息service

        :param query_db: orm对象
        :param page_object: 编辑湖北理工用户对象
        :return: 编辑湖北理工用户校验结果
        """
        edit_hbpuuser = page_object.model_dump(exclude_unset=True, exclude={})
        hbpuuser_info = await cls.hbpuuser_detail_services(query_db, page_object.uid)
        if hbpuuser_info.uid:
            try:
                await HbpuuserDao.edit_hbpuuser_dao(query_db, edit_hbpuuser)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='湖北理工用户不存在')

    @classmethod
    async def delete_hbpuuser_services(cls, query_db: AsyncSession, page_object: DeleteHbpuuserModel):
        """
        删除湖北理工用户信息service

        :param query_db: orm对象
        :param page_object: 删除湖北理工用户对象
        :return: 删除湖北理工用户校验结果
        """
        if page_object.uids:
            uid_list = page_object.uids.split(',')
            try:
                for uid in uid_list:
                    await HbpuuserDao.delete_hbpuuser_dao(query_db, HbpuuserModel(uid=uid))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入用户id为空')

    @classmethod
    async def hbpuuser_detail_services(cls, query_db: AsyncSession, uid: int):
        """
        获取湖北理工用户详细信息service

        :param query_db: orm对象
        :param uid: 用户id
        :return: 用户id对应的信息
        """
        hbpuuser = await HbpuuserDao.get_hbpuuser_detail_by_id(query_db, uid=uid)
        if hbpuuser:
            result = HbpuuserModel(**CamelCaseUtil.transform_result(hbpuuser))
        else:
            result = HbpuuserModel(**dict())

        return result

    @staticmethod
    async def export_hbpuuser_list_services(hbpuuser_list: List):
        """
        导出湖北理工用户信息service

        :param hbpuuser_list: 湖北理工用户信息列表
        :return: 湖北理工用户信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'uid': '用户id',
            'husername': '湖北理工username',
            'hpassword': '湖北理工password',
            'accessToken': '湖北理工access_token',
            'refreshToken': '湖北理工refresh_token',
            'tokenTime': '获取token的时间',
            'tokenType': 'Token Type',
            'sno': 'SNO学号',
            'name': '姓名',
            'building': '楼栋号',
            'room': '房间号',
            'sendky': '微信推送send_key',
            'email': '邮件推送',
            'accessEmail': '邮箱认证',
            'psuhTime': '推送时间',
            'pushkey': '微信推送Key',
        }
        binary_data = ExcelUtil.export_list2excel(hbpuuser_list, mapping_dict)

        return binary_data

    @classmethod
    async def hbpuuser_insert(cls, query_db: AsyncSession, access_token: str, token_type: str, refresh_token: str,
                              sno: str, name: str, uid: int, ecardUsername: str, ecardPassword: str):
        """插入用户信息"""
        hbpuuser = HbpuuserModel(
            uid=uid,
            husername=ecardUsername,
            hpassword=ecardPassword,
            access_token=access_token,
            token_type=token_type,
            refresh_token=refresh_token,
            sno=sno,
            name=name,
            token_time=datetime.utcnow()
        )
        try:
            await HbpuuserDao.insert_hbpuuser_dao(query_db, hbpuuser)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @staticmethod
    async def bind_room_info(db: AsyncSession, uid: int, building: str, room: str):
        return await HbpuuserDao.update_room_info_by_uid(db, uid, building, room)

    @classmethod
    async def hbpuuser_detail_services2(cls, query_db: AsyncSession, uid: int):
        """
        获取湖北理工用户详细信息service

        :param query_db: orm对象
        :param uid: 用户id
        :return: 用户id对应的信息
        """
        hbpuuser = await HbpuuserDao.get_hbpuuser_detail_by_id(query_db, uid=uid)
        if hbpuuser:
            return HbpuuserModel(**CamelCaseUtil.transform_result(hbpuuser))
        else:
            return None

    @classmethod
    async def hbpuuser_detail_services_by_pushkey(cls, query_db: AsyncSession):
        data = await HbpuuserDao.get_hbpuuser_detail_by_pushkey(query_db)
        num = len(data)
        return data, num



