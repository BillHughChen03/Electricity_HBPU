from datetime import datetime
from typing import List, Optional

from sqlalchemy import delete, update, desc, insert
from sqlalchemy import select, and_, between
from sqlalchemy.ext.asyncio import AsyncSession

from module_admin.system.entity.do.electricity_do import HbpuElectricity
from module_admin.system.entity.vo.electricity_vo import ElectricityModel, ElectricityPageQueryModel
from utils.page_util import PageUtil


class ElectricityDao:
    """
    电力模块数据库操作层
    """

    @classmethod
    async def get_electricity_detail_by_id(cls, db: AsyncSession, info_id: int):
        """
        根据数据编号获取电力详细信息

        :param db: orm对象
        :param info_id: 数据编号
        :return: 电力信息对象
        """
        electricity_info = (
            (
                await db.execute(
                    select(HbpuElectricity)
                    .where(
                        HbpuElectricity.info_id == info_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return electricity_info

    @classmethod
    async def get_electricity_detail_by_info(cls, db: AsyncSession, electricity: ElectricityModel):
        """
        根据电力参数获取电力信息

        :param db: orm对象
        :param electricity: 电力参数对象
        :return: 电力信息对象
        """
        electricity_info = (
            (
                await db.execute(
                    select(HbpuElectricity).where(
                        HbpuElectricity.info_id == electricity.info_id if electricity.info_id else True,
                    )
                )
            )
            .scalars()
            .first()
        )

        return electricity_info

    @classmethod
    async def get_electricity_list(cls, db: AsyncSession, query_object: ElectricityPageQueryModel,
                                   is_page: bool = False):
        """
        根据查询参数获取电力列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 电力列表信息对象
        """
        query = (
            select(HbpuElectricity)
            .where(
                HbpuElectricity.info_id == query_object.info_id if query_object.info_id else True,
                HbpuElectricity.total == query_object.total if query_object.total else True,
                HbpuElectricity.remaining == query_object.remaining if query_object.remaining else True,
                HbpuElectricity.campus == query_object.campus if query_object.campus else True,
                HbpuElectricity.building_name.like(
                    f'%{query_object.building_name}%') if query_object.building_name else True,
                HbpuElectricity.room_name.like(f'%{query_object.room_name}%') if query_object.room_name else True,
                HbpuElectricity.building == query_object.building if query_object.building else True,
                HbpuElectricity.room == query_object.room if query_object.room else True,
                HbpuElectricity.finish_time == query_object.finish_time if query_object.finish_time else True,
                HbpuElectricity.yesterday_remaining == query_object.yesterday_remaining if query_object.yesterday_remaining else True,
            )
            .order_by(HbpuElectricity.info_id)
            .distinct()
        )
        electricity_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return electricity_list

    @classmethod
    async def add_electricity_dao(cls, db: AsyncSession, electricity: ElectricityModel):
        """
        新增电力数据库操作

        :param db: orm对象
        :param electricity: 电力对象
        :return:
        """
        db_electricity = HbpuElectricity(**electricity.model_dump(exclude={}))
        db.add(db_electricity)
        await db.flush()

        return db_electricity

    @classmethod
    async def edit_electricity_dao(cls, db: AsyncSession, electricity: dict):
        """
        编辑电力数据库操作

        :param db: orm对象
        :param electricity: 需要更新的电力字典
        :return:
        """
        await db.execute(update(HbpuElectricity), [electricity])

    @classmethod
    async def delete_electricity_dao(cls, db: AsyncSession, electricity: ElectricityModel):
        """
        删除电力数据库操作

        :param db: orm对象
        :param electricity: 电力对象
        :return:
        """
        await db.execute(delete(HbpuElectricity).where(HbpuElectricity.info_id.in_([electricity.info_id])))

    @classmethod
    async def get_latest_remaining_by_room(cls, db: AsyncSession, room: str):
        result = await db.execute(
            select(HbpuElectricity.remaining)  # 只查询remaining字段
            .where(HbpuElectricity.room == room)
            .order_by(desc(HbpuElectricity.info_id))  # 最新一条记录
            .limit(1)
        )
        remaining = result.scalar_one_or_none()
        if remaining is None:
            remaining = "0"
        return remaining

    @classmethod
    async def add_electricity_by_room(
            cls,
            db: AsyncSession,
            total: str = None,
            remaining: str = None,
            campus: str = None,
            building_name: str = None,
            room_name: str = None,
            building: str = None,
            room: str = None,
            finish_time=None,  # 如果是datetime类型，直接传datetime对象
            yesterday_remaining: str = None,
    ):
        try:
            stmt = insert(HbpuElectricity).values(
                total=total,
                remaining=remaining,
                campus=campus,
                building_name=building_name,
                room_name=room_name,
                building=building,
                room=room,
                finish_time=finish_time,
                yesterday_remaining=yesterday_remaining,
            )
            await db.execute(stmt)
            await db.commit()
            return True
        except Exception as e:
            print(f"插入失败：{e}")
            await db.rollback()
            return False

    @classmethod
    async def get_electricity_data(
            cls,
            db: AsyncSession,
            campus: Optional[str],
            building: Optional[str],
            room: Optional[str],
            start_time: Optional[str],
            end_time: Optional[str]
    ) -> List[HbpuElectricity]:
        stmt = select(HbpuElectricity)
        conditions = []

        if campus:
            conditions.append(HbpuElectricity.campus == campus)
        if building:
            conditions.append(HbpuElectricity.building == building)
        if room:
            conditions.append(HbpuElectricity.room == room)

        # 如果提供了时间范围，则使用 finish_time 范围筛选
        if start_time and end_time:
            start = datetime.fromisoformat(start_time)
            end = datetime.fromisoformat(end_time)
            conditions.append(between(HbpuElectricity.finish_time, start, end))
        else:
            # 否则返回该房间所有历史记录
            if building and room:
                conditions.append(HbpuElectricity.building == building)
                conditions.append(HbpuElectricity.room == room)

        if conditions:
            stmt = stmt.where(and_(*conditions))

        stmt = stmt.order_by(HbpuElectricity.info_id.desc())

        result = await db.execute(stmt)
        return result.scalars().all()