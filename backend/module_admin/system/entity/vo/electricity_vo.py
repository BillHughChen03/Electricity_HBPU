from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query


class ElectricityModel(BaseModel):
    """
    电力表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    info_id: Optional[int] = Field(default=None, description='数据编号')
    total: Optional[str] = Field(default=None, description='总用电')
    remaining: Optional[str] = Field(default=None, description='剩余电量')
    campus: Optional[str] = Field(default=None, description='校区')
    building_name: Optional[str] = Field(default=None, description='宿舍区')
    room_name: Optional[str] = Field(default=None, description='房间号')
    building: Optional[str] = Field(default=None, description='宿舍楼编号')
    room: Optional[str] = Field(default=None, description='房间号')
    finish_time: Optional[datetime] = Field(default=None, description='完成时间')
    yesterday_remaining: Optional[str] = Field(default=None, description='昨日剩余电量')


class ElectricityQueryModel(ElectricityModel):
    """
    电力不分页查询模型
    """
    pass


@as_query
class ElectricityPageQueryModel(ElectricityQueryModel):
    """
    电力分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')

@as_query
class ElectricityQueryModel2(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    info_id: Optional[int] = Field(default=None, description='数据编号')
    total: Optional[str] = Field(default=None, description='总用电')
    remaining: Optional[str] = Field(default=None, description='剩余电量')
    campus: Optional[str] = Field(default=None, description='校区')
    building_name: Optional[str] = Field(default=None, description='宿舍区')
    room_name: Optional[str] = Field(default=None, description='房间号')
    building: Optional[str] = Field(default=None, description='宿舍楼编号')
    room: Optional[str] = Field(default=None, description='房间号')
    finish_time: Optional[datetime] = Field(default=None, description='完成时间')
    yesterday_remaining: Optional[str] = Field(default=None, description='昨日剩余电量')
    start_time: Optional[datetime] = Field(None, alias='start_time', description="查询开始时间")
    end_time: Optional[datetime] = Field(None, alias='end_time', description="查询结束时间")


class DeleteElectricityModel(BaseModel):
    """
    删除电力模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    info_ids: str = Field(description='需要删除的数据编号')
