from pydantic import ConfigDict
from pydantic.alias_generators import to_camel
from sqlalchemy import String, Integer, DateTime, Column
from config.database import Base


class HbpuElectricity(Base):
    """
    电力表
    """

    __tablename__ = 'hbpu_electricity'

    info_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='数据编号')
    total = Column(String(255), nullable=True, comment='总用电')
    remaining = Column(String(255), nullable=True, comment='剩余电量')
    campus = Column(String(255), nullable=True, comment='校区')
    building_name = Column(String(255), nullable=True, comment='宿舍区')
    room_name = Column(String(255), nullable=True, comment='房间号')
    building = Column(String(255), nullable=True, comment='宿舍楼编号')
    room = Column(String(255), nullable=True, comment='房间号')
    finish_time = Column(DateTime, nullable=True, comment='完成时间')
    yesterday_remaining = Column(String(255), nullable=True, comment='昨日剩余电量')

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )



