from selenium import webdriver
from bs4 import BeautifulSoup
import time

import getpass

# OUT FGV
APPS = 'http://apps-webofknowledge.ez91.periodicos.capes.gov.br.sbproxy.fgv.br'
# IN FGV
#APPS = 'http://apps-webofknowledge.ez91.periodicos.capes.gov.br'

driver = webdriver.Chrome(executable_path = r'/Users/acwgdb/chromedriver')


def login(local=None):

	if local == 'FGV':
		driver.get( APPS + '/WOS_GeneralSearch.do')

		driver.maximize_window()
	else:
		driver.get('https://login.sbproxy.fgv.br/login?url=' + APPS + '/WOS_GeneralSearch.do')

		driver.maximize_window()

		user = driver.find_element_by_xpath('//*[@id="user"]')
		user.send_keys(getpass.getpass('User:'))

		password = driver.find_element_by_xpath('//*[@id="pass"]')
		pswd = getpass.getpass('Password:')
		password.send_keys(pswd)

		login = driver.find_element_by_xpath('//*[@id="login-table"]/tbody/tr[3]/td/input[3]')
		login.click()

		time.sleep(30)

	return driver


def clearSearchHistory():

	driver.get('https://login.sbproxy.fgv.br/login?url=' + APPS + '/WOS_GeneralSearch.do')
	soup = BeautifulSoup(driver.page_source,'lxml')

	select_all = driver.find_element_by_xpath('/html/body/div[12]/form/table/tbody/tr[5]/td[6]/div/input[1]')
	select_all.click()

	delete = driver.find_element_by_xpath('/html/body/div[12]/form/table/tbody/tr[5]/td[6]/div/input[2]')
	delete.click()

	return driver


def advancedSearch(journals, year_list, ind):
	'''
		Advanced Search by Publication Name (field_tags = 'SO').
		Add filters: PY - Publication Year AND DT - Document Type (Articles)

		INPUT:
			journals: data frame
			year_list: list of years 
			ind: index of journal to start the search

		OUTPUT: 
			driver
	'''

	soup = BeautifulSoup(driver.page_source,'lxml')
	SID = soup.find('td', class_ = 'csi-checkemail-left-column').input['value']

	advancedSearch = APPS + '/WOS_AdvancedSearch_input.do?SID=' + SID + '&product=WOS&search_mode=AdvancedSearch'
	driver.get(advancedSearch)

	n = len(journals)

	year_from = str(year_list[0])
	#year_to = str(year_list[-1]) 
	year_to = str(2017)

	for i in range(ind, n+1):

		print('Advanced Search - Journal ' + str(i))

		search = driver.find_element_by_xpath('//*[@id="value(input1)"]')
		search.clear()
		search.send_keys('SO = (' + journals.TITLE[i] + ')' + ' AND PY = (' + year_from + '-' + year_to +') AND DT = (Article)')

		button = driver.find_element_by_xpath('//*[@id="searchButton"]/input')
		button.click()
		time.sleep(3)

	return driver


def advancedSearch_all(journals, year_list):

	soup = BeautifulSoup(driver.page_source,'lxml')
	SID = soup.find('td', class_ = 'csi-checkemail-left-column').input['value']

	advancedSearch = APPS + '/WOS_AdvancedSearch_input.do?SID=' + SID + '&product=WOS&search_mode=AdvancedSearch'
	driver.get(advancedSearch)

	n = len(journals)

	year_from = str(year_list[0])
	#year_to = str(year_list[-1]) 
	year_to = str(2017)

	search_list = ''

	print('Advanced Search - ' + str(n) + ' Journals')

	for i in range(1, n+1):

		search_list = search_list + '(SO = (' + journals.TITLE[i] + ')' + ' AND PY = (' + year_from + '-' + year_to +') AND DT = (Article)) OR '

	search_list = search_list[:-4]

	search = driver.find_element_by_xpath('//*[@id="value(input1)"]')
	search.clear()
	search.send_keys(search_list)

	button = driver.find_element_by_xpath('//*[@id="searchButton"]/input')
	button.click()

	return driver


def searchHistoryLinks(journals):
	'''
		INPUT:
			journals: data frame

		OUTPUT:
			journals: data frame
	'''

	n = len(journals)

	soup = BeautifulSoup(driver.page_source,'lxml')

	all_div = soup.find_all('div', class_ = 'historyResults')

	i = n
	for div in all_div:
	    journals.LINK[i] = APPS + div.a['href']
	    i = i - 1

	return journals, driver


