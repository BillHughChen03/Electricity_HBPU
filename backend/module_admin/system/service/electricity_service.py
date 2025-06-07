from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy import select, and_, func
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.system.dao.electricity_dao import ElectricityDao
from module_admin.system.entity.vo.electricity_vo import DeleteElectricityModel, ElectricityModel, \
    ElectricityPageQueryModel, ElectricityQueryModel2
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class ElectricityService:
    """
    电力模块服务层
    """

    @classmethod
    async def get_electricity_list_services(
            cls, query_db: AsyncSession, query_object: ElectricityPageQueryModel, is_page: bool = False
    ):
        """
        获取电力列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 电力列表信息对象
        """
        electricity_list_result = await ElectricityDao.get_electricity_list(query_db, query_object, is_page)

        return electricity_list_result

    @classmethod
    async def check_info_id_unique_services(cls, query_db: AsyncSession, page_object: ElectricityModel):
        """
        检查数据编号是否唯一service

        :param query_db: orm对象
        :param page_object: 电力对象
        :return: 校验结果
        """
        info_id = -1 if page_object.info_id is None else page_object.info_id
        electricity = await ElectricityDao.get_electricity_detail_by_info(query_db,
                                                                          ElectricityModel(infoId=page_object.info_id))
        if electricity and electricity.info_id != info_id:
            return CommonConstant.NOT_UNIQUE
        return CommonConstant.UNIQUE

    @classmethod
    async def add_electricity_services(cls, query_db: AsyncSession, page_object: ElectricityModel):
        """
        新增电力信息service

        :param query_db: orm对象
        :param page_object: 新增电力对象
        :return: 新增电力校验结果
        """
        if not await cls.check_info_id_unique_services(query_db, page_object):
            raise ServiceException(message=f'新增电力{page_object.info_id}失败，数据编号已存在')
        try:
            await ElectricityDao.add_electricity_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_electricity_services(cls, query_db: AsyncSession, page_object: ElectricityModel):
        """
        编辑电力信息service

        :param query_db: orm对象
        :param page_object: 编辑电力对象
        :return: 编辑电力校验结果
        """
        edit_electricity = page_object.model_dump(exclude_unset=True, exclude={})
        electricity_info = await cls.electricity_detail_services(query_db, page_object.info_id)
        if electricity_info.info_id:
            if not await cls.check_info_id_unique_services(query_db, page_object):
                raise ServiceException(message=f'修改电力{page_object.info_id}失败，数据编号已存在')
            try:
                await ElectricityDao.edit_electricity_dao(query_db, edit_electricity)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='电力不存在')

    @classmethod
    async def delete_electricity_services(cls, query_db: AsyncSession, page_object: DeleteElectricityModel):
        """
        删除电力信息service

        :param query_db: orm对象
        :param page_object: 删除电力对象
        :return: 删除电力校验结果
        """
        if page_object.info_ids:
            info_id_list = page_object.info_ids.split(',')
            try:
                for info_id in info_id_list:
                    await ElectricityDao.delete_electricity_dao(query_db, ElectricityModel(infoId=info_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入数据编号为空')

    @classmethod
    async def electricity_detail_services(cls, query_db: AsyncSession, info_id: int):
        """
        获取电力详细信息service

        :param query_db: orm对象
        :param info_id: 数据编号
        :return: 数据编号对应的信息
        """
        electricity = await ElectricityDao.get_electricity_detail_by_id(query_db, info_id=info_id)
        if electricity:
            result = ElectricityModel(**CamelCaseUtil.transform_result(electricity))
        else:
            result = ElectricityModel(**dict())

        return result

    @staticmethod
    async def export_electricity_list_services(electricity_list: List):
        """
        导出电力信息service

        :param electricity_list: 电力信息列表
        :return: 电力信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'infoId': '数据编号',
            'total': '总用电',
            'remaining': '剩余电量',
            'campus': '校区',
            'buildingName': '宿舍区',
            'roomName': '房间号',
            'building': '宿舍楼编号',
            'room': '房间号',
            'finishTime': '完成时间',
            'yesterdayRemaining': '昨日剩余电量',
        }
        binary_data = ExcelUtil.export_list2excel(electricity_list, mapping_dict)

        return binary_data

    class ElectricityService:
        @classmethod
        async def get_latest_remaining_by_room(cls, db: AsyncSession, room: str):
            remaining = await ElectricityDao.get_latest_remaining_by_room(db, room)
            # 这里你可以做一些额外处理，比如默认值处理、日志等
            if remaining is None:
                remaining = 0  # 或者根据业务需求设定默认值
            return remaining

    @classmethod
    async def get_electricity_data(
            cls,
            db: AsyncSession,
            campus: str,
            building: str,
            room: str,
            start_time: str,
            end_time: str
    ):
        return await ElectricityDao.get_electricity_data(
            db, campus, building, room, start_time, end_time
        )

