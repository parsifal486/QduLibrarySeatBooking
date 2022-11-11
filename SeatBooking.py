from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
from time import sleep
from selenium.webdriver.support.ui import Select

# 时间检索器
now = datetime.datetime.now()
if now.hour != 7 or now.minute != 00:
    sleep(60)

# 预约信息
id = "2020205053"   # 此处填写学号信息
pw = "amazing"      # 密码
zone = 2            # 区域号 对应号码可在下方注释查找，当前为2，即浮山校区图书馆二楼
room = 2            # 房间号 对应号码可在下方注释中查找，当前为2，即为浮山校区图书馆二楼
seatNum_dig = 30    # 座位号，提前选好就行，注意不要选到因为疫情而暂停使用的座位
speed = 2           # 运行速度参数，不建议再调小了，如果网速较慢的话建议酌情调大2~3
startTime = 2150    # 开始时间前两位表示小时，后两位表示分钟，此处为21点50 注意：如果是7点的话前面不需要补0，直接改成 700 就可以
endTime = 2155      # 结束时间，格式要求同上，注意开始和结束的差不要超过6小时哦（预约最多每次6小时

'''
zone&room号码:
2:浮山校区图书馆二楼 1：B203 2:B204 3:B205 4:B206 5:二楼A区 6：二楼B区
3:浮山校区图书馆三楼 1:三楼A区 2:三楼B区 3:三楼大厅
4:金家岭校区图文中心一楼 1:一楼大厅
5:金家岭校区图文中心二楼 1:二楼大厅 52:208
6:金家岭校区图文中心三楼 1:三楼大厅 62:310
7:金家岭校区图文中心四楼 1:多媒体阅览室 2:411大自修室 3:411小自修室
'''

# 登录选项信息处理：将房间号,时间等数码转换为字符串
seatNum_str = str(seatNum_dig).zfill(3)
startTimeStr = str(startTime)
endTimeStr = str(endTime)

# 打开网页
browser = webdriver.Chrome(r'C:\apps\chromedriver\chromedriver.exe')
browser.get('http://authserver.qdu.edu.cn/authserver/login?service=http://csyy.qdu.edu.cn:8080/loginall.aspx')

# 自动填写账号密码并登录
idInput = browser.find_elements(By.ID, "username")
idInput[0].click()
idInput[0].send_keys(id)

pwInput = browser.find_elements(By.ID, "password")
pwInput[0].click()
pwInput[0].send_keys(pw)

confirm = browser.find_element(By.XPATH, '//*[@id="casLoginForm"]/div[4]/div/button')
confirm.click()

# 选取区域&座位
# 打开区域页面
zonePath = '//*[@id="item_list"]/ul/li[' + str(zone) + "]/a"
zoneSelect = browser.find_element(By.XPATH, zonePath)
zoneSelect.click()
sleep(0.2*speed)  # 此处埋坑，可以通过改进wait的方式来提高运行速度，speed为等待时间的速度因子，不建议k值设置过低，容易造成指令快于网页加载的情况

# 打开房间页面
roomPath = '//*[@id="item_list"]/ul/li[' + str(zone) + ']/ul/li[' + str(room) + ']'
roomSelect = browser.find_element(By.XPATH, roomPath)
roomSelect.click()
sleep(0.8*speed)

# 预约日期写入
dateList = browser.find_elements(By.CLASS_NAME, 'hasDatepicker')
dateList[0].click()
dateSelect = browser.find_elements(By.CSS_SELECTOR, '[data-handler="selectDay"]')
dateSelect[1].click()

# 重置时间
dateList[1].click()
timepicker = browser.find_elements(By.CLASS_NAME, 'ui-timepicker-select')
Select(timepicker[0]).select_by_value("7")
timepicker = browser.find_elements(By.CLASS_NAME, 'ui-timepicker-select')
Select(timepicker[1]).select_by_value("0")
dateList[2].click()
timepicker = browser.find_elements(By.CLASS_NAME, 'ui-timepicker-select')
Select(timepicker[0]).select_by_value("22")
timepicker = browser.find_elements(By.CLASS_NAME, 'ui-timepicker-select')
Select(timepicker[1]).select_by_value("0")
browser.find_element(By.CLASS_NAME, "ui-priority-primary").click()
sleep(0.8*speed)

# 选择座位（需要先找到区域号对应的字符串
zoneRoomDict = {21: 'B203', 22: 'B204', 23: 'B205', 24: 'B206', 25: '2F-A区自修区', 26: '2F-B区自修区',
                31: '3F-A区自修区', 32: '3F-B区自修区', 33: '3F-大厅自修区',
                41: '1F-大厅自修区',
                51: '2F-大厅自修区', 52: '208自修室',
                61: '金家岭3F大厅', 62: '301自修室',
                71: '408多媒体', 72: '411大自修室', 73: '411小自修室'}

zoneRoomStr = zoneRoomDict[zone*10+room]
seat = browser.find_element(By.CSS_SELECTOR, f'[style="display:none;"] [title="{zoneRoomStr}-{seatNum_str}"]')
sitKey = seat.get_attribute("key")
print("sitKey:", sitKey)
seatSelector = browser.find_element(By.CSS_SELECTOR, f'[class="fp-user fp-user-con"] [key="{sitKey}"]')
seatSelector.click()
sleep(0.3*speed)

# 预约时间写入并确认
start = Select(browser.find_elements(By.CSS_SELECTOR, '[name="start_time"]')[2])
sleep(0.2*speed)
start.select_by_value('700')
end = Select(browser.find_elements(By.CSS_SELECTOR, '[name="end_time"]')[2])
end.select_by_value('702')
sleep(1)
confirm = browser.find_element(By.XPATH, '/html/body/div[8]/div[2]/form/div[2]/input[1]')
confirm.click()

# broswer.close()