import json
from datetime import datetime

from fastapi import APIRouter, Depends, Form, Request
from fastapi import status
from pydantic import BaseModel
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_admin.system.entity.vo.hbpuuser_vo import DeleteHbpuuserModel, HbpuuserModel, HbpuuserPageQueryModel
from module_admin.system.hbpu_utils.hbpu_auth_utils import HupuLogin
from module_admin.system.hbpu_utils.hbpu_electricity_utils import GetElectricityData
from module_admin.system.service.hbpuuser_service import HbpuuserService
from module_admin.system.utils.wx_send import sc_send
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

hbpuuserController = APIRouter(prefix='/hbpuuser/hbpuuser')


@hbpuuserController.get('/getwxpushlist')
@Log(title='湖北理工用户', business_type=BusinessType.EXPORT)
async def wxpushlist(
        request: Request,
        query_db: AsyncSession = Depends(get_db)
):
    try:
        users , num = await HbpuuserService.hbpuuser_detail_services_by_pushkey(query_db)
        return ResponseUtil.success(msg={"data": users, "total": num})

    except Exception as e:
        logger.error(f"失败: {e}", exc_info=True)
        return ResponseUtil.failure(msg=f"操作失败：{str(e)}")


@hbpuuserController.get('/list', response_model=PageResponseModel)
async def get_hbpuuser_hbpuuser_list(
        request: Request,
        hbpuuser_page_query: HbpuuserPageQueryModel = Depends(HbpuuserPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    hbpuuser_page_query_result = await HbpuuserService.get_hbpuuser_list_services(query_db, hbpuuser_page_query,
                                                                                  is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=hbpuuser_page_query_result)


@hbpuuserController.post('')
@ValidateFields(validate_model='add_hbpuuser')
@Log(title='湖北理工用户', business_type=BusinessType.INSERT)
async def add_hbpuuser_hbpuuser(
        request: Request,
        add_hbpuuser: HbpuuserModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_hbpuuser_result = await HbpuuserService.add_hbpuuser_services(query_db, add_hbpuuser)
    logger.info(add_hbpuuser_result.message)

    return ResponseUtil.success(msg=add_hbpuuser_result.message)


@hbpuuserController.put('')
@ValidateFields(validate_model='edit_hbpuuser')
@Log(title='湖北理工用户', business_type=BusinessType.UPDATE)
async def edit_hbpuuser_hbpuuser(
        request: Request,
        edit_hbpuuser: HbpuuserModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_hbpuuser.update_by = current_user.user.user_name
    edit_hbpuuser.update_time = datetime.now()
    edit_hbpuuser_result = await HbpuuserService.edit_hbpuuser_services(query_db, edit_hbpuuser)
    logger.info(edit_hbpuuser_result.message)

    return ResponseUtil.success(msg=edit_hbpuuser_result.message)


@hbpuuserController.delete('/{uids}')
@Log(title='湖北理工用户', business_type=BusinessType.DELETE)
async def delete_hbpuuser_hbpuuser(request: Request, uids: str, query_db: AsyncSession = Depends(get_db)):
    delete_hbpuuser = DeleteHbpuuserModel(uids=uids)
    delete_hbpuuser_result = await HbpuuserService.delete_hbpuuser_services(query_db, delete_hbpuuser)
    logger.info(delete_hbpuuser_result.message)

    return ResponseUtil.success(msg=delete_hbpuuser_result.message)


@hbpuuserController.get(
    '/{uid}', response_model=HbpuuserModel
)
async def query_detail_hbpuuser_hbpuuser(request: Request, uid: int, query_db: AsyncSession = Depends(get_db)):
    hbpuuser_detail_result = await HbpuuserService.hbpuuser_detail_services(query_db, uid)
    logger.info(f'获取uid为{uid}的信息成功')

    return ResponseUtil.success(data=hbpuuser_detail_result)


@hbpuuserController.post('/export')
@Log(title='湖北理工用户', business_type=BusinessType.EXPORT)
async def export_hbpuuser_hbpuuser_list(
        request: Request,
        hbpuuser_page_query: HbpuuserPageQueryModel = Form(),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    hbpuuser_query_result = await HbpuuserService.get_hbpuuser_list_services(query_db, hbpuuser_page_query,
                                                                             is_page=False)
    hbpuuser_export_result = await HbpuuserService.export_hbpuuser_list_services(hbpuuser_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(hbpuuser_export_result))


class EcardVerifyRequest(BaseModel):
    ecardUsername: str
    ecardPassword: str


@hbpuuserController.post('/ecardverify')
@Log(title='湖北理工用户', business_type=BusinessType.EXPORT)
async def getecardinfo(
        request: Request,  # ✅ 添加 FastAPI 的 Request 对象
        payload: EcardVerifyRequest,
        query_db: AsyncSession = Depends(get_db)
):
    ecardUsername = payload.ecardUsername
    ecardPassword = payload.ecardPassword
    try:
        access_token, token_type, refresh_token, sno, name = HupuLogin(ecardUsername, ecardPassword)
        response_data = {
            "access_token": access_token,
            "token_type": token_type,
            "refresh_token": refresh_token,
            "sno": sno,
            "name": name
        }
        # 构造返回的 JSON 数据
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "登录成功",
            "data": response_data
        }
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    except Exception as e:
        raw_message = getattr(e, 'message', str(e))

        try:
            # 提取嵌套 JSON 部分
            json_str_start = raw_message.find('{')
            json_data = json.loads(raw_message[json_str_start:])

            # 使用 JSON 中的字段填充 response body
            error_code = json_data.get('code', 500)
            error_message = json_data.get('message', '发生未知错误')
            http_status = json_data.get('status', 500)  # 用于 HTTP 返回状态码

        except Exception:
            error_code = getattr(e, 'status', 500)
            error_message = raw_message
            http_status = 500

        error_response = {
            "code": http_status,  # 例如 400
            "message": error_message  # 例如 "用户名或密码错误"
        }

        return JSONResponse(content=error_response, status_code=http_status)


class SaveSendKey(BaseModel):
    uid: int
    sendkey: str


@hbpuuserController.post('/savekey')
@Log(title='湖北理工用户', business_type=BusinessType.EXPORT)
async def savesendKey(
        request: Request,
        payload: SaveSendKey,
        query_db: AsyncSession = Depends(get_db)
):
    sendkey = payload.sendkey
    uid = payload.uid
    try:
        existing_user = await HbpuuserService.hbpuuser_detail_services2(query_db, uid)

        if existing_user:
            # 如果存在，则更新现有记录
            existing_user.sendky = sendkey
            update_result = await HbpuuserService.edit_hbpuuser_services(query_db, existing_user)
            logger.info(f"用户信息更新成功：{update_result.message}")
            return ResponseUtil.success(msg=update_result.message)
    except Exception as e:
        logger.error(f"保存用户信息失败: {e}", exc_info=True)
        return ResponseUtil.failure(msg=f"操作失败：{str(e)}")


class SaveWays(BaseModel):
    uid: int
    pushkey: str


@hbpuuserController.post('/saveways')
@Log(title='湖北理工用户', business_type=BusinessType.EXPORT)
async def savesendKey(
        request: Request,
        payload: SaveWays,
        query_db: AsyncSession = Depends(get_db)
):
    pushkey = payload.pushkey
    uid = payload.uid
    try:
        existing_user = await HbpuuserService.hbpuuser_detail_services2(query_db, uid)

        if existing_user:
            # 如果存在，则更新现有记录
            existing_user.pushkey = pushkey
            update_result = await HbpuuserService.edit_hbpuuser_services(query_db, existing_user)
            logger.info(f"用户信息更新成功：{update_result.message}")
            return ResponseUtil.success(msg=update_result.message)
    except Exception as e:
        logger.error(f"保存用户信息失败: {e}", exc_info=True)
        return ResponseUtil.failure(msg=f"操作失败：{str(e)}")


class SendTestBase(BaseModel):
    sendky: str


@hbpuuserController.post('/sendtest')
@Log(title='湖北理工用户', business_type=BusinessType.EXPORT)
async def SendTest(
        request: Request,
        payload: SendTestBase,
        query_db: AsyncSession = Depends(get_db)
):
    key = payload.sendky
    try:
        ret = sc_send(key, '电力系统推送测试！', '看到这里说明成功啦！')
        return ResponseUtil.success(msg=ret)
    except Exception as e:
        logger.error(f"发送失败: {e}", exc_info=True)
        return ResponseUtil.failure(msg=f"操作失败：{str(e)}")


class EcardVerifyRequest1(BaseModel):
    ecardUsername: str
    ecardPassword: str
    uid: int


@hbpuuserController.post('/ecardsave')
@Log(title='湖北理工用户', business_type=BusinessType.EXPORT)
async def getecardinfo(
        request: Request,
        payload: EcardVerifyRequest1,
        query_db: AsyncSession = Depends(get_db)
):
    ecardUsername = payload.ecardUsername
    ecardPassword = payload.ecardPassword
    uid = payload.uid

    try:
        # 登录获取 token 和其他信息
        access_token, token_type, refresh_token, sno, name = HupuLogin(ecardUsername, ecardPassword)

        # 查询是否已存在该 uid 的用户
        existing_user = await HbpuuserService.hbpuuser_detail_services2(query_db, uid)

        if existing_user:
            # 如果存在，则更新现有记录
            existing_user.husername = ecardUsername
            existing_user.hpassword = ecardPassword
            existing_user.access_token = access_token
            existing_user.token_type = token_type
            existing_user.refresh_token = refresh_token
            existing_user.sno = sno
            existing_user.name = name
            existing_user.token_time = datetime.now()

            update_result = await HbpuuserService.edit_hbpuuser_services(query_db, existing_user)
            logger.info(f"用户信息更新成功：{update_result.message}")
            return ResponseUtil.success(msg=update_result.message)
        else:
            # 如果不存在，则新增用户
            hbpuuser_model = HbpuuserModel(
                uid=uid,
                husername=ecardUsername,
                hpassword=ecardPassword,
                token_time=datetime.utcnow()
            )

            # 逐个赋值
            access_token, token_type, refresh_token, sno, name = HupuLogin(ecardUsername, ecardPassword)

            if access_token is None:
                print("获取失败")
            else:
                print("获取成功")

            hbpuuser_model.access_token = access_token
            hbpuuser_model.token_type = token_type
            hbpuuser_model.refresh_token = refresh_token
            hbpuuser_model.sno = sno
            hbpuuser_model.name = name
            hbpuuser_model.token_time = datetime.now()

            print("最终hbpuuser_model:", hbpuuser_model.model_dump(by_alias=False))

            add_hbpuuser_result = await HbpuuserService.add_hbpuuser_services(query_db, hbpuuser_model)
            logger.info(f"新增用户成功：{add_hbpuuser_result.message}")
            return ResponseUtil.success(msg=add_hbpuuser_result.message)

    except Exception as e:
        logger.error(f"保存用户信息失败: {e}", exc_info=True)
        return ResponseUtil.failure(msg=f"操作失败：{str(e)}")


class RoomBindRequest(BaseModel):
    uid: int
    building: str
    room: str


@hbpuuserController.post('/bind_room')
@Log(title='绑定寝室信息', business_type=BusinessType.UPDATE)
async def bind_room(
        request: Request,
        payload: RoomBindRequest,
        query_db: AsyncSession = Depends(get_db)
):
    try:
        result = await HbpuuserService.bind_room_info(query_db, payload.uid, payload.building, payload.room)
        return ResponseUtil.success(data=result, msg="寝室信息绑定成功")

    except Exception as e:
        await query_db.rollback()
        return ResponseUtil.error(msg=f"绑定失败：{str(e)}")


@hbpuuserController.post('/getfee')
@Log(title='绑定寝室信息', business_type=BusinessType.EXPORT)
async def room_fee(
        request: Request,
        payload: RoomBindRequest,
        query_db: AsyncSession = Depends(get_db)
):
    try:
        result = await HbpuuserService.hbpuuser_detail_services(query_db, payload.uid)
        if result:
            access_token = result.access_token
            token_type = result.token_type
            building = payload.building
            room = payload.room
            total_electricity, remaining_electricity, building_name, room_name, finish_time, campus = GetElectricityData(
                access_token,
                token_type, building,
                room)
            response_data = {
                "total_electricity": total_electricity,
                "remaining_electricity": remaining_electricity,
                "building_name": building_name,
                "room_name": room_name,
                "finish_time": finish_time,
                "campus": campus
            }
            # 构造返回的 JSON 数据
            response = {
                "code": status.HTTP_200_OK,
                "message": "查询成功",
                "data": response_data
            }
            return JSONResponse(content=response, status_code=status.HTTP_200_OK)

    except Exception as e:
        error_response = {
            "code": 400,  # 例如 400
            "message": str(e)
        }
        return JSONResponse(content=error_response, status_code=status.HTTP_400_BAD_REQUEST)


