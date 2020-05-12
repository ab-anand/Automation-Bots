from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import os
import time
import json
import pickle
from simplecrypt import decrypt
import itertools
import threading
import time
import sys

done = False


# here is the animation
def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rSubmiting your code to the online judge(It takes time please be patient):' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    print('\n')


t = threading.Thread(target=animate)
t.start()

basic_details = {}
with open('../basic_details.json', 'rb') as f:
    basic_details = pickle.load(f)

chromeOptions = Options()
chromeOptions.add_argument('--headless')
driver = webdriver.Chrome(basic_details['path'] + '/chromedriver', options=chromeOptions)

driver.get('https://www.codechef.com')

time.sleep(3)
# TODO : Ask for username and password from user and tell the user that we will logout of existing places

password = decrypt('password', basic_details['password']).decode('utf8')

# Logging in
uname_sel = driver.find_element_by_css_selector('#edit-name')
pass_sel = driver.find_element_by_css_selector('#edit-pass')
sub_sel = driver.find_element_by_css_selector('#edit-submit')
uname_sel.send_keys(basic_details['user_name'])
pass_sel.send_keys(password)
sub_sel.click()
try:
    time.sleep(5)
    limit_page = driver.find_element_by_css_selector('#session-limit-page > div > div > div')
    checks = limit_page.find_elements_by_tag_name('input')
    time.sleep(5)
    for i in checks[:-1]:
        i.click()
    sub = driver.find_element_by_css_selector('#edit-submit')
    sub.click()
except NoSuchElementException:
    pass

with open('problem.json', 'r') as f:
    prob_details = json.load(f)
# TODO: Make a json from the setup.py file to get the link to submit page of the problem
page_link = 'https://www.codechef.com/submit/' + prob_details['code']
pwd = os.getcwd()
driver.get(page_link)

# File uploading and selecting the language and clicking
while 1:
    try:
        file_sel = driver.find_element_by_css_selector('#edit-sourcefile')
        file_sel.send_keys(pwd + '/sol.cpp')
        lang_sel = driver.find_element_by_css_selector('#edit-language')
        langs = lang_sel.find_elements_by_tag_name('option')
        for i in langs:
            if 'C++14(gcc 6.3)' in i.text:
                i.click()
        submit_file_sel = driver.find_element_by_css_selector('#edit-submit-1')
        submit_file_sel.click()
        break
    except NoSuchElementException:
        pass
# End file upload and submit


# Getting information from the result page
while 1:
    try:
        overall_res = driver.find_element_by_css_selector('#display_result > center > strong')
        sub_table = driver.find_element_by_css_selector('#status_table > table > tbody')
        status = sub_table.find_elements_by_tag_name('tr')
        break
    except NoSuchElementException:
        pass
# End of getting info from result page


# putting info result info into suitable containers
sub_tasks = []
subtask_scores = []
total_score = status[-1].text
for i in status[1:-1]:
    if 'Subtask' in i.text:
        sub_tasks.append('*')
        subtask_scores.append(i.text)
    else:
        sub_tasks.append(i.text)

# Printing the result in appropriate from

done=True
print('\n')
if 'Correct Answer' != overall_res.text:
    print('{:😥^35}'.format(overall_res.text))
else:
    print('{:👏^35}'.format(overall_res.text))
cnt = 0
print('\n{:^20}{:^20}{:^20}'.format('Sub-Task', 'Task #', 'Result (time)'))
for i in sub_tasks:
    if i == '*':
        print('\n{:*^60}'.format(subtask_scores[cnt]))
        cnt += 1
    else:
        l = i.split(' ')
        print('\n{:^20}{:^20}{:^20}'.format(l[0], l[1], l[2].split('\n')[0] + ' ' + l[2].split('\n')[1]))
print('\n{:^60}'.format(total_score))

# End of displaying the result
