from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time  # for sleep

import os 
import requests
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate

class Scraper :

  def __init__(self):
    self.from_addr = 'baseball.team.impact@gmail.com'
    self.my_password = 'ueknoiibsgcyfxpe'

    self.line_notify_token = os.environ.get('LINE_NOTIFY_TOKEN', 'xQfqD0GeVU9xvEwkJgls9sxvDBWoyd81SkxFl5MDoTP')
    
    options = Options()
    options.add_argument('--disable-gpu');
    options.add_argument('--disable-extensions');
    options.add_argument('--proxy-server="direct://"');
    options.add_argument('--proxy-bypass-list=*');
    options.add_argument('--start-maximized');
    # Headless Chromeをあらゆる環境で起動させるオプション
    # options.add_argument('--headless');

    driver_path = os.environ.get('DRIVER_PATH', '/Users/ohnukihiroki/Downloads/chromedriver')
    self.driver = webdriver.Chrome(executable_path=driver_path, options=options)

  # LINEに通知させる関数
  def line_notify(self, message):
    line_notify_api = 'https://notify-api.line.me/api/notify'
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + self.line_notify_token}
    requests.post(line_notify_api, data=payload, headers=headers)

  def create_mail(self, to_addr, bcc_addrs, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = self.from_addr
    msg['To'] = to_addr
    msg['Bcc'] = bcc_addrs
    msg['Date'] = formatdate()
    return msg

  def send(self, to_addrs, msg):
    smtpobj = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10)
    smtpobj.login(self.from_addr, self.my_password)
    smtpobj.sendmail(self.from_addr, to_addrs, msg.as_string())
    smtpobj.close()

  def find_element(self, selector, el=None):
      target = selector
      if not el:
          el = self.driver
      if type(selector) is str:
          self.wait_until(selector, el)
          target = el.find_element_by_css_selector(selector)
      return target

  def find_elements(self, selector, el=None):
      target = selector
      if not el:
          el = self.driver
      if type(selector) is str:
          self.wait_until(selector, el)
          target = el.find_elements_by_css_selector(selector)
      return target

  def wait_until(self, selector, el=None):
      if not el:
          el = self.driver
      WebDriverWait(el, 15).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
  
  def switch_to_window(self, window_order):
      allHandles = self.driver.window_handles
      self.driver.switch_to_window(allHandles[window_order])
      self.driver.set_window_size(1600, 1200)
      print("opened : " + self.driver.title)

  def close_window_and_return(self):
      print("closing : " + self.driver.title)
      self.driver.close() #close current window
      allHandles = self.driver.window_handles
      self.driver.switch_to_window(allHandles[0]) #return to first window        print("back to : " + self.driver.title)

  def click(self, selector, el=None):
      target = self.find_element(selector, el)
      success = False
      count = 0
      while (not success) and count < 3:
          count += 1
          try:
              target.click()
              success = True
          except:
              import traceback
              traceback.print_exc()
              time.sleep(1)