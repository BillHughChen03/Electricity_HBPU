import requests
import time


# 内部类，不对外暴露
class _ElectricityUtils:
    def __init__(self, electricity_url):
        self.electricity_url = electricity_url

    def get_electricity_data(self, access_token, token_type, building, room):
        """获取电费信息"""
        # 确保所有参数都是字符串类型
        access_token = str(access_token)
        token_type = str(token_type)
        building = str(building)
        room = str(room)

        headers = {
            "Authorization": "Basic Y2hhcmdlOmNoYXJnZV9zZWNyZXQ=",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://ecard.hbpu.edu.cn",
            "Referer": "https://ecard.hbpu.edu.cn/charge-app/",
            "synjones-auth": f"{token_type} {access_token}"
        }
        data = f"feeitemid=221&type=IEC&level=3&campus=1-sh&building={building}&room={room}"
        response = requests.post(self.electricity_url, headers=headers, data=data)

        if response.status_code == 200:
            return response.json()
        else:
            response_data = response.json()
            text = response_data.get("message")
            raise ValueError(f"获取电费信息失败，状态码：{response.status_code}，响应内容：{text}")


class _ElectricityUtils2:
    def __init__(self, electricity_url):
        self.electricity_url = electricity_url

    def get_electricity_data(self, access_token, token_type, building, room):
        """获取电费信息"""
        # 确保所有参数都是字符串类型
        access_token = str(access_token)
        token_type = str(token_type)
        building = str(building)
        room = str(room)

        headers = {
            "Authorization": "Basic Y2hhcmdlOmNoYXJnZV9zZWNyZXQ=",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://ecard.hbpu.edu.cn",
            "Referer": "https://ecard.hbpu.edu.cn/charge-app/",
            "synjones-auth": f"{token_type} {access_token}"
        }
        data = f"feeitemid=221&type=IEC&level=3&campus=1-sh&building={building}&room={room}"
        response = requests.post(self.electricity_url, headers=headers, data=data)

        if response.status_code == 200:
            return response.json()
        else:
            response_data = response.json()
            text = response_data.get("message")
            if text == "已经在其他设备登录":
                raise ValueError("别处登录")
            else:
                ValueError(f"获取电费信息失败，状态码：{response.status_code}，响应内容：{text}")


# 对外暴露的函数
def GetElectricityData(access_token, token_type, building, room):
    """
    获取电费信息
    :param access_token: 访问令牌
    :param token_type: 令牌类型（如 'bearer'）
    :param building: 楼栋号
    :param room: 房间号
    :return: 提取的关键信息，失败时抛出异常
    """
    electricity_url = "https://ecard.hbpu.edu.cn/charge/feeitem/getThirdData"
    electricity_utils = _ElectricityUtils(electricity_url)
    try:
        response_data = electricity_utils.get_electricity_data(access_token, token_type, building, room)
        # 提取关键信息
        total_electricity = response_data.get("map", {}).get("showData", {}).get("电表总用电量")
        remaining_electricity = response_data.get("map", {}).get("showData", {}).get("当前剩余电量")
        building_name = response_data.get("map", {}).get("data", {}).get("building")
        room_name = response_data.get("map", {}).get("data", {}).get("room")
        campus = response_data.get("map", {}).get("data", {}).get("campus")
        finish_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        return total_electricity, remaining_electricity, building_name, room_name, finish_time, campus
    except Exception as e:
        raise e


def GetElectricityData2(access_token, token_type, building, room):
    """
    获取电费信息
    :param access_token: 访问令牌
    :param token_type: 令牌类型（如 'bearer'）
    :param building: 楼栋号
    :param room: 房间号
    :return: 提取的关键信息，失败时抛出异常
    """
    electricity_url = "https://ecard.hbpu.edu.cn/charge/feeitem/getThirdData"
    electricity_utils = _ElectricityUtils2(electricity_url)
    try:
        response_data = electricity_utils.get_electricity_data(access_token, token_type, building, room)
        # 提取关键信息
        total_electricity = response_data.get("map", {}).get("showData", {}).get("电表总用电量")
        remaining_electricity = response_data.get("map", {}).get("showData", {}).get("当前剩余电量")
        building_name = response_data.get("map", {}).get("data", {}).get("building")
        room_name = response_data.get("map", {}).get("data", {}).get("room")
        campus = response_data.get("map", {}).get("data", {}).get("campus")
        finish_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        return total_electricity, remaining_electricity, building_name, room_name, finish_time, campus
    except Exception as e:
        raise e


# 使用示例
# if __name__ == "__main__":
#     try:
#         access_token = "..."
#         token_type = "bearer"
#         building = 9  # 传入数字类型
#         room = 12215  # 传入数字类型
#         total_electricity, remaining_electricity, building_name, room_name, finish_time, campus = GetElectricityData2(
#             access_token,
#             token_type, building,
#             room)
#         print(f"电表总用电量: {total_electricity}")
#         print(f"当前剩余电量: {remaining_electricity}")
#         print(f"校区: {campus}")
#         print(f"楼栋: {building_name}")
#         print(f"房间: {room_name}")
#         print(f"完成时间: {finish_time}")
#     except Exception as e:
#         print(f"获取电费信息失败：{e}")
