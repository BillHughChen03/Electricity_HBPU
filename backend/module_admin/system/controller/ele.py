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
    ElectricityPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

electricityController = APIRouter(prefix='/ele/ele', dependencies=[Depends(LoginService.get_current_user)])



