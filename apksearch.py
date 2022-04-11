import requests
from bs4 import BeautifulSoup
from colorama import Fore, Back, init

init(autoreset=True)


class apksearch:

	def __init__(self, searchterm):
		self.self = self
		self.downloadUrls = []
		self.searchterm = searchterm
		self.page = 1
		self.useragent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'}

		while True:
			print(f'Scanning page - {self.page}')
			print('-' * 20)
			self.checkExists(searchterm)
			self.page += 1

	def checkExists(self, searchterm):
		if self.page == 1:
			baseUrl = f'https://www.apkmirror.com/uploads/?devcategory={searchterm}'
		else:
			baseUrl = f'https://www.apkmirror.com/uploads/page/{self.page}/?devcategory=canva'
		urlCollection = []
		r = requests.get(baseUrl, headers=self.useragent)
		html = r.text
		if 'No uploads found' in html:
			print(f'{Fore.RED}No search results found')
			print(f'{Fore.RED}Exiting...')
			exit()

		soup = BeautifulSoup(html, "html.parser")
		for link in soup.findAll('a', {'class': 'fontBlack'}):
			try:
				if searchterm in link['href']:
					print(f"{Fore.LIGHTYELLOW_EX}Found APK url >> {Fore.LIGHTWHITE_EX}{link['href']}")
					self.getAll(f"https://www.apkmirror.com{link['href']}")
					urlCollection.append(link['href'])
			except KeyError:
				pass

		for u in urlCollection:
			self.getAll(f'https://www.apkmirror.com{u}')

	def getAll(self, url):
		r = requests.get(url, headers=self.useragent)
		html = r.text
		if 'No uploads found' in html:
			print(f'{Fore.RED}No search results found')
			if len(self.downloadUrls) >0:
				exportcsv()
			exit()

		soup = BeautifulSoup(html, "html.parser")
		for link in soup.findAll('a', {'class': 'accent_color'}):
			try:
				FoundURL = link['href']
				if '-download/' in link['href']:
					self.downloadUrls.append(link['href'])
					print(f"{Fore.GREEN}        Found Download url >> {Fore.LIGHTWHITE_EX}{link['href']}")
					self.downloadUrls.append({'parentUrl': url, 'downloadUrl': f"https://www.apkmirror.com{link['href']}"})
			except KeyError:
				pass

	def exportcsv(self):
		with open(f'{self.searchterm}.csv', 'w') as f:
			w = csv.DictWriter(f, self.downloadUrls.keys())
			w.writeheader()
			w.writerow(my_dict)

searchterm = input('Search: ')
apksearch(searchterm)