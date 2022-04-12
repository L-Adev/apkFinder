import requests
import sys,os
from bs4 import BeautifulSoup
from colorama import Fore, Back, init
import argparse
import concurrent.futures

init(autoreset=True)


class apksearch:

	def __init__(self, searchterm,threads,output):
		self.self = self
		self.downloadUrls = []
		self.urlCollection = []
		self.threads=threads
		self.output=output
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
					urlCollection.append(link['href'])
					with concurrent.futures.ThreadPoolExecutor(max_workers=int(self.threads)) as executor:
						checks = {executor.submit(self.getAll, cUrl): cUrl for cUrl in self.urlCollection}
						for future in concurrent.futures.as_completed(checks):
							url = checks[future]
							try:
								self.printresult(future.result())
							# self.updateui(future.result())
							# data = future.result()
							# print(data)
							except Exception as e:
								print(e)
								executor.shutdown()
					executor.shutdown()

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


def parse_args():
	# parse the arguments
	parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -d google.com -p basicscan")
	parser.error = parser_error
	parser._optionals.title = "OPTIONS"
	parser.add_argument('-t', '--threads', help="Threads to use for this scan", required=False, default=50)
	parser.add_argument('-s', '--search', help="The term to search for", required=False, default=input('Enter a search term: '))
	return parser.parse_args()


def parser_error(errmsg):
	print("Usage: python " + sys.argv[0] + " [Options] use -h for help")
	print("Error: " + errmsg)
	sys.exit()


def main():
	args = parse_args()
	threadarg = args.threads
	outputarg = args.output
	searcharg = args.search

	lookup = apksearch(searcharg,threadarg,outputarg)


if __name__ == '__main__':
    main()