from datetime import datetime

from fastapi import APIRouter, Depends, Form, Request, Query
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_admin.system.service.hbpudept_service import HbpudeptService
from module_admin.system.entity.vo.hbpudept_vo import DeleteHbpudeptModel, HbpudeptModel, HbpudeptPageQueryModel, \
    HbpudeptQueryModel, AutoDeptQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

hbpudeptController = APIRouter(prefix='/hbpudept/hbpudept', dependencies=[Depends(LoginService.get_current_user)])


@hbpudeptController.get('/cascade_options')
@Log(title='寝室查询表分级查询', business_type=BusinessType.OTHER)
async def get_cascade_options(
    request: Request,
    query_db: AsyncSession = Depends(get_db),
):
    """
    用于分级查询：
    - 如果不传任何参数，返回所有校区（school）
    - 传 school，返回该校区下的所有公寓区（area）
    - 传 school 和 area，返回楼栋（building_name）
    - 传 school、area、building_name，返回楼层（floor）
    - 传 school、area、building_name、floor，返回房间号（room_num）
    """
    # 从 request.query_params 中直接获取参数
    query_params = request.query_params
    school = query_params.get('school')
    area = query_params.get('area')
    building_name = query_params.get('building_name')
    floor = query_params.get('floor')

    # 打印接收到的参数
    print(f"Received parameters: school={school}, area={area}, building_name={building_name}, floor={floor}")

    query_model = AutoDeptQueryModel(**dict(request.query_params))
    print("构建模型内容：", query_model.dict())
    result = await HbpudeptService.get_cascade_options_services(query_db, query_model)
    return ResponseUtil.success(data=result)


@hbpudeptController.get(
    '/list', response_model=PageResponseModel
)
async def get_hbpudept_hbpudept_list(
        request: Request,
        hbpudept_page_query: HbpudeptPageQueryModel = Depends(HbpudeptPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    hbpudept_page_query_result = await HbpudeptService.get_hbpudept_list_services(query_db, hbpudept_page_query,
                                                                                  is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=hbpudept_page_query_result)


@hbpudeptController.post('')
@ValidateFields(validate_model='add_hbpudept')
@Log(title='寝室查询表', business_type=BusinessType.INSERT)
async def add_hbpudept_hbpudept(
        request: Request,
        add_hbpudept: HbpudeptModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_hbpudept_result = await HbpudeptService.add_hbpudept_services(query_db, add_hbpudept)
    logger.info(add_hbpudept_result.message)

    return ResponseUtil.success(msg=add_hbpudept_result.message)


@hbpudeptController.put('')
@ValidateFields(validate_model='edit_hbpudept')
@Log(title='寝室查询表', business_type=BusinessType.UPDATE)
async def edit_hbpudept_hbpudept(
        request: Request,
        edit_hbpudept: HbpudeptModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_hbpudept.update_by = current_user.user.user_name
    edit_hbpudept.update_time = datetime.now()
    edit_hbpudept_result = await HbpudeptService.edit_hbpudept_services(query_db, edit_hbpudept)
    logger.info(edit_hbpudept_result.message)

    return ResponseUtil.success(msg=edit_hbpudept_result.message)


@hbpudeptController.delete('/{schools}')
@Log(title='寝室查询表', business_type=BusinessType.DELETE)
async def delete_hbpudept_hbpudept(request: Request, schools: str, query_db: AsyncSession = Depends(get_db)):
    delete_hbpudept = DeleteHbpudeptModel(schools=schools)
    delete_hbpudept_result = await HbpudeptService.delete_hbpudept_services(query_db, delete_hbpudept)
    logger.info(delete_hbpudept_result.message)

    return ResponseUtil.success(msg=delete_hbpudept_result.message)


@hbpudeptController.get(
    '/{school}', response_model=HbpudeptModel
)
async def query_detail_hbpudept_hbpudept(request: Request, school: int, query_db: AsyncSession = Depends(get_db)):
    hbpudept_detail_result = await HbpudeptService.hbpudept_detail_services(query_db, school)
    logger.info(f'获取school为{school}的信息成功')

    return ResponseUtil.success(data=hbpudept_detail_result)


@hbpudeptController.post('/export')
@Log(title='寝室查询表', business_type=BusinessType.EXPORT)
async def export_hbpudept_hbpudept_list(
        request: Request,
        hbpudept_page_query: HbpudeptPageQueryModel = Form(),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    hbpudept_query_result = await HbpudeptService.get_hbpudept_list_services(query_db, hbpudept_page_query,
                                                                             is_page=False)
    hbpudept_export_result = await HbpudeptService.export_hbpudept_list_services(hbpudept_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(hbpudept_export_result))

@hbpudeptController.get(
    '/getroomdetails/{room}', response_model=HbpudeptModel
)
async def query_detail_hbpudept_hbpudept(request: Request, room: str, query_db: AsyncSession = Depends(get_db)):
    hbpudept_detail_result = await HbpudeptService.hbpudept_detail_services_by_room(query_db, room)
    logger.info(f'获取room为{room}的信息成功')

    return ResponseUtil.success(data=hbpudept_detail_result)