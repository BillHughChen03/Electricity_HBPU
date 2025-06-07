from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class HbpuuserModel(BaseModel):
    """
    湖北理工用户表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    uid: Optional[int] = Field(default=None, description='用户id')
    husername: Optional[str] = Field(default=None, description='湖北理工username')
    hpassword: Optional[str] = Field(default=None, description='湖北理工password')
    access_token: Optional[str] = Field(default=None, description='湖北理工access_token')
    refresh_token: Optional[str] = Field(default=None, description='湖北理工refresh_token')
    token_time: Optional[datetime] = Field(default=None, description='获取token的时间')
    token_type: Optional[str] = Field(default=None, description='Token Type')
    sno: Optional[str] = Field(default=None, description='SNO学号')
    name: Optional[str] = Field(default=None, description='姓名')
    building: Optional[str] = Field(default=None, description='楼栋号')
    room: Optional[str] = Field(default=None, description='房间号')
    sendky: Optional[str] = Field(default=None, description='微信推送send_key')
    email: Optional[str] = Field(default=None, description='邮件推送')
    access_email: Optional[int] = Field(default=None, description='邮箱认证')
    psuh_time: Optional[datetime] = Field(default=None, description='推送时间')
    pushkey: Optional[str] = Field(default=None, description='微信推送Key')






class HbpuuserQueryModel(HbpuuserModel):
    """
    湖北理工用户不分页查询模型
    """
    pass


@as_query
class HbpuuserPageQueryModel(HbpuuserQueryModel):
    """
    湖北理工用户分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteHbpuuserModel(BaseModel):
    """
    删除湖北理工用户模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    uids: str = Field(description='需要删除的用户id')
