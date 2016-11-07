# -*- coding: utf-8 -*-

from splinter.browser import Browser
from time import sleep
import traceback

# 用户名，密码
username = "***"
passwd = "***"
# cookies
ends = u"%u4E0A%u6D77%2CSHH"
starts = u"%u4E5D%u6C5F%2CJJG"
# 时间格式2016-01-31
dtime = u"2016-12-03"
# 车次，选择第几趟，0则从上之下依次点击
order = 2
###乘客名
pa = u"姓名"

"""网址"""
ticket_url = "https://kyfw.12306.cn/otn/leftTicket/init"
login_url = "https://kyfw.12306.cn/otn/login/init"
initmy_url = "https://kyfw.12306.cn/otn/index/initMy12306"


def login():
    b.find_by_text(u"登录").click()
    sleep(3)
    b.fill("loginUserDTO.user_name", username)
    sleep(1)
    b.fill("userDTO.password", passwd)
    sleep(1)
    print u"等待验证码，自行输入..."
    while True:
        if b.url != initmy_url:
            #print "."
            sleep(1)
        else:
            break
            
class finishreservation(Exception): pass
	
def huoche():
    global b
    b = Browser(driver_name="chrome")
    b.visit(ticket_url)

    while b.is_text_present(u"登录"):
        sleep(1)
        login()
        if b.url == initmy_url:
            break

    try:
        print u"进入购票页面..."
        # 跳回购票页面
        b.visit(ticket_url)

        # 加载查询信息
        b.cookies.add({"_jc_save_fromStation": starts})
        b.cookies.add({"_jc_save_toStation": ends})
        b.cookies.add({"_jc_save_fromDate": dtime})
        b.reload()
        b.cookies.all()

        sleep(2)

        count = 0
        # 循环点击预订
        if order != 0:
            while b.url == ticket_url:
                b.find_by_text(u"查询").click()
                count +=1
                print u"1循环点击查询... 第 %s 次, order=%d" % (count,order)
                sleep(10) #in seconds
                try:
                    b.find_by_text(u"预订")[order - 1].click()
                    sleep(1)
                    if b.is_text_present(u"证件号码",wait_time=0.5):
                    	b.find_by_text(pa)[1].click()
                    	b.execute_script("alert('请选择验证码并提交订单')")
                    	break;
                except:
                    print u"还没开始预订"
                    continue
        else:
            while b.url == ticket_url:
                b.find_by_text(u"查询").click()
                count += 1
                #print u"循环点击查询... 第 %s 次" % count
                print u"2循环点击查询... 第 %s 次, order=%d" % (count,order)
                sleep(10)
                try:
                    for i in b.find_by_text(u"预订"):
                        i.click()
                        sleep(1)
                        if b.is_text_present(u"证件号码"):
                            b.find_by_text(pa)[1].click()
                            b.execute_script("alert('请选择验证码并提交订单')")
                            raise finishreservation()
                            #break;
                except finishreservation:
                	  break;
                except Exception as e:
                    print u"还没开始预订"
                    continue

        #sleep(1)
        #b.find_by_text(pa)[1].click()
        
        print  u"请手动操作...."
    except Exception as e:
        print(traceback.print_exc())

if __name__ == "__main__":
    huoche()

