import requests
import base64


# 内部类，不对外暴露
class _AuthUtils:
    def __init__(self, auth_url, client_id, client_secret):
        self.auth_url = auth_url
        self.client_id = client_id
        self.client_secret = client_secret

    def login(self, username, password):
        """登录并获取令牌"""
        client_auth = f"{self.client_id}:{self.client_secret}"
        encoded_auth = base64.b64encode(client_auth.encode()).decode()

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {encoded_auth}"
        }
        data = f"username={username}&password={password}&grant_type=password&scope=all&loginFrom=app&logintype=sno&synAccessSource=app"
        response = requests.post(self.auth_url, headers=headers, data=data)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"登录失败，状态码：{response.status_code}，响应内容：{response.text}")

    def refresh_token(self, refresh_token):
        """使用刷新令牌续签"""
        client_auth = f"{self.client_id}:{self.client_secret}"
        encoded_auth = base64.b64encode(client_auth.encode()).decode()

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {encoded_auth}"
        }
        data = f"refresh_token={refresh_token}&grant_type=refresh_token&scope=all&loginFrom=app&logintype=sno&synAccessSource=app"
        response = requests.post(self.auth_url, headers=headers, data=data)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"续签失败，状态码：{response.status_code}，响应内容：{response.text}")


# 对外暴露的函数
def HupuLogin(id, password):
    """
    登录湖北理工系统并获取令牌
    :param id: 用户名（可以是数字或字符串）
    :param password: 密码
    :return: 登录成功返回 (access_token, token_type, refresh_token, sno, name)，登录失败抛出异常
    """
    # 确保 id 是字符串类型
    if not isinstance(id, str):
        id = str(id)

    auth_url = "https://ecard.hbpu.edu.cn/berserker-auth/oauth/token"
    client_id = "mobile_service_platform"
    client_secret = "mobile_service_platform_secret"

    auth_utils = _AuthUtils(auth_url, client_id, client_secret)
    try:
        response_data = auth_utils.login(id, password)
        # 提取关键信息
        access_token = response_data.get("access_token")
        token_type = response_data.get("token_type")
        refresh_token = response_data.get("refresh_token")
        sno = response_data.get("sno")
        name = response_data.get("name")
        return access_token, token_type, refresh_token, sno, name
    except Exception as e:
        print(f"发生错误：{e}")
        raise e


# 对外暴露的续签函数
def HupuRefreshToken(refresh_token):
    """
    使用刷新令牌续签
    :param refresh_token: 刷新令牌
    :return: 续签成功返回 (access_token, token_type, refresh_token, sno, name)，续签失败抛出异常
    """
    auth_url = "https://ecard.hbpu.edu.cn/berserker-auth/oauth/token"
    client_id = "mobile_service_platform"
    client_secret = "mobile_service_platform_secret"

    auth_utils = _AuthUtils(auth_url, client_id, client_secret)
    try:
        response_data = auth_utils.refresh_token(refresh_token)
        # 提取关键信息
        access_token = response_data.get("access_token")
        token_type = response_data.get("token_type")
        refresh_token = response_data.get("refresh_token")
        sno = response_data.get("sno")
        name = response_data.get("name")
        return access_token, token_type, refresh_token, sno, name
    except Exception as e:
        if isinstance(e, requests.exceptions.RequestException):
            raise Exception(f"网络请求失败，错误信息：{e}")
        elif isinstance(e, Exception):
            error_message = str(e)
            if "暂无承载数据" in error_message:
                raise Exception("续签失败，可能是刷新令牌无效或过期。")
            else:
                raise Exception(f"续签失败，错误信息：{error_message}")

# 使用示例
# if __name__ == "__main__":
#     try:
#         access_token, token_type, refresh_token, sno, name = HupuLogin(学号, 密码)
#         print(f"Access Token: {access_token}")
#         print(f"Token Type: {token_type}")
#         print(f"Refresh Token: {refresh_token}")
#         print(f"SNO: {sno}")
#         print(f"Name: {name}")
#     except Exception as e:
#         print(f"登录失败：{e}")

# if __name__ == "__main__":
#     refresh_token = "..."
#     try:
#         # 使用刷新令牌进行续签
#         new_access_token, new_token_type, new_refresh_token, new_sno, new_name = HupuRefreshToken(refresh_token)
#         print(f"续签成功！")
#         print(f"新的 Access Token: {new_access_token}")
#         print(f"新的 Token Type: {new_token_type}")
#         print(f"新的 Refresh Token: {new_refresh_token}")
#         print(f"学号: {new_sno}")
#         print(f"姓名: {new_name}")
#
#     except Exception as e:
#         print(f"发生错误：{e}")
