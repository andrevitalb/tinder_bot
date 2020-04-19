from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

class TinderBot():
	def __init__(self):
		self.driver = webdriver.Chrome()

