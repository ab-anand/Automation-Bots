import json
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import re
import os
import time
from bs4 import BeautifulSoup
import requests
from shutil import copyfile
import pickle
from simplecrypt import encrypt

origin_path = os.getcwd()

basic_details = dict()
print('{:🤝^95}'.format(' Welcome to codechef contest setup bot!!'))
while 1:
    path = input('Enter the path in which you want to create the contest:')
    if not path.startswith('/'):
        print('Should put the absosute path of the directory')
    else:
        break

print('{:^150}'.format('Make sure you give the correct username and password because you won\'t get an error even if '
                       'you didn\'t !!!'))

uname = input('Enter your codechef username:')
passwd = getpass('Enter your codechef password:')

basic_details['user_name'] = uname

basic_details['path'] = os.getcwd()

encryptedPass = encrypt('password', passwd)

basic_details['password'] = encryptedPass  # FIXME:hash the password before saving it

months = ['JAN', 'FEB', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUG', 'SEPT', 'OCT', 'DEC']


def unmark(content):
    bs = ""
    for i in content.text[content.text.find('\n', 1):].split('\n'):
        if i:
            i = i.replace('$', '')
            i = i.replace('\le', '<=')
            i = i.replace('\lt', '<')
            i = i.replace('*', '')
            i = i.replace('###', '\n')
            i = i.replace('\ldots', '...')
            i = i.replace('`', '')
            bs += (i.strip(' ') + '\n')
    return bs


def CreateDict(contests, laddress):
    # TODO: need to correct what year is shown in the name of the file.
    for month in months:
        if laddress and month in laddress:
            contests[month + ' long challange'] = {'linkAddr': laddress}
            break
    else:
        if laddress and 'COOK' in laddress:
            monthIn = int(re.findall(r'[0-9]+', laddress)[0])
            month = months[(monthIn - 5) % 12 - 1]
            contests[month + ' cook off'] = {'linkAddr': laddress}

        elif laddress and 'LTIME' in laddress:
            monthIn = int(re.findall(r'[0-9]+', laddress)[0])
            month = months[(monthIn - 7) % 12 - 1]
            contests[month + ' lunch time'] = {'linkAddr': laddress}
    return (contests)


# FIXME: fix the timing of the searching of elements gets real anoying when we aren't noticing
def getContent(probName):
    url = 'https://www.codechef.com/' + probDict[probName]['link']
    probPage = requests.get(url)
    probsoup = BeautifulSoup(probPage.text, features="html.parser")
    time.sleep(2)
    cont = probsoup.select('#problem-page > div > div > div.primary-colum-width-left')[0]
    problem = cont.select('div')[0]
    content = problem.select('div')[1]
    content = unmark(content)
    return (content)


def getInputCases(content):
    inpStr = ""
    for i in content[content.find(' Example Input'):content.find(' Example Output')].split('\n')[1:]:
        inpStr += i
        inpStr += '\n'
    inpStr = inpStr.strip()
    return (inpStr)


def getOutputCases(content):
    outStr = ""
    if content.find(' Explanation') != -1:
        for i in content[content.find(' Example Output'):content.find(' Explanation')].split('\n')[1:]:
            outStr += i
            outStr += '\n'
    else:
        for i in content[content.find(' Example Output'):content.find('All')].split('\n')[1:]:
            outStr += i
            outStr += '\n'
    outStr = outStr.strip()
    return (outStr)


chromeOptions = Options()
chromeOptions.add_argument('--headless')

driver = webdriver.Chrome('./chromedriver', options=chromeOptions)

print('1).Do you want to use our ui or')
print('2).Will you put the link of the contest')
c = int(input('Enter your choice:'))
if c == 2:
    TargetPath = input('Enter URL of the contest:')
    contests = {}
    contests = CreateDict(contests, TargetPath)
    ch = 1
else:
    driver.get('https://www.codechef.com')
    time.sleep(2)
    links = driver.find_elements_by_tag_name('a')
    contests = dict()
    for link in links:
        try:
            laddress = link.get_attribute('href')
        except StaleElementReferenceException:
            continue
        contests.update(CreateDict(contests, laddress))
    while 1:
        i = 1
        for contest in contests.keys():
            print(str(i) + ').' + contest)
            i += 1
        print(str(i) + ').Exit')
        ch = int(input('Enter your choice to participate ( ex:1 for 1st choice):'))
        try:
            driver.get((list(contests.values())[ch - 1]['linkAddr']))
        except IndexError:
            break
            print('Invalid choice')
        while 1:
            try:
                details = driver.find_element_by_xpath('//*[@id="rules"]/div/div/div/ul[1]')
                break
            except NoSuchElementException:
                pass
        print('------------------------------------------------')
        print('Timing details:')
        print(details.text[:details.text.find('Check')])
        print('------------------------------------------------')
        announcments = driver.find_element_by_xpath('//*[@id="announcements"]')
        print(announcments.text)
        print('------------------------------------------------')
        print('In which division would you like to particpate:\n')
        print('1).Division A\n2).Division B\n3).Do you want to see the contests menu again\n')
        divCh = int(input('Enter your choice:'))
        if divCh != 3:
            DestUrl = (list(contests.values())[ch - 1]['linkAddr'])
            if DestUrl.find('?') != -1:
                TargetPath = DestUrl[:DestUrl.find('?')] + ('A' if divCh == 1 else 'B')
            else:
                TargetPath = DestUrl + ('A' if divCh == 1 else 'B')
            break
        else:
            print('+++++++++++++++++++++++++++++++++++++++++++++')

contCode = TargetPath.split('/')[-1]
basic_details['contest-code'] = contCode

res = requests.get(TargetPath)
soup = BeautifulSoup(res.text, features="html.parser")

probDict = dict()
table = soup.select('#primary-content > div.content-spacer > div > div > table')[0]
tbody = table.select('tbody')[0]
trows = tbody.select('tr')
for row in trows:
    eles = row.select('td')
    name = eles[0].text
    code = eles[1].text
    subs = eles[2].text
    acc = eles[3].text
    contCode = contCode.split('?')[0]
    link = contCode + '/problems/' + code
    probDict[name.strip()] = {'link': link.strip(), 'subs': subs.strip(), 'code': code.strip(), 'acc': acc.strip()}

contName = list(contests.keys())[ch - 1].replace(' ', '_')
os.chdir(path)
# origin_path = os.getcwd()
try:
    os.mkdir(contName)
except FileExistsError:
    pass
os.chdir(contName)
for problem in probDict.items():
    rPname = problem[0]
    pName = problem[0].replace(' ', '_')
    print('Creating ' + pName + ' Directory')
    try:
        os.mkdir(pName)
    except FileExistsError:
        pass
    os.chdir(pName)
    if rPname:
        content = getContent(rPname)
        inpStr = getInputCases(content)
        outStr = getOutputCases(content)
    print('writing statment.txt in ' + pName)
    with open('statment.txt', 'w') as f:
        f.write(content)
        f.close()
    print('writing input.dat in ' + pName)
    with open('given_input.dat', 'w') as f:
        f.write(inpStr)
        f.close()
    print('writing output.dat in ' + pName)
    with open('giver_output.dat', 'w') as f:
        f.write(outStr)
        f.close()
    print('Creating sol.cpp in ' + pName)
    copyfile(origin_path + '/template.cpp', './sol.cpp')
    # with open('sol.cpp', 'w') as f:
    #     f.close()
    print('copying test.py file in ' + pName)
    copyfile(origin_path + '/test.py', './test.py')
    print('copying submit.py file in ' + pName)
    copyfile(origin_path + '/submit.py', './submit.py')
    print('Creating a problem.json file')
    with open('problem.json', 'w') as f:
        json.dump(problem[1], f)
    print('----------------------------------------------')

    os.chdir('..')
os.chdir(origin_path)
print('Successfuly created a contest for you !!!!')

# with open(path + '/' + contName + '/basic_details.json', 'w') as file:
#     json.dump(basic_details, file)

with open(path + '/' + contName + '/basic_details.json', 'wb') as f:
    pickle.dump(basic_details, f)
