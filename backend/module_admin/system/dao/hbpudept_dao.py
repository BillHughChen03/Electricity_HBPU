from sqlalchemy import delete, select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.system.entity.do.hbpudept_do import Dept
from module_admin.system.entity.vo.hbpudept_vo import HbpudeptModel, HbpudeptPageQueryModel, AutoDeptQueryModel
from utils.page_util import PageUtil


class HbpudeptDao:
    """
    寝室查询表模块数据库操作层
    """

    @classmethod
    async def get_hbpudept_detail_by_id(cls, db: AsyncSession, school: int):
        """
        根据校区获取寝室查询表详细信息

        :param db: orm对象
        :param school: 校区
        :return: 寝室查询表信息对象
        """
        hbpudept_info = (
            (
                await db.execute(
                    select(Dept)
                    .where(
                        Dept.school == school
                    )
                )
            )
            .scalars()
            .first()
        )

        return hbpudept_info

    @classmethod
    async def get_hbpudept_detail_by_room(cls, db: AsyncSession, room: str):
        """
        根据房间获取寝室查询表详细信息

        :param db: orm对象
        :param school: 校区
        :return: 寝室查询表信息对象
        """
        hbpudept_info = (
            (
                await db.execute(
                    select(Dept)
                    .where(
                        Dept.room == room
                    )
                )
            )
            .scalars()
            .first()
        )

        return hbpudept_info

    @classmethod
    async def get_hbpudept_detail_by_info(cls, db: AsyncSession, hbpudept: HbpudeptModel):
        """
        根据寝室查询表参数获取寝室查询表信息

        :param db: orm对象
        :param hbpudept: 寝室查询表参数对象
        :return: 寝室查询表信息对象
        """
        hbpudept_info = (
            (
                await db.execute(
                    select(Dept).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return hbpudept_info

    @classmethod
    async def get_hbpudept_list(cls, db: AsyncSession, query_object: AutoDeptQueryModel, is_page: bool = False):
        """
        根据查询参数获取寝室查询表列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 寝室查询表列表信息对象
        """
        query = (
            select(Dept)
            .where(
                Dept.school == query_object.school if query_object.school else True,
                Dept.area == query_object.area if query_object.area else True,
                Dept.building_name == query_object.building_name if query_object.building_name else True,
                Dept.floor == query_object.floor if query_object.floor else True,
                Dept.room_num == query_object.room_num if query_object.room_num else True,
                Dept.room == query_object.room if query_object.room else True,
                Dept.building == query_object.building if query_object.building else True,
            )
            .order_by(Dept.school)
            .distinct()
        )
        hbpudept_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return hbpudept_list

    @classmethod
    async def add_hbpudept_dao(cls, db: AsyncSession, hbpudept: HbpudeptModel):
        """
        新增寝室查询表数据库操作

        :param db: orm对象
        :param hbpudept: 寝室查询表对象
        :return:
        """
        db_hbpudept = Dept(**hbpudept.model_dump(exclude={}))
        db.add(db_hbpudept)
        await db.flush()

        return db_hbpudept

    @classmethod
    async def edit_hbpudept_dao(cls, db: AsyncSession, hbpudept: dict):
        """
        编辑寝室查询表数据库操作

        :param db: orm对象
        :param hbpudept: 需要更新的寝室查询表字典
        :return:
        """
        await db.execute(update(Dept), [hbpudept])

    @classmethod
    async def delete_hbpudept_dao(cls, db: AsyncSession, hbpudept: HbpudeptModel):
        """
        删除寝室查询表数据库操作

        :param db: orm对象
        :param hbpudept: 寝室查询表对象
        :return:
        """
        await db.execute(delete(Dept).where(Dept.school.in_([hbpudept.school])))

    """
    寝室查询表模块数据库操作层
    """

    @classmethod
    async def get_cascade_options_by_level(cls, db: AsyncSession, level: str, **kwargs):
        """
        根据分级查询的级别获取对应的数据

        :param db: orm对象
        :param level: 分级查询的级别（school, area, building_name, floor, room_num）
        :param kwargs: 其他查询参数（school, area, building_name, floor）
        :return: 查询结果列表
        """
        query = select(Dept)
        if level == 'school':
            query = query.with_only_columns(Dept.school).distinct()
        elif level == 'area':
            query = query.with_only_columns(Dept.area).distinct().where(Dept.school == kwargs.get('school'))
        elif level == 'building_name':
            query = query.with_only_columns(Dept.building_name).distinct().where(
                Dept.school == kwargs.get('school'),
                Dept.area == kwargs.get('area')
            )
        elif level == 'floor':
            print("!!!!!    building_name", Dept.building_name)
            query = query.with_only_columns(Dept.floor).distinct().where(
                Dept.school == kwargs.get('school'),
                Dept.area == kwargs.get('area'),
                Dept.building_name == kwargs.get('building_name'),
            )
        elif level == 'room_num':
            query = query.with_only_columns(Dept.room_num).distinct().where(
                Dept.school == kwargs.get('school'),
                Dept.area == kwargs.get('area'),
                Dept.building_name == kwargs.get('building_name'),
                Dept.floor == kwargs.get('floor')
            )
        else:
            raise ValueError("Invalid level for cascade options")

        result = await db.execute(query)
        return [row[0] for row in result.all()]

    @classmethod
    async def get_detail_by_room_num(cls, query_db: AsyncSession, school: str, area: str, building_name: str,
                                     floor: str, room_num: str):
        stmt = select(Dept).where(
            and_(
                Dept.school == school,
                Dept.area == area,
                Dept.building_name == building_name,
                Dept.floor == floor,
                Dept.room_num == room_num
            )
        )
        result = await query_db.execute(stmt)
        row = result.fetchone()
        if row is None:
            return None
        else:
            return dict(row._mapping)
