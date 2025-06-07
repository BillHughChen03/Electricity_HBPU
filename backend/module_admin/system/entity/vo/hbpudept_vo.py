from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query


class HbpudeptModel(BaseModel):
    """
    寝室查询表表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    school: Optional[str] = Field(default=None, description='校区')
    area: Optional[str] = Field(default=None, description='公寓区')
    building_name: Optional[str] = Field(default=None, description='楼栋号')
    floor: Optional[str] = Field(default=None, description='楼层')
    room_num: Optional[str] = Field(default=None, description='房间号')
    room: Optional[str] = Field(default=None, description='房间id')
    building: Optional[str] = Field(default=None, description='楼栋id')


class HbpudeptQueryModel(HbpudeptModel):
    """
    寝室查询表不分页查询模型
    """
    pass


class AutoDeptQueryModel(BaseModel):
    """
    寝室查询表不分页查询模型
    """
    school: Optional[str] = Field(default=None, description='校区')
    area: Optional[str] = Field(default=None, description='公寓区')
    building_name: Optional[str] = Field(default=None, description='楼栋号')
    floor: Optional[str] = Field(default=None, description='楼层')
    room_num: Optional[str] = Field(default=None, description='房间号')
    room: Optional[str] = Field(default=None, description='房间id')
    building: Optional[str] = Field(default=None, description='楼栋id')


@as_query
class HbpudeptPageQueryModel(HbpudeptQueryModel):
    """
    寝室查询表分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteHbpudeptModel(BaseModel):
    """
    删除寝室查询表模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    schools: str = Field(description='需要删除的校区')
