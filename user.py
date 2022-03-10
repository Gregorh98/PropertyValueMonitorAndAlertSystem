import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date
from functions import *
import re

class User():
	def __init__(self, userid, name, email, code, propertyValue):
		self.userid = userid
		self.name = name
		self.propertyCode = code
		self.email = email
		self.propertyValue = propertyValue
		
	def getPropertyValue(self):
		URL = f"https://www.zoopla.co.uk/property/uprn/{self.propertyCode}/"
		page = requests.get(URL)
		soup = BeautifulSoup(page.content, "html.parser")
		results = soup.find_all("p", class_=re.compile("EstimatedPriceText"))
		return(results[0].text.strip())
			
	def emailValue(self, oldValue, newValue):
		mailserver = smtplib.SMTP('smtp.office365.com',587)
		mailserver.ehlo()
		mailserver.starttls()
		mailserver.ehlo()
		mailserver.login('gregor.hastings@outlook.com', 'lG4M#@0WTB&y')
		msg = MIMEMultipart()
		msg['From'] = 'gregor.hastings@outlook.com'
		msg['To'] = self.email
		msg['Subject'] = 'Change in property price!'
		message = f"Hello, {self.name}!\n\nThe price of your property has changed!\nIt was previously worth {oldValue}.\nIt is now worth {newValue}!\n\n{date.today()}"
		msg.attach(MIMEText(message))
		mailserver.sendmail('gregor.hastings@outlook.com', self.email, msg.as_string())
		mailserver.quit()
		
	def checkPropertyValue(self):
		newValue = int(self.getPropertyValue()[1:].replace(",", ""))
		
		if newValue != self.propertyValue:
			try:
				self.emailValue(convertToCurrency(self.propertyValue), convertToCurrency(newValue))
				return newValue
			except Exception as e:
				print(f"Unable to email user {self.name}\n\n\n{e}")
		return None;
		
		
		
	
