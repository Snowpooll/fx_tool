from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
userdata_dir = 'UserData'  # カレントディレクトリの直下に作る場合
os.makedirs(userdata_dir, exist_ok=True)


url="https://wp.developapp.net/wp-admin/"

options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=' + userdata_dir)
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=options)
driver.get(url)