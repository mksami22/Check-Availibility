from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import slack 
import os
import time

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.bestbuy.ca/en-ca/product/insignia-portable-air-conditioner-12000-btu-white-grey-only-at-best-buy/11794998")

my_secret = os.environ['slack_token']


client = slack.WebClient(token=os.environ['slack_token'])

# client.chat_postMessage(channel='#project', text='helloooo')

def isAvailableText(driver):
  e = driver.find_element_by_css_selector('.storeAvailabilityContainer_1Ez2A > div > span')
  return e.text

def checkWebsite():
  print('refreshing...')
  driver.refresh()
  try:
    availableText = isAvailableText(driver)
    if availableText == 'Unavailable for store pickup':
      text_to_send = availableText
    else:
      text_to_send = availableText + ' ' + '<@U027BM71A8L>'
  except Exception as e:
    text_to_send = str(e)

  client.chat_postMessage(channel='#project', text=text_to_send)
  print('sent a message: ' + text_to_send)

while True:
  checkWebsite()
  # This used to run every 5 minutes.
  # I modified it to run every 60 minutes.
  waited = 0
  for i in range(60):
    time.sleep(60)
    waited += 1
    print(f'waited for: {waited} minute')
