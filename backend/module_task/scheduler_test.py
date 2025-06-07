import asyncio
import logging
import random
from datetime import datetime
from time import sleep

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.get_db import get_db
from module_admin.system.dao.hbpuuser_dao import HbpuuserDao
from module_admin.system.dao.electricity_dao import ElectricityDao

from module_admin.system.hbpu_utils.hbpu_auth_utils import HupuLogin
from module_admin.system.hbpu_utils.hbpu_electricity_utils import GetElectricityData2
from module_admin.system.utils.wx_send import sc_send


def job(*args, **kwargs):
    """
    定时任务执行同步函数示例
    """
    print(args)
    print(kwargs)
    print(f'{datetime.now()}同步函数执行了')


async def async_job(*args, **kwargs):
    """
    定时任务执行异步函数示例
    """
    print(args)
    print(kwargs)
    print(f'{datetime.now()}异步函数执行了')


#
# async def run_fee_send(*args, **kwargs):
#     print(args)
#     print(kwargs)
#     print(f'{datetime.now()}异步函数执行了')
#     """
#     异步函数，用于处理电费查询和推送通知。
#     """
#     async for query_db in get_db():
#         # 获取用户数据列表和总人数
#         users = await HbpuuserDao.get_hbpuuser_detail_by_pushkey(query_db)
#         num = len(users)
#
#         # 遍历每个用户
#         for i in range(num):
#             # 解包每一行数据
#             index, uid, husername, hpassword, access_token, building, room, sendky, token_type = users[i]
#             print(
#                 f"第{index}个用户：Uid={uid}, 用户名={husername}, 密码={hpassword}, token={access_token}, 楼栋={building}, 房间={room}, sendky={sendky}, tokenType={token_type}")
#
#             try:
#                 random_seconds = random.uniform(0.5, 2.0)  # 生成0.5到2.0之间的随机浮点数
#                 print(f"随机暂停时间：{random_seconds} 秒")
#                 await asyncio.sleep(random_seconds)  # 非阻塞式暂停指定时间
#
#                 # 查询电量数据
#                 total_electricity, remaining_electricity, building_name, room_name, finish_time, campus = GetElectricityData2(
#                     access_token, token_type, building, room
#                 )
#
#                 # 查询昨日电量数据
#                 remaining_yesterday = await ElectricityDao.get_latest_remaining_by_room(query_db, room)
#                 remaining_yesterday = str(remaining_yesterday)
#                 var = float(remaining_yesterday) - float(remaining_electricity)
#                 var = f"{var:.2f}"
#
#                 # 插入最新一条数据
#                 await ElectricityDao.add_electricity_by_room(
#                     query_db,
#                     total=total_electricity,
#                     remaining=remaining_electricity,
#                     campus=campus,
#                     building_name=building_name,
#                     room_name=room_name,
#                     building=building,
#                     room=room,
#                     finish_time=datetime.now(),
#                     yesterday_remaining=remaining_yesterday
#                 )
#
#                 # 推送数据
#                 ret = sc_send(sendky, f"剩余电量 {remaining_electricity}",
#                               f"当前剩余电量: {remaining_electricity}\n\n" +
#                               f"昨日剩余电量: {remaining_yesterday}\n\n" +
#                               f"使用电量: {var}\n\n" +
#                               f"完成时间: {finish_time}")
#                 code = ret.get("code")
#
#                 print(f"发送状态码: {code}")
#                 if code == 0:
#                     print("推送成功")
#                     logging.info(f"{husername} 查询成功，并发送成功。")
#                 else:
#                     msg = ret.get("message")
#                     print("推送失败")
#                     logging.warning(f"{husername} 查询成功，但推送失败：{msg}")
#
#             except Exception as e:
#                 e_str = str(e)
#                 print(f"{husername} 处理异常：{e_str}")
#                 logging.error(f"{husername} 查询失败，异常信息：{e_str}")
#
#                 # 检查是否是“别处登录”异常
#                 if "别处登录" in e_str:
#                     try:
#                         random_seconds = random.uniform(0.5, 1.0)  # 生成0.5到2.0之间的随机浮点数
#                         print(f"随机暂停时间：{random_seconds} 秒")
#                         await asyncio.sleep(random_seconds)  # 非阻塞式暂停指定时间
#
#                         # 刷新 access_token
#                         access_token, token_type, refresh_token, sno, name = HupuLogin(husername, hpassword)
#                         # 再尝试一次查询与推送
#                         try:
#                             total_electricity, remaining_electricity, building_name, room_name, finish_time, campus = GetElectricityData2(
#                                 access_token, token_type, building, room
#                             )
#
#                             remaining_yesterday = await ElectricityDao.get_latest_remaining_by_room(query_db, room)
#                             remaining_yesterday = str(remaining_yesterday)
#                             var = float(remaining_yesterday) - float(remaining_electricity)
#                             var = f"{var:.2f}"
#
#                             # 插入最新一条数据
#                             await ElectricityDao.add_electricity_by_room(
#                                 query_db,
#                                 total=total_electricity,
#                                 remaining=remaining_electricity,
#                                 campus=campus,
#                                 building_name=building_name,
#                                 room_name=room_name,
#                                 building=building,
#                                 room=room,
#                                 finish_time=datetime.now(),
#                                 yesterday_remaining=remaining_yesterday
#                             )
#
#                             await HbpuuserDao.update_token_info_by_uid(query_db, uid, access_token, refresh_token)
#
#                             # 推送数据
#                             ret = sc_send(sendky, f"剩余电量 {remaining_electricity}",
#                                           f"当前剩余电量: {remaining_electricity}\n\n" +
#                                           f"昨日剩余电量: {remaining_yesterday}\n\n" +
#                                           f"使用电量: {var}\n\n" +
#                                           f"完成时间: {finish_time}")
#
#                             code = ret.get("code")
#                             if code == 0:
#                                 print("推送成功（刷新后）")
#                                 logging.info(f"{husername} 刷新后查询并推送成功。")
#                             else:
#                                 msg = ret.get("message", "未知错误")
#                                 print("推送失败（刷新后）")
#                                 logging.warning(f"{husername} 刷新后推送失败：{msg}")
#                         except Exception as e2:
#                             print(f"{husername} 刷新后仍失败：{e2}")
#                             logging.error(f"{husername} 刷新后仍失败：{e2}")
#                             continue  # 跳过当前用户
#                     except Exception as login_err:
#                         print(f"{husername} 登录失败，跳过：{login_err}")
#                         logging.error(f"{husername} 登录失败，跳过：{login_err}")
#                         continue
#                 else:
#                     continue