def allArticles(journals, journal_id, articles):
	'''
		INPUT:
			journals: data frame
			journal_id: id of journal chosen 
			articles: data frame

		OUTPUT:
			articles: data frame
	'''

	ID_J = len(journals)
	ID_A = len(articles) + 1

	url = APPS + '/summary.do?product=WOS&parentProduct=WOS&search_mode=AdvancedSearch&qid=' + str(journal_id) + '&SID=6BO521EqrbfLAhtLGK1&page=1&action=changePageSize&pageSize=50'
	driver.get(url)

	pages = int(driver.find_element_by_xpath('//*[@id="pageCount.top"]').text)

	print('Peiódico ' + str(journal_id) + ' - Total de Páginas: ' + str(pages))

	for page in range(1, pages+1):
		
		soup = BeautifulSoup(driver.page_source, 'lxml')
		all_div = soup.find_all('div', class_ = 'search-results-item')
		all_div = all_div[0:int(len(all_div)/2)] # os resultados aparecem em duplicatas nas páginas

		for div in all_div:
			title = div.find('a', class_ = 'smallV110').value.text

			if title != None: # existem alguns artigos sem links
				year = int(div.find_all('span', class_ = 'data_bold')[-1].value.text[-4:])
				link = APPS + div.find('a', class_ = 'smallV110')['href']

				articles.loc[ID_A] = [title, link, journal_id, int(year), 'NaN']
				ID_A = ID_A + 1

		url = APPS + '/summary.do?product=WOS&parentProduct=WOS&search_mode=AdvancedSearch&qid=' + str(journal_id) + '&SID=6BO521EqrbfLAhtLGK1&page=' + str(page+1) + '&action=changePageSize&pageSize=50'
		driver.get(url)

	return articles


def extractInfo(articles, ID_J):
	'''
		INPUT:
			articles: data frame
			ID_J: id of journal chosen

		OUTPUT:
			articles: data frame
	'''

	ID_A = len(articles)

	aux = articles[articles['JOURNAL_ID'] == ID_J]

	for i in range(1, ID_A+1):
		driver.get(articles.LINK[i])
		soup = BeautifulSoup(driver.page_source,'lxml')

		#ref = soup.find('div', class_ = 'block-text-content').p.find_next_sibling().text.split('          ')[1][0]
		ref = driver.find_element_by_xpath('//*[@id="records_form"]/div/div/div/div[2]/div[2]/div/div/p[2]').text

		if int(str(ref[0])) == 0:
			cited_link = 'NaN'
		else:
			cited_link = APPS + '/' + soup.find('a', title = 'View this record’s bibliography')['href']

		articles.LINK_CIT[i] = cited_link

	return articles


def allCitations(articles, articles_cit, journals_cit, citations):

	ID_A = len(articles)
	ID_CIT = len(citations) + 1
	ID_J_CIT = len(journals_cit)
	ID_A_CIT = len(articles_cit)

	for  articleSource_id in range(1, ID_A+1):
		print('Citações Feitas pelo Artigo ID = ' + str(articleSource_id))
		journalSurce_id = articles.JOURNAL_ID[articleSource_id]
		print('Artigo do Journal ID = ' + str(journalSurce_id))

		link_cit = articles.LINK_CIT[articleSource_id]

		if link_cit == 'NaN':
			continue

		driver.get(link_cit)
		pages = int(driver.find_element_by_xpath('//*[@id="pageCount.top"]').text)
		k = 0

		for page in range(1, pages+1):
			soup = BeautifulSoup(driver.page_source, 'lxml')
			all_div = soup.find_all('div', class_ = 'search-results-item')
			all_div = all_div[0:int(len(all_div)/2)] # os resultados aparecem em duplicatas nas páginas

			for div in all_div:
				k = k + 1
				article_title = div.find('a', class_ = 'smallV110')

				if article_title != None and article_title['href'] != 'javascript:;': # existem alguns artigos sem links
					article_title = article_title.value.text
					year = int(div.find_all('span', class_ = 'data_bold')[-1].value.text[-4:]) 
					journal_title = div.find('span', id = 'show_journal_overlay_link_' + str(k)).a.span.value.text

					if journal_title not in list(journals_cit.TITLE):
						ID_J_CIT = ID_J_CIT + 1
						journals_cit.loc[ID_J_CIT] = [journal_title, 0, 0]
						journalTarget_id = ID_J_CIT
					else:
						journalTarget_id = journals_cit.index[journals_cit['TITLE'] == journal_title].tolist()[0]


					if article_title not in list(articles_cit.TITLE):
						ID_A_CIT = ID_A_CIT + 1
						articles_cit.loc[ID_A_CIT] = [article_title, journal_id, int(year), 0, 0]
						articleTarget_id = ID_A_CIT
					else:
						articleTarget_id = articles_cit.index[articles_cit['TITLE'] == article_title].tolist()[0]

					citations.loc[ID_CIT] = [articleSource_id, journalSurce_id, articleTarget_id, journalTarget_id, year]
					ID_CIT = ID_CIT + 1

					articles_cit.CITED_IN[articleTarget_id] = articles_cit.CITED_IN[articleTarget_id] + 1
					articles_cit.CITED_OUT[articleSource_id] = articles_cit.CITED_OUT[articleSource_id] + 1

					journals_cit.TOT_DEGREE[journalTarget_id] = journals_cit.TOT_DEGREE[journalTarget_id] + 1
					journals_cit.TOT_ART[journalSurce_id] = journals_cit.TOT_ART[journalSurce_id] + 1

			arrow = soup.find('a', class_ = 'paginationNext')['href']
			if arrow != 'javascript: void(0)': driver.get(arrow)

		articles_cit.to_csv('outputs/articles_cit.csv')
		journals_cit.to_csv('outputs/journals_cit.csv')
		citations.to_csv('outputs/citations.csv')

	return articles_cit, journals_cit, citations

