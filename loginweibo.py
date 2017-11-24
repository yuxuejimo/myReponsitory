#coding=utf-8
from selenium import webdriver
import time
from PIL import Image
import pytesseract
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Ie()
# 填写表单

# 登录
def input_un_pw_code(un , pw):
    # 填写用户名，密码
    driver.find_element_by_id('login_field').send_keys(un)
    driver.find_element_by_id('password_field').send_keys(pw)
    # 识别验证码
    driver.save_screenshot('D://aa.png')
    imgelement = driver.find_elements_by_xpath('//img[@src="/home/login_code"]')[0]
    location = imgelement.location
    size = imgelement.size
    rangle=(int(location['x']),int(location['y']),int(location['x']+size['width']),int(location['y']+size['height']))
    i=Image.open("D://aa.png") #打开截图
    frame4=i.crop(rangle)  #使用Image的crop函数，从截图中再次截取我们需要的区域
    frame4.save('D://code.png')
    text=pytesseract.image_to_string(Image.open('D://code.png')).strip() #使用image_to_string识别验证码
    print(text)
    driver.find_element_by_id('login_code_field').send_keys(text)
    # 记住用户名，密码
    
    driver.find_element_by_id('user_remember_me').click()

# 获取可参与采购的项目
def get_participate_items(project_id):
    # 根据项目编号搜索项目 GDC-20171115112485533
    driver.find_element_by_id('project_code').send_keys(project_id)
    # 点击搜索
    driver.find_elements_by_xpath('//button[@type="submit"]')[0].click()
    # 点击搜索出来的项目名称
    time.sleep(1)
    # 点击要竞价的项目名称链接
    driver.find_elements_by_tag_name('a')[-1].click()
    driver.find_elements_by_link_text('北京CA')[0].click()
    # 输入CA密码
    driver.find_element_by_id('UserPwd').send_keys('lijian100324')
    driver.find_elements_by_xpath('//input[@type="submit"]')[0].click()
    time.sleep(2)
    driver.find_element_by_xpath('//input[@id="submit_button"]').click()
    # 确定alert
    driver.switch_to_alert().accept()
    driver.switch_to_alert().accept()
    # 选择同意竞价规则和送货要求
    con_cb = driver.find_elements_by_css_selector('input[type=checkbox]')
    for c in con_cb:
        c.click()
    time.sleep(1)
    driver.find_element_by_id('submit_button').click()
    time.sleep(1)
    driver.switch_to_alert().accept()
    driver.switch_to_alert().accept()

# 填写报价
def input_quotation():
    # 获取需要填写的行
    row_count = len(driver.find_elements_by_name('FDBid_Price'))
    for i in range(0, row_count):
        driver.find_elements_by_name('FDBid_Price')[i].send_keys('34')
        driver.find_elements_by_name('FDMemo')[i].click()
        driver.find_element_by_id('simple_submit' + str(i + 1)).click()
        time.sleep(1)
        driver.switch_to_alert().accept()
        time.sleep(1)
    # 信用中国信用记录截图
    driver.find_element_by_name('xy1_file').send_keys(r'D:\post竞价\竞价所需截图\信用中国截图.jpg')
    # 中国政府采购网截图
    driver.find_element_by_name('xy2_file').send_keys(r'D:\post竞价\竞价所需截图\中国政府采购网截图.png')
    time.sleep(1)
    driver.find_element_by_id('submit_button').click()
    time.sleep(1)
    driver.switch_to_alert().accept()
    driver.switch_to_alert().accept()


def isElementExist(element):
    flag = True
    browser = driver
    try:
        browser.find_element_by_class_name(element)
        return flag
    except:
        flag = False
        return flag

if __name__ == '__main__':
    driver.get('http://www.zycg.gov.cn/')
    # 判断是否登录
    if not isElementExist("logind_user"):
        # 登录
        driver.get('http://www.zycg.gov.cn/session/login_page')
        un = 'lanyun1'
        pw = 'lijian100324'
        input_un_pw_code(un, pw)
        time.sleep(1)
        try:
            driver.find_elements_by_xpath('//input[@type="submit"]')[0].click()
        except Exception as e:
            print(e)
            driver.switch_to_alert().accept()
            input_un_pw_code(un,pw)
    # 开始竞价
    driver.get('http://www.zycg.gov.cn/main')
    # 等待网页加载
    time.sleep(3)
    # 点击网上竞价（新版）
    try:
        wsjj = driver.find_element_by_id('webfx-tree-object-19-icon')
        # 双击，显示可参与采购项目
        ActionChains(driver).double_click(wsjj).perform()
        # 可参与采购项目
        time.sleep(2)
        kcycgxm_url = driver.find_element_by_id('webfx-tree-object-30-anchor').get_attribute('href')
        # 打开可参与采购项目页面
        driver.get(kcycgxm_url)
        # 根据项目编号搜索项目 GDC-20171115112485533
        get_participate_items('GDC-20160525104743000')
        input_quotation()
        driver.quit()
    except Exception as e:
        print(e)




