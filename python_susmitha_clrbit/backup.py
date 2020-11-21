chromedriver = "/Users/sancheru/Downloads/chromedriver"

  chrome_options = Options()
  chrome_options.add_argument("--user-data-dir=chrome-data")
  driver = webdriver.Chrome(chromedriver,options=chrome_options)
  driver.get('https://caprica.seoboxes.com:2096/cpsess8220829249/3rdparty/roundcube/?_task=mail&_action=compose&_id=14557673775fb5a90c1c498')


  username_input = '//*[@id="user"]'
  password_input = '//*[@id="pass"]'
  login_submit = '//*[@id="login_submit"]'
  #driver.find_element_by_xpath(first_login).click()
  driver.find_element_by_xpath(username_input).send_keys("stewardsmike@wizzardpro.com")
  driver.find_element_by_xpath(password_input).send_keys("stewardsmike34")
  driver.find_element_by_xpath(login_submit).click()
  driver.maximize_window()
  time.sleep(4)
  print("Window has been opened")

  driver.find_element_by_xpath('//*[@id="rcmbtn107"]').click()#Junk -> //*[@id="rcmliSU5CT1guSnVuaw"]/a
  print("Navigating to Next Page")
  time.sleep(1)
  print("Sleep 1 second")

  to_input = '//*[@id="_to"]'
  subject_input = '//*[@id="compose-subject"]'
  composebody_input = '//*[@id="composebody"]'
  send_message_submit = '//*[@id="rcmbtn107"]'


  '''driver.find_element_by_xpath(to_input).send_keys("web@sroportal.sk, info@sroportal.sk,,")
  driver.find_element_by_xpath(subject_input).send_keys("Paid ad space")
  driver.find_element_by_xpath(composebody_input).send_keys("Hi,\nWe just came through your website. \nWe are interested in buying a guest post on your website sroportal.sk. We will provide relevant quality content that includes sports betting. If possible, how much does it cost?\nPlease let me know what you think, waiting for your response,\nBest regards")
'''
  time.sleep(1)
  driver.find_element_by_xpath(send_message_submit).click()
  time.sleep(1)
