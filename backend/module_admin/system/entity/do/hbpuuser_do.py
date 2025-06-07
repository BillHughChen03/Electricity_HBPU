from sqlalchemy import DateTime, Integer, String, Column
from config.database import Base


class HbpuUser(Base):
    """
    湖北理工用户表
    """

    __tablename__ = 'hbpu_user'

    uid = Column(Integer, primary_key=True, nullable=False, comment='用户id')
    husername = Column(String(255), nullable=True, comment='湖北理工username')
    hpassword = Column(String(255), nullable=True, comment='湖北理工password')
    access_token = Column(String(2048), nullable=True, comment='湖北理工access_token')
    refresh_token = Column(String(2048), nullable=True, comment='湖北理工refresh_token')
    token_time = Column(DateTime, nullable=True, comment='获取token的时间')
    token_type = Column(String(255), nullable=True, comment='Token Type')
    sno = Column(String(255), nullable=True, comment='SNO学号')
    name = Column(String(255), nullable=True, comment='姓名')
    building = Column(String(255), nullable=True, comment='楼栋号')
    room = Column(String(255), nullable=True, comment='房间号')
    sendky = Column(String(255), nullable=True, comment='微信推送send_key')
    email = Column(String(255), nullable=True, comment='邮件推送')
    access_email = Column(Integer, nullable=True, comment='邮箱认证')
    psuh_time = Column(DateTime, nullable=True, comment='推送时间')
    pushkey = Column(String(512), nullable=True, comment='微信推送Key')




