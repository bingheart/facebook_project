import json
import os
import random
import time
from selenium.webdriver.common.keys import Keys
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import requests
import undetected_chromedriver as webdriver
from facebook_project.settings import CACHES
import redis

class FacebookCom():

    def get_driver(self,path_data):
        options = webdriver.ChromeOptions()
        options.add_argument(f"--load-extension={path_data}")
        options.add_argument("--enable-automation")  # 启用自动化
        options.add_argument("--start-maximized")  # 瀏覽器最大化
        options.add_argument("--disable-infobars")  # 禁用信息欄
        options.add_argument("--disable-popup-blocking")  # 禁用彈出窗口阻止
        options.add_argument("--disable-notifications")  # 禁用通知
        options.add_argument("--disable-password-manager-reauthentication")  # 禁用密碼管理器重新驗證
        options.add_argument("--disable-infobars")  # 禁用提示框
        options.add_argument("--disable-save-password-bubble")  # 禁止保存密碼提示
        driver = uc.Chrome(headless=False, options=options, use_subprocess=False)
        return driver

    def login(self,driver, user_name, password):
        driver.find_element(By.ID, 'email').send_keys(user_name)
        driver.find_element(By.ID, 'pass').send_keys(password)
        driver.find_element(By.ID, 'loginbutton').click()

    def get_2fa(self,key='2PJ7+NCL6+57JM+QLBU+MES6+6HGU+ZCKD+J4QR'):
        try:
            url = f"http://xd-2fa.axnasgmail.cn/app/PHP_API_OK.php?key={key}"
            req = requests.get(url=url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36'})
            if req.status_code == 200:
                return req.json()['code']
        except:
            return input('請輸入驗證碼：')

    def wait_for_page_load(self,driver, timeout=10):
        # 等待頁面加載完成
        WebDriverWait(driver, timeout).until(
            EC.staleness_of(driver.find_element(By.TAG_NAME, 'html'))
        )

    def is_verification(self,driver):
        try:
            # 等待直到用戶名元素可見，即表示登錄成功
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'approvals_code'))
            )
            # 等待直到用戶名元素可見，即表示登錄成功
            return True
        except:
            return False
    def input_verification_code(self,driver, code):
        driver.find_element(By.ID, 'approvals_code').send_keys(code)
        driver.find_element(By.ID, 'checkpointSubmitButton').click()
        try:
            element_present = EC.presence_of_element_located((By.NAME, 'name_action_selected'))
            WebDriverWait(driver, 10).until(element_present)
            time.sleep(5)  # 等待 2 秒
            # driver.find_element(By.NAME, 'name_action_selected').click()
            for i in range(1,5):
                try:
                    checkpointSubmitButton = driver.find_element(By.ID, 'checkpointSubmitButton')
                    if checkpointSubmitButton:
                        checkpointSubmitButton.click()
                        time.sleep(5)
                except:
                    time.sleep(2)
        except TimeoutException:
            print("等待超時，頁面可能未能完全加載。")

    def rolling(self,driver,page):
        try:
            element_present = EC.presence_of_element_located((By.ID, 'facebook'))
            WebDriverWait(driver, 10).until(element_present)
            time.sleep(5)  # 等待 2 秒
            for i in range(0,page):
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
                time.sleep(5)  # 等待 2 秒
        except TimeoutException:
            print("等待超時，頁面可能未能完全加載。")

class Redis():
    # 设置用户信息
    def set_user_info(self,redis_client,user_id, code, password, cookie):
        user_info_key = f'user:{user_id}'
        # 将用户信息存储到 Hash 中

        redis_client.hset(user_info_key, 'user_id', user_id)
        redis_client.hset(user_info_key, 'password', password)
        redis_client.hset(user_info_key, 'code', code)
        redis_client.hset(user_info_key, 'cookie', json.dumps(cookie, ensure_ascii=False))

    # 添加用户到队列并设置用户信息
    def add_user_to_queue(self,redis_client,user_id, code, password, cookie):
        user_queue_key = 'user_queue_key'
        # 向队列中添加用户ID（转换为字符串）
        redis_client.lpush(str(user_queue_key), str(user_id))
        # 设置用户信息
        self.set_user_info(redis_client,str(user_id), code, password, cookie)

if __name__ == '__main__':
    project_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")).replace('\\', '/')
    path_data = project_path + '/reptiles/google_plugins'
    facebook_com = FacebookCom()
    while True:
        LOCATION = str(CACHES['default']['LOCATION']).replace('redis://','').split(':')
        PASSWORD = CACHES['default']['OPTIONS']['PASSWORD']
        redis_client = redis.StrictRedis(host=LOCATION[0], port=LOCATION[1], db=0, password=PASSWORD)
        facebook_user = redis_client.lpop('user_queue')
        crawler_queue = redis_client.lpop('crawler_queue')
        if facebook_user != None:
            facebook_user = json.loads(facebook_user.decode('utf-8'))
            driver=facebook_com.get_driver(path_data)
            driver.get('https://www.facebook.com/')
            facebook_com.login(driver, facebook_user['user_name'], facebook_user['password'])
            if facebook_com.is_verification(driver):
                print('登錄成功')
                code = facebook_com.get_2fa(key=facebook_user['code'])
                facebook_com.input_verification_code(driver, code)
                try:
                    element_present = EC.presence_of_element_located((By.ID, 'facebook'))
                    WebDriverWait(driver, 10).until(element_present)
                    print("确认存在")
                    cookies = driver.get_cookies()
                    Redis().add_user_to_queue(redis_client, facebook_user['user_name'], facebook_user['code'], facebook_user['password'], cookies)
                except TimeoutException:
                    print("等待超時，頁面可能未能完全加載。")
            driver.quit()
        elif crawler_queue != None:
            user_cookies_s = redis_client.lrange("user_cookies", 0, -1)
            user_queue_key = redis_client.lrange('user_queue_key', 0, -1)
            if len(user_queue_key) == 0:
                break
            updated_user_info = redis_client.hgetall("user:"+str(user_queue_key[0].decode('utf-8')))
            if updated_user_info == None:
                print('cookie 不能为空')
                break
            crawler_queue = json.loads(crawler_queue.decode('utf-8'))
            cookie=updated_user_info.get(b'cookie',b'').decode('utf-8')
            if cookie:
                cookies = json.loads(cookie)
            else:
                cookies = None
            if cookies == None:
                break
            driver = facebook_com.get_driver(path_data)
            driver.get('https://www.facebook.com/')
            for cookie in cookies:
                driver.add_cookie(cookie)
            if crawler_queue.get('is_post',False):
                time.sleep(5)
                driver.get('https://www.facebook.com/profile.php?id={}'.format(crawler_queue.get('id',None)))
                facebook_com.rolling(driver, crawler_queue.get('page',1))
            else:
                time.sleep(5)
                driver.get('https://www.facebook.com/profile.php?id={}&sk=friends'.format(crawler_queue.get('id', None)))
                facebook_com.rolling(driver, crawler_queue.get('page', 1))
            cookies = driver.get_cookies()
            redis_client.hset("user:"+str(user_queue_key[0].decode('utf-8')), 'cookie', json.dumps(cookies, ensure_ascii=False))
            driver.quit()