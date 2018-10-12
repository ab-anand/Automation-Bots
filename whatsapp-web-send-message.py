from selenium import webdriver

chrome_driver = 'C:/Users/Aashish/Downloads/chromedriver_win32/chromedriver'
driver = webdriver.Chrome(chrome_driver)
driver.get('http://web.whatsapp.com')

name = input('Enter the name of user or group : ')
msg = input('Enter the message : ')

input('Enter anything after scanning QR code')

user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
user.click()

msg_box = driver.find_element_by_class_name('_2S1VP')
msg_box.send_keys(msg)
driver.find_element_by_class_name('_35EW6').click()
