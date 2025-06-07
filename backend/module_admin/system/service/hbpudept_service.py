from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.system.dao.hbpudept_dao import HbpudeptDao
from module_admin.system.entity.vo.hbpudept_vo import DeleteHbpudeptModel, HbpudeptModel, HbpudeptPageQueryModel, \
    HbpudeptQueryModel, AutoDeptQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class HbpudeptService:
    """
    寝室查询表模块服务层
    """

    @classmethod
    async def get_hbpudept_list_services(
            cls, query_db: AsyncSession, query_object: HbpudeptPageQueryModel, is_page: bool = False
    ):
        """
        获取寝室查询表列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 寝室查询表列表信息对象
        """
        hbpudept_list_result = await HbpudeptDao.get_hbpudept_list(query_db, query_object, is_page)

        return hbpudept_list_result

    @classmethod
    async def add_hbpudept_services(cls, query_db: AsyncSession, page_object: HbpudeptModel):
        """
        新增寝室查询表信息service

        :param query_db: orm对象
        :param page_object: 新增寝室查询表对象
        :return: 新增寝室查询表校验结果
        """
        try:
            await HbpudeptDao.add_hbpudept_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_hbpudept_services(cls, query_db: AsyncSession, page_object: HbpudeptModel):
        """
        编辑寝室查询表信息service

        :param query_db: orm对象
        :param page_object: 编辑寝室查询表对象
        :return: 编辑寝室查询表校验结果
        """
        edit_hbpudept = page_object.model_dump(exclude_unset=True, exclude={})
        hbpudept_info = await cls.hbpudept_detail_services(query_db, page_object.school)
        if hbpudept_info.school:
            try:
                await HbpudeptDao.edit_hbpudept_dao(query_db, edit_hbpudept)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='寝室查询表不存在')

    @classmethod
    async def delete_hbpudept_services(cls, query_db: AsyncSession, page_object: DeleteHbpudeptModel):
        """
        删除寝室查询表信息service

        :param query_db: orm对象
        :param page_object: 删除寝室查询表对象
        :return: 删除寝室查询表校验结果
        """
        if page_object.schools:
            school_list = page_object.schools.split(',')
            try:
                for school in school_list:
                    await HbpudeptDao.delete_hbpudept_dao(query_db, HbpudeptModel(school=school))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入校区为空')

    @classmethod
    async def hbpudept_detail_services(cls, query_db: AsyncSession, school: int):
        """
        获取寝室查询表详细信息service

        :param query_db: orm对象
        :param school: 校区
        :return: 校区对应的信息
        """
        hbpudept = await HbpudeptDao.get_hbpudept_detail_by_id(query_db, school=school)
        if hbpudept:
            result = HbpudeptModel(**CamelCaseUtil.transform_result(hbpudept))
        else:
            result = HbpudeptModel(**dict())

        return result

    @staticmethod
    async def export_hbpudept_list_services(hbpudept_list: List):
        """
        导出寝室查询表信息service

        :param hbpudept_list: 寝室查询表信息列表
        :return: 寝室查询表信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'school': '校区',
            'area': '公寓区',
            'building_name': '楼栋号',
            'floor': '楼层',
            'roomNum': '房间号',
            'room': '房间id',
            'building': '楼栋id',
        }
        binary_data = ExcelUtil.export_list2excel(hbpudept_list, mapping_dict)

        return binary_data

    # @classmethod
    # async def get_hbpudept_list_services(
    #         cls, query_db: AsyncSession, query_object: AutoDeptQueryModel, is_page: bool = False
    # ):
    #     """
    #     获取寝室查询表列表信息service
    #
    #     :param query_db: orm对象
    #     :param query_object: 查询参数对象
    #     :param is_page: 是否开启分页
    #     :return: 寝室查询表列表信息对象
    #     """
    #     hbpudept_list_result = await HbpudeptDao.get_hbpudept_list(query_db, query_object, is_page)
    #
    #     return hbpudept_list_result

    @classmethod
    async def get_cascade_options_services(
            cls, query_db: AsyncSession, query_model: AutoDeptQueryModel
    ):
        print("进入分级查询：")
        print("Query Model 内容：", query_model.dict())

        # 优先处理 room_num 查询整条记录
        if query_model.room_num is not None:
            result = await HbpudeptDao.get_detail_by_room_num(
                query_db,
                school=query_model.school,
                area=query_model.area,
                building_name=query_model.building_name,
                floor=query_model.floor,
                room_num=query_model.room_num
            )
            return result

        # 原有的级联查询逻辑
        if query_model.school is None:
            result = await HbpudeptDao.get_cascade_options_by_level(query_db, level='school')
        elif query_model.area is None:
            result = await HbpudeptDao.get_cascade_options_by_level(query_db, level='area', school=query_model.school)
        elif query_model.building_name is None:
            result = await HbpudeptDao.get_cascade_options_by_level(query_db, level='building_name',
                                                                    school=query_model.school, area=query_model.area)
        elif query_model.floor is None:
            result = await HbpudeptDao.get_cascade_options_by_level(query_db, level='floor',
                                                                    school=query_model.school, area=query_model.area,
                                                                    building_name=query_model.building_name)
        else:
            result = await HbpudeptDao.get_cascade_options_by_level(query_db, level='room_num',
                                                                    school=query_model.school, area=query_model.area,
                                                                    building_name=query_model.building_name,
                                                                    floor=query_model.floor)
        return result

    @classmethod
    async def hbpudept_detail_services_by_room(cls, query_db: AsyncSession, room: str):
        """
        获取寝室查询表详细信息service

        :param query_db: orm对象
        :param school: 校区
        :return: 校区对应的信息
        """
        hbpudept = await HbpudeptDao.get_hbpudept_detail_by_room(query_db, room=room)
        if hbpudept:
            result = HbpudeptModel(**CamelCaseUtil.transform_result(hbpudept))
        else:
            result = HbpudeptModel(**dict())

        return result