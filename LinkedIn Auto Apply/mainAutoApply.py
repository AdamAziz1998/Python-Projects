from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
import time
import math
import re
from tqdm import tqdm
from selenium.webdriver.support.color import Color
import ast
import numpy as np
import pandas as pd
from IPython.display import HTML
import base64
from datetime import date
#-------------------------------------------------------some options and arguments------------------------------------------

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")

#-------------------------------------------------------increase speeds-------------------------------------------------------

#options.add_argument('--headless')  # Do not comment in if you are signing in, incase of the captcha
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

#---------------------------------------bypass block created from speed increase above---------------------------------------- 

#This block occured on a betting website originally
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')

#-------------------------------------------------Finding path to chromedriver-------------------------------------------------

driver = webdriver.Chrome(options = options, executable_path = otar.chrome_driver_path)








































current = Search()

print(current.filters('location',
    'python',    
    False, True, True,
    True, False, False, False,
    False, True, False,
    True, False, False, False, False, False, False, 
    True,
    False,
    True, False))