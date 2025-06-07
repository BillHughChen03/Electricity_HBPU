from datetime import datetime

from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_admin.system.service.electricity_service import ElectricityService
from module_admin.system.entity.vo.electricity_vo import DeleteElectricityModel, ElectricityModel, \
    ElectricityPageQueryModel, ElectricityQueryModel2
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

electricityController = APIRouter(prefix='/hbpuelectricity/electricity',
                                  dependencies=[Depends(LoginService.get_current_user)])


@electricityController.get(
    '/list', response_model=PageResponseModel,
)
async def get_hbpuelectricity_electricity_list(
        request: Request,
        electricity_page_query: ElectricityPageQueryModel = Depends(ElectricityPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    electricity_page_query_result = await ElectricityService.get_electricity_list_services(query_db,
                                                                                           electricity_page_query,
                                                                                           is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=electricity_page_query_result)


@electricityController.post('')
@ValidateFields(validate_model='add_electricity')
@Log(title='电力', business_type=BusinessType.INSERT)
async def add_hbpuelectricity_electricity(
        request: Request,
        add_electricity: ElectricityModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_electricity_result = await ElectricityService.add_electricity_services(query_db, add_electricity)
    logger.info(add_electricity_result.message)

    return ResponseUtil.success(msg=add_electricity_result.message)


@electricityController.put('')
@ValidateFields(validate_model='edit_electricity')
@Log(title='电力', business_type=BusinessType.UPDATE)
async def edit_hbpuelectricity_electricity(
        request: Request,
        edit_electricity: ElectricityModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_electricity.update_by = current_user.user.user_name
    edit_electricity.update_time = datetime.now()
    edit_electricity_result = await ElectricityService.edit_electricity_services(query_db, edit_electricity)
    logger.info(edit_electricity_result.message)

    return ResponseUtil.success(msg=edit_electricity_result.message)


@electricityController.delete('/{info_ids}')
@Log(title='电力', business_type=BusinessType.DELETE)
async def delete_hbpuelectricity_electricity(request: Request, info_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_electricity = DeleteElectricityModel(infoIds=info_ids)
    delete_electricity_result = await ElectricityService.delete_electricity_services(query_db, delete_electricity)
    logger.info(delete_electricity_result.message)

    return ResponseUtil.success(msg=delete_electricity_result.message)


@electricityController.get(
    '/{info_id}', response_model=ElectricityModel
)
async def query_detail_hbpuelectricity_electricity(request: Request, info_id: int,
                                                   query_db: AsyncSession = Depends(get_db)):
    electricity_detail_result = await ElectricityService.electricity_detail_services(query_db, info_id)
    logger.info(f'获取info_id为{info_id}的信息成功')

    return ResponseUtil.success(data=electricity_detail_result)


@electricityController.post('/export')
@Log(title='电力', business_type=BusinessType.EXPORT)
async def export_hbpuelectricity_electricity_list(
        request: Request,
        electricity_page_query: ElectricityPageQueryModel = Form(),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    electricity_query_result = await ElectricityService.get_electricity_list_services(query_db, electricity_page_query,
                                                                                      is_page=False)
    electricity_export_result = await ElectricityService.export_electricity_list_services(electricity_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(electricity_export_result))


@electricityController.get('/room/list')
async def get_electricity_room_list(
        request: Request,
        campus: str = None,
        building: str = None,
        room: str = None,
        start_time: str = None,
        end_time: str = None,
        db: AsyncSession = Depends(get_db)
):
    electricity_list = await ElectricityService.get_electricity_data(
        db, campus, building, room, start_time, end_time
    )

    result = {
        "total": len(electricity_list),
        "list": [
            {
                "infoId": e.info_id,
                "total": e.total,
                "remaining": e.remaining,
                "campus": e.campus,
                "buildingName": e.building_name,
                "roomName": e.room_name,
                "building": e.building,
                "room": e.room,
                "finishTime": e.finish_time,
                "yesterdayRemaining": e.yesterday_remaining
            }
            for e in electricity_list
        ]
    }
    return ResponseUtil.success(result)
