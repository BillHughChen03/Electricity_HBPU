from sqlalchemy import delete, select, update, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from module_admin.system.entity.do.hbpuuser_do import HbpuUser
from module_admin.system.entity.vo.hbpuuser_vo import HbpuuserModel, HbpuuserPageQueryModel
from utils.page_util import PageUtil


class HbpuuserDao:
    """
    湖北理工用户模块数据库操作层
    """

    @classmethod
    async def get_hbpuuser_detail_by_id(cls, db: AsyncSession, uid: int):
        """
        根据用户id获取湖北理工用户详细信息

        :param db: orm对象
        :param uid: 用户id
        :return: 湖北理工用户信息对象
        """
        hbpuuser_info = (
            (
                await db.execute(
                    select(HbpuUser)
                    .where(
                        HbpuUser.uid == uid
                    )
                )
            )
            .scalars()
            .first()
        )

        return hbpuuser_info

    @classmethod
    async def get_hbpuuser_detail_by_info(cls, db: AsyncSession, hbpuuser: HbpuuserModel):
        """
        根据湖北理工用户参数获取湖北理工用户信息

        :param db: orm对象
        :param hbpuuser: 湖北理工用户参数对象
        :return: 湖北理工用户信息对象
        """
        hbpuuser_info = (
            (
                await db.execute(
                    select(HbpuUser).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return hbpuuser_info

    @classmethod
    async def get_hbpuuser_list(cls, db: AsyncSession, query_object: HbpuuserPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取湖北理工用户列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 湖北理工用户列表信息对象
        """
        query = (
            select(HbpuUser)
            .where(
                HbpuUser.husername.like(f'%{query_object.husername}%') if query_object.husername else True,
                HbpuUser.hpassword == query_object.hpassword if query_object.hpassword else True,
                HbpuUser.access_token == query_object.access_token if query_object.access_token else True,
                HbpuUser.refresh_token == query_object.refresh_token if query_object.refresh_token else True,
                HbpuUser.token_time == query_object.token_time if query_object.token_time else True,
                HbpuUser.token_type == query_object.token_type if query_object.token_type else True,
                HbpuUser.sno == query_object.sno if query_object.sno else True,
                HbpuUser.name.like(f'%{query_object.name}%') if query_object.name else True,
                HbpuUser.building == query_object.building if query_object.building else True,
                HbpuUser.room == query_object.room if query_object.room else True,
                HbpuUser.sendky == query_object.sendky if query_object.sendky else True,
                HbpuUser.email == query_object.email if query_object.email else True,
                HbpuUser.access_email == query_object.access_email if query_object.access_email else True,
                HbpuUser.pushkey == query_object.pushkey if query_object.pushkey else True,
            )
            .order_by(HbpuUser.uid)
            .distinct()
        )
        hbpuuser_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return hbpuuser_list

    @classmethod
    async def add_hbpuuser_dao(cls, db: AsyncSession, hbpuuser: HbpuuserModel):
        """
        新增湖北理工用户数据库操作

        :param db: orm对象
        :param hbpuuser: 湖北理工用户对象
        :return:
        """
        db_hbpuuser = HbpuUser(**hbpuuser.model_dump(exclude={}))
        db.add(db_hbpuuser)
        await db.flush()

        return db_hbpuuser

    @classmethod
    async def edit_hbpuuser_dao(cls, db: AsyncSession, hbpuuser: dict):
        """
        编辑湖北理工用户数据库操作

        :param db: orm对象
        :param hbpuuser: 需要更新的湖北理工用户字典
        :return:
        """
        await db.execute(update(HbpuUser), [hbpuuser])

    @classmethod
    async def delete_hbpuuser_dao(cls, db: AsyncSession, hbpuuser: HbpuuserModel):
        """
        删除湖北理工用户数据库操作

        :param db: orm对象
        :param hbpuuser: 湖北理工用户对象
        :return:
        """
        await db.execute(delete(HbpuUser).where(HbpuUser.uid.in_([hbpuuser.uid])))

    @classmethod
    async def update_room_info_by_uid(cls, db: AsyncSession, uid: int, building: str, room: str):
        """
        根据 UID 更新寝室信息，无需查询整条记录
        """
        stmt = (
            update(HbpuUser)
            .where(HbpuUser.uid == uid)
            .values(building=building, room=room)
        )
        await db.execute(stmt)
        await db.commit()
        return {"uid": uid, "building": building, "room": room}

    @classmethod
    async def get_hbpuuser_detail_by_pushkey(cls, db: AsyncSession):
        result = await db.execute(
            select(
                HbpuUser.uid,
                HbpuUser.husername,
                HbpuUser.hpassword,
                HbpuUser.access_token,
                HbpuUser.building,
                HbpuUser.room,
                HbpuUser.sendky,
                HbpuUser.token_type
            ).where(
                or_(HbpuUser.pushkey == "2", HbpuUser.pushkey == "3")
            )
        )
        rows = result.all()  # rows 是 list[tuple]
        indexed_rows = [(i, *row) for i, row in enumerate(rows)]
        return indexed_rows

    @classmethod
    async def update_token_info_by_uid(cls, db: AsyncSession, uid: int, access: str, refresh: str):
        """
        根据 UID 更新寝室信息，无需查询整条记录
        """
        stmt = (
            update(HbpuUser)
            .where(HbpuUser.uid == uid)
            .values(access_token=access, refresh_token=refresh)
        )
        await db.execute(stmt)
        await db.commit()
        return True
