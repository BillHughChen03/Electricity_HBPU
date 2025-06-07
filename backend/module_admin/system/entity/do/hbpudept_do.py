from sqlalchemy import String, Column
from config.database import Base


class Dept(Base):
    """
    寝室查询表
    """
    __tablename__ = 'dept'
    __table_args__ = {'extend_existing': True}

    school = Column(String(255), nullable=True, comment='校区')
    area = Column(String(255), nullable=True, comment='公寓区')
    building_name = Column(String(255), nullable=True, comment='楼栋号')
    floor = Column(String(255), nullable=True, comment='楼层')
    room_num = Column(String(255), nullable=True, comment='房间号')
    room = Column(String(255), primary_key=True, comment='房间id')  # 设置为主键
    building = Column(String(255), nullable=True, comment='楼栋id')