async def run_fee_send(*args, **kwargs):
    print(args)
    print(kwargs)
    print(f'{datetime.now()}异步函数执行了')
    """
    异步函数，用于处理电费查询和推送通知。
    """
    async for query_db in get_db():
        # 获取用户数据列表和总人数
        users = await HbpuuserDao.get_hbpuuser_detail_by_pushkey(query_db)
        num = len(users)

        # 遍历每个用户
        for i in range(num):
            # 解包每一行数据
            index, uid, husername, hpassword, access_token, building, room, sendky, token_type = users[i]
            print(
                f"第{index}个用户：Uid={uid}, 用户名={husername}, 密码={hpassword}, token={access_token}, 楼栋={building}, 房间={room}, sendky={sendky}, tokenType={token_type}")

            try:
                random_seconds = random.uniform(0.5, 2.0)  # 生成0.5到2.0之间的随机浮点数
                print(f"随机暂停时间：{random_seconds} 秒")
                await asyncio.sleep(random_seconds)  # 非阻塞式暂停指定时间

                # 查询电量数据
                total_electricity, remaining_electricity, building_name, room_name, finish_time, campus = GetElectricityData2(
                    access_token, token_type, building, room
                )

                # 查询昨日电量数据
                remaining_yesterday = await ElectricityDao.get_latest_remaining_by_room(query_db, room)
                remaining_yesterday = str(remaining_yesterday)
                var = float(remaining_yesterday) - float(remaining_electricity)
                var = f"{var:.2f}"

                # 插入最新一条数据
                await ElectricityDao.add_electricity_by_room(
                    query_db,
                    total=total_electricity,
                    remaining=remaining_electricity,
                    campus=campus,
                    building_name=building_name,
                    room_name=room_name,
                    building=building,
                    room=room,
                    finish_time=datetime.now(),
                    yesterday_remaining=remaining_yesterday
                )

                # 推送数据
                ret = sc_send(sendky, f"剩余电量 {remaining_electricity}",
                              f"当前剩余电量: {remaining_electricity}\n\n" +
                              f"昨日剩余电量: {remaining_yesterday}\n\n" +
                              f"使用电量: {var}\n\n" +
                              f"完成时间: {finish_time}")
                code = ret.get("code")

                print(f"发送状态码: {code}")
                if code == 0:
                    print("推送成功")
                    logging.info(f"{husername} 查询成功，并发送成功。")
                else:
                    msg = ret.get("message")
                    print("推送失败")
                    logging.warning(f"{husername} 查询成功，但推送失败：{msg}")

            except Exception as e:
                e_str = str(e)
                print(f"{husername} 处理异常：{e_str}")
                logging.error(f"{husername} 查询失败，异常信息：{e_str}")

                # 尝试重新获取access_token并重试（适用于所有异常）
                try:
                    random_seconds = random.uniform(0.5, 1.0)  # 生成0.5到1.0之间的随机浮点数
                    print(f"随机暂停时间：{random_seconds} 秒")
                    await asyncio.sleep(random_seconds)  # 非阻塞式暂停指定时间

                    # 刷新 access_token
                    print(f"{husername} 尝试重新获取access_token...")
                    access_token, token_type, refresh_token, sno, name = HupuLogin(husername, hpassword)

                    # 再尝试一次查询与推送
                    try:
                        total_electricity, remaining_electricity, building_name, room_name, finish_time, campus = GetElectricityData2(
                            access_token, token_type, building, room
                        )

                        remaining_yesterday = await ElectricityDao.get_latest_remaining_by_room(query_db, room)
                        remaining_yesterday = str(remaining_yesterday)
                        var = float(remaining_yesterday) - float(remaining_electricity)
                        var = f"{var:.2f}"

                        # 插入最新一条数据
                        await ElectricityDao.add_electricity_by_room(
                            query_db,
                            total=total_electricity,
                            remaining=remaining_electricity,
                            campus=campus,
                            building_name=building_name,
                            room_name=room_name,
                            building=building,
                            room=room,
                            finish_time=datetime.now(),
                            yesterday_remaining=remaining_yesterday
                        )

                        # 更新数据库中的token信息
                        await HbpuuserDao.update_token_info_by_uid(query_db, uid, access_token, refresh_token)

                        # 推送数据
                        ret = sc_send(sendky, f"剩余电量 {remaining_electricity}",
                                      f"当前剩余电量: {remaining_electricity}\n\n" +
                                      f"昨日剩余电量: {remaining_yesterday}\n\n" +
                                      f"使用电量: {var}\n\n" +
                                      f"完成时间: {finish_time}")

                        code = ret.get("code")
                        if code == 0:
                            print("推送成功（重试后）")
                            logging.info(f"{husername} 重试后查询并推送成功。")
                        else:
                            msg = ret.get("message", "未知错误")
                            print("推送失败（重试后）")
                            logging.warning(f"{husername} 重试后推送失败：{msg}")

                    except Exception as e2:
                        print(f"{husername} 重试后仍失败：{e2}")
                        logging.error(f"{husername} 重试后仍失败：{e2}")
                        continue  # 跳过当前用户，进入下一用户

                except Exception as login_err:
                    print(f"{husername} 重新登录失败，跳过该用户：{login_err}")
                    logging.error(f"{husername} 重新登录失败，跳过该用户：{login_err}")
                    continue  # 跳过当前用户，进入下一用户
