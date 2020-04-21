from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

from secrets import username, password
from random import random

class TinderBot():
	def __init__(self):
		self.driver = webdriver.Chrome()

	def login(self, login = 'FB'):
		# Go to website and wait for login popup
		self.driver.get('https://tinder.com')
		sleep(3)

		if login == 'FB':
			# Check if FB Login button is displayed
			if len(self.driver.find_elements_by_xpath('//button[text()="Trouble Logging In?"]')) >= 1:
				# If it is, click it
				self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/span/div[2]/button').click()
			else:
				# If it isn't click More Login Options button and then click it
				self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/span/button').click()
				self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/span/div[3]/button').click()

			# Switch to FB login popup
			base_window = self.driver.window_handles[0]
			self.driver.switch_to_window(self.driver.window_handles[1])

			# Enter login credentials & submit
			self.driver.find_element_by_xpath('//*[@id="email"]').send_keys(username)
			self.driver.find_element_by_xpath('//*[@id="pass"]').send_keys(password)
			self.driver.find_element_by_xpath('//*[@id="u_0_0"]').click()
		elif login == 'Google':
			# Click Google login button
			self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/span/div[1]/div/button').click()

			# Switch to Gmail login popup
			base_window = self.driver.window_handles[0]
			self.driver.switch_to_window(self.driver.window_handles[1])

			# Enter login credentials & submit
			self.driver.find_element_by_xpath('//*[@id="identifierId"]').send_keys(username)
			self.driver.find_element_by_xpath('//*[@id="identifierNext"]').click()
			sleep(3)

			self.driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
			self.driver.find_element_by_xpath('//*[@id="passwordNext"]').click()

		sleep(5.5)

		# Switch back to base window
		self.driver.switch_to_window(base_window)

		# Allow location usage. disable notifications & accept privacy terms
		self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]').click()
		sleep(0.5)

		self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[2]').click()
		sleep(0.5)

		self.driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div/div[1]/div/button').click()
		sleep(0.5)

		# Temporary action for free passport accept
		# # Remove once this free feature is disabled
		# self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]/button').click()

	def like(self):
		like_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button')

		like_btn.click()

	def dislike(self):
		dislike_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[2]/button')

		dislike_btn.click()
		
	def auto_swipe(self):
		self.likes, self.dislikes, self.matches = 0, 0, 0
		while True:
			sleep(3)

			try:
				rand = random()
				if rand < .73: 
					self.like()
					self.likes = self.likes + 1
					print('{}th like'.format(self.likes))
				else: 
					self.dislike()
					self.dislikes = self.dislikes + 1
					print('{}th dislike'.format(self.dislikes))
			except Exception:
				try: 
					self.close_popup()
				except Exception: 
					try:
						self.close_ad_popup()
					except Exception:
						try:
							self.close_match()
							self.matches = self.matches + 1
							print('{}th match'.format(self.matches))
						except Exception:
							print('\n\n**************No one left!**************\n{} total likes\n{} total dislikes\n{} total matches'.format(self.likes, self.dislikes, self.matches))
							break 

	def close_popup(self):
		self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]/button[2]').click()

	def close_ad_popup(self):
		self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[3]/button[2]').click()

	def close_match(self):
		self.driver.find_element_by_xpath('//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a').click()

	def message_all(self):
		while True:
			matches = self.driver.find_elements_by_class_name('matchListItem')[1:]
			
			if len(matches) < 1: 
				break

			matches[0].click()
			sleep(0.2)

			msg_box = self.driver.find_element_by_class_name('sendMessageForm__input')
			msg_box.send_keys('Hello there (:')

			send_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[3]/form/button')
			send_btn.click()
			sleep(1)

			matches_tab = self.driver.find_element_by_xpath('//*[@id="match-tab"]')
			matches_tab.click()
			sleep(0.5)

bot = TinderBot()
bot.login()
bot.auto_swipe()
bot.message_all()