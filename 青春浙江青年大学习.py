import json
import msvcrt
import re
import time
import webbrowser

import requests
from lxml import etree


# 获取token
# 使用微信固定的openid获取青春浙江一次性token
def get_token():
    timestamp = int(time.time())  # 获取时间戳

    response = requests.get(
        f'https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/login/we-chat/callback?callback=https%3A%2F%2Fqczj'
        f'.h5yunban.com%2Fqczj-youth-learning%2Findex.php&scope=snsapi_userinfo&appid=wx56b888a1409a2920&openid='
        f'{openid}&nickname=fuckqndxx&headimg=&time='
        f'{timestamp}&source=common&sign=380C5B891B88C955C6E4BD8A7A3E1FA1&t={timestamp}',
        headers=headers,
    )
    match = re.search(r"localStorage\.setItem\('accessToken',\s*'([^']+)'\);", response.text)  # 提取出token
    if match:
        token = match.group(1)
        print(f"{Color.GREEN}成功获取Token:{Color.RESET}", token)
        return token
    else:
        print(f"{Color.RED}获取Token失败{Color.RESET}")
        return None


# 获取当前期数编号
def serial_number():
    try:
        response = requests.get(
            'https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/common-api/course/current',
            params=params,
            headers=headers,
        )
        data = response.json()  # 使用 response.json() 解析 JSON 数据

        course_id = data['result']['id']  # 提取 "id" 字段的值

        # 打印结果
        print(f"{Color.GREEN}提取到的课程ID:{Color.RESET}", course_id)
        return course_id
    except json.JSONDecodeError as e:
        print(f"{Color.RED}JSON 解析错误:{Color.RESET} {e}")
        return None
    except KeyError as e:
        print(f"{Color.RED}未找到字段 'result' 或 'id':{Color.RESET} {e}")
        return None
    except Exception as e:
        print(f"{Color.RED}未知错误:{Color.RESET} {e}")
        return None


# 青春浙江学习签到
def to_study(course_id):
    json_data = {
        'course': course_id,
        "subOrg": None,
        'nid': nid,
        'cardNo': card,
    }

    response = requests.post(
        'https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/user-api/course/join',
        params=params,
        headers=headers,
        json=json_data,
    )
    print(f"{Color.GREEN}签到结果:{Color.RESET}", response.text)
    if response.status_code == 200 and response.json().get('status') == 200:
        print(f"{Color.GREEN}签到成功{Color.RESET}")
    else:
        print(f"{Color.RED}签到失败!{Color.RESET} ")


# 从青年大学习官网获取结尾图片地址
def get_screenshot_url():
    response = requests.get('https://m.cyol.com/gb/channels/vrGlAKDl/index.html', headers=headers)
    response_html = etree.HTML(response.text)
    href_list = response_html.xpath('/html/body/section[1]/div/ul//a/@href')
    if 'index.html' in href_list[0]:
        return href_list[0].replace("index.html", "images/end.jpg")
    elif 'm.html' in href_list[0]:
        return href_list[0].replace("m.html", "images/end.jpg")


# 定义字体颜色
class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'


# 退出函数
def exit_program():
    """退出程序的函数"""
    print("按任意键退出....")
    while True:
        msvcrt.getch()
        exit(0)


if __name__ == '__main__':
    print(f"""{Color.YELLOW}
    ███████╗██╗   ██╗ ██████╗██╗  ██╗          
    ██╔════╝██║   ██║██╔════╝██║ ██╔╝          
    █████╗  ██║   ██║██║     █████╔╝           
    ██╔══╝  ██║   ██║██║     ██╔═██╗           
    ██║     ╚██████╔╝╚██████╗██║  ██╗          
    ╚═╝      ╚═════╝  ╚═════╝╚═╝  ╚═╝          

     ██████╗ ███╗   ██╗██████╗ ██╗  ██╗██╗  ██╗
    ██╔═══██╗████╗  ██║██╔══██╗╚██╗██╔╝╚██╗██╔╝
    ██║   ██║██╔██╗ ██║██║  ██║ ╚███╔╝  ╚███╔╝ 
    ██║▄▄ ██║██║╚██╗██║██║  ██║ ██╔██╗  ██╔██╗ 
    ╚██████╔╝██║ ╚████║██████╔╝██╔╝ ██╗██╔╝ ██╗
     ╚══▀▀═╝ ╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
     {Color.RESET}
    ------------------------------------------------------------
                    FuckQndxx 0.6    by Ku-ru-mi
    ------------------------------------------------------------
    https://github.com/Ku-ru-mi/Qczj-Qndxx
      """)
    openid = ""  # 抓包获取
    nid = ""  # 团组织编号
    card = ""  # 姓名或学号
    """头文件，重复多的都放这了"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) '
                      'WindowsWechat(0x6309080f) XWEB/8519 Flue',
    }
    params = {
        'accessToken': get_token(),
    }

    to_study(course_id=serial_number())  # 签到
    screenshot_url = get_screenshot_url()  # 获取最新一期end图片
    print(f'{Color.GREEN}即将在一秒后打开浏览器{Color.RESET}{screenshot_url}')
    time.sleep(1)
    webbrowser.open(screenshot_url)  # 打开浏览器

    exit_program()
