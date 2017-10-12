import urllib.request
from datetime import datetime
from bs4 import BeautifulSoup		

def get_page(url):
	return urllib.request.urlopen(url).read()


def parse(html, currency):
	soup = BeautifulSoup(html, 'html.parser')
	table = soup.find('tbody')

	projects = []



	for row in table.find_all('tr'):
		cols = row.find_all('td')

		projects.append(
			'   ' + 
			cols[0].a.text + '         ' +
			cols[2].text + '        ' +
			cols[3].text)

	print('Currency code| Units per ' + currency + 
		'      |    ' + currency + ' per Unit'
		  ' ')

	for project in projects:
		print(project)


def main():
	today_date = datetime.now().date()
	currency = input('Enter currency code (ex. USD): ')
	html = get_page('http://www.xe.com/currencytables/?from=' + currency + '&date=' + str(today_date))
	parse(html, currency)


if __name__ == '__main__':
	main()
