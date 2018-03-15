from selenium import webdriver
from bs4 import BeautifulSoup
import time

import getpass


# OUT FGV
#APPS = 'http://apps-webofknowledge.ez91.periodicos.capes.gov.br.sbproxy.fgv.br'
# IN FGV
APPS = 'http://apps-webofknowledge.ez91.periodicos.capes.gov.br'

driver = webdriver.Chrome(executable_path = r'/Users/Walter/Documents/chromedriver')


def login(local=None):

	if local == 'FGV':
		driver.get( APPS + '/WOS_GeneralSearch.do')

	else:
		driver.get('https://login.sbproxy.fgv.br/login?url=' + APPS + '/WOS_GeneralSearch.do')

		user = driver.find_element_by_xpath('//*[@id="user"]')
		user.send_keys(getpass.getpass('User:'))

		password = driver.find_element_by_xpath('//*[@id="pass"]')
		pswd = getpass.getpass('Password:')
		password.send_keys(pswd)

		login = driver.find_element_by_xpath('//*[@id="login-table"]/tbody/tr[3]/td/input[3]')
		login.click()

		time.sleep(30)

	driver.maximize_window()

	return driver


def advancedSearch(journals, year_list):
	'''
		Advanced Search by Publication Name (field_tags = 'SO').
		Add filters: PY - Publication Year AND DT - Document Type (Articles)

		INPUT:
			journals: data frame
			year_list: list of years 

		OUTPUT: 
			driver
	'''

	soup = BeautifulSoup(driver.page_source,'lxml')
	SID = soup.find('td', class_ = 'csi-checkemail-left-column').input['value']

	advancedSearch = APPS + '/WOS_AdvancedSearch_input.do?SID=' + SID + '&product=WOS&search_mode=AdvancedSearch'
	driver.get(advancedSearch)

	n = len(journals)

	year_from = str(year_list[0])
	year_to = '2017'


	for i in range(1, n+1):

		print('Advanced Search - Journal ' + str(i))

		search = driver.find_element_by_xpath('//*[@id="value(input1)"]')
		search.clear()
		search.send_keys('SO = (' + journals.TITLE[i] + ')' + ' AND PY = (' + year_from + '-' + year_to +') AND DT = (Article)')


		button = driver.find_element_by_xpath('//*[@id="searchButton"]/input')
		button.click()
		time.sleep(3)

	return driver


def clearSearchHistory():

	soup = BeautifulSoup(driver.page_source,'lxml')
	SID = soup.find('td', class_ = 'csi-checkemail-left-column').input['value']

	advancedSearch = APPS + '/WOS_AdvancedSearch_input.do?SID=' + SID + '&product=WOS&search_mode=AdvancedSearch'
	driver.get(advancedSearch)

	select_all = driver.find_element_by_xpath('/html/body/div[11]/form/table/tbody/tr[1]/th[6]/div[2]/input[1]').click()
	delete = driver.find_element_by_xpath('/html/body/div[11]/form/table/tbody/tr[1]/th[6]/div[2]/input[2]').click()
	time.sleep(5)

	return driver


def searchHistoryLinks(journals):
	'''
		INPUT:
			journals: data frame

		OUTPUT:
			journals: data frame
			driver
	'''

	n = len(journals)

	soup = BeautifulSoup(driver.page_source,'lxml')

	all_div = soup.find_all('div', class_ = 'historyResults')

	i = n
	for div in all_div:
	    journals.LINK[i] = APPS + div.a['href']
	    i = i - 1

	return journals, driver


def allArticles(journals, articles):
	'''
		INPUT:
			journals: data frame 
			articles: data frame

		OUTPUT:
			articles: data frame
	'''

	limit = 1200

	ID_J = len(journals)
	ID_A = len(articles) + 1
	k = 1

	if ID_A == 1: 
		ID_J_START = 1
	else:
		ID_J_START = articles.JOURNAL_ID[ID_A-1] + 1 

	for journal_id in range(ID_J_START, ID_J + 1):

		if k < limit:
			url = APPS + '/summary.do?product=WOS&parentProduct=WOS&search_mode=AdvancedSearch&qid=' + str(journal_id) + '&SID=6BO521EqrbfLAhtLGK1&page=1&action=changePageSize&pageSize=50'
			driver.get(url)

			pages = int(driver.find_element_by_xpath('//*[@id="pageCount.top"]').text)

			if k + pages + 1 > limit:
				k = limit 
				break

			print('Peiódico ' + str(journal_id) + ' - Total de Páginas: ' + str(pages))

			for page in range(1, pages+1):

				soup = BeautifulSoup(driver.page_source, 'lxml')
				all_div = soup.find_all('div', class_ = 'search-results-item')
				#all_div = all_div[0:int(len(all_div)/2)] # os resultados aparecem em duplicatas nas páginas

				for div in all_div:
					title = div.find('a', class_ = 'smallV110').value.text

					if title != None: # existem alguns artigos sem links
						#year = int(div.find_all('span', class_ = 'data_bold')[-1].value.text[-4:])
						year = div.find_all('span', class_ = 'label')[-1].next_sibling.value
						if year == None:
							if div.find('span', text = 'Acesso antecipado: ') == None:
								year = int(div.find_all('span', class_ = 'label')[-2].next_sibling.value.text[-4:])
							else:
								year = int(div.find('span', text = 'Acesso antecipado: ').findNextSiblings('span')[1].text)
						else:
							year = int(year.text[-4:])
						link = APPS + div.find('a', class_ = 'smallV110')['href']

						articles.loc[ID_A] = [title, link, journal_id, int(year), 'NaN']
						ID_A = ID_A + 1

				articles.to_csv('outputs/articles.csv')

				url = APPS + '/summary.do?product=WOS&parentProduct=WOS&search_mode=AdvancedSearch&qid=' + str(journal_id) + '&SID=6BO521EqrbfLAhtLGK1&page=' + str(page+1) + '&action=changePageSize&pageSize=50'
				driver.get(url)

			k = k + pages + 1
			print(len(articles[articles.JOURNAL_ID == journal_id]))

		else:
			break

	return articles


def extractInfo(articles, ID_A_START):
	'''
		INPUT:
			articles: data frame
			ID_A_START: id of journal chosen

		OUTPUT:
			articles: data frame
	'''

	limit=1200

	ID_A = len(articles)

	k = 1

	for i in range(ID_A_START, ID_A_START+ID_A):

		while k <= limit:
			driver.get(articles.LINK[i])
			soup = BeautifulSoup(driver.page_source,'lxml')

			#ref = soup.find('div', class_ = 'block-text-content').p.find_next_sibling().text.split('          ')[1][0]
			ref = soup.find('a', title = 'Visualizar a bibliografia deste registro')

			if ref == None:
				ref = '0'
			else:
				ref = ref.b.text

			if int(str(ref[0])) == 0:
				cited_link = 0
			else:
				cited_link = APPS + '/' + soup.find('a', title = 'Exibir a bibliografia deste registro')['href']

			articles.LINK_CIT[i] = cited_link
			break
		k = k + 1

	return articles


def allCitations(articles, journals, ID_A_START, articles_cit, journals_cit, citations):
	'''
		INPUT:
			articles: data frame
			journals: data frame
			ID_A_START: int
			articles_cit: data frame
			journals_cit: data frame
			citations: data frame

		OUTPUT:
			articles_cit: data frame
			journals_cit: data frame
			citations: data frame
			articleSource_id: int
	'''
	
	ID_A = len(articles)
	ID_A_INIC = articles.index[0]
	ID_CIT = len(citations) + 1
	ID_J_CIT = len(journals_cit)
	ID_A_CIT = len(articles_cit)

	limit = 500
	l = 1

	for articleSource_id in range(ID_A_START, ID_A_INIC+ID_A):
		print('Citações Feitas pelo Artigo ID = ' + str(articleSource_id))
		journalSource_id = articles.JOURNAL_ID[articleSource_id]
		print('Artigo do Journal ID = ' + str(journalSource_id))

		link_cit = articles.LINK_CIT[articleSource_id]

		if link_cit == '0': continue

		while l < limit:

			driver.get(link_cit)
			pages = int(driver.find_element_by_xpath('//*[@id="pageCount.top"]').text)
			k = 0

			if l + pages + 1> limit: 
				l = limit
				break

			for page in range(1, pages+1):
				soup = BeautifulSoup(driver.page_source, 'lxml')
				all_div = soup.find_all('div', class_ = 'search-results-item')
				#all_div = all_div[0:int(len(all_div)/2)] # os resultados aparecem em duplicatas nas páginas

				for div in all_div:
					k = k + 1
					article_title = div.find('a', class_ = 'smallV110')
					#article_title = div.find('span', class_ = 'reference-title')

					if article_title != None and article_title['href'] != 'javascript:;' and article_title.text[:21] != ' (Visualizar registro': # existem alguns artigos sem links
						journal_ISSN = div.find('p', class_ = 'FR_field sameLine')
						if journal_ISSN == None: continue

						journal_ISSN = journal_ISSN.value.text
						article_WOS = article_title['href'].split('WOS:')[-1].split('&')[0]
						article_title = article_title.value.text
						year = int(div.find_all('span', class_ = 'data_bold')[-1].value.text[-4:]) 
						journal_title = div.find('span', id = 'show_journal_overlay_link_' + str(k)).a.span.value.text
						
						if journal_ISSN not in list(journals_cit.index):
							ID_J_CIT = journal_ISSN
							journals_cit.loc[ID_J_CIT] = [journal_title, 0, 0]
							journalTarget_id = ID_J_CIT
						else:
							journalTarget_id = journal_ISSN


						if article_WOS not in list(articles_cit.index):
							ID_A_CIT = article_WOS
							articles_cit.loc[ID_A_CIT] = [article_title, journal_id, int(year), 0, 0]
							articleTarget_id = ID_A_CIT
						else:
							articleTarget_id = article_WOS

						articleSource_WOS = articles.ID_WOS[articleSource_id]
						journalSource_ISSN = journals.ISSN[journalSource_id]

						citations.loc[ID_CIT] = [articleSource_WOS, journalSource_ISSN, articleTarget_id, journalTarget_id, year]
						ID_CIT = ID_CIT + 1

						articles_cit.CITED_IN[articleTarget_id] = articles_cit.CITED_IN[articleTarget_id] + 1
						articles_cit.CITED_OUT[articleSource_WOS] = articles_cit.CITED_OUT[articleSource_WOS] + 1

						journals_cit.TOT_DEGREE[journalTarget_id] = journals_cit.TOT_DEGREE[journalTarget_id] + 1

				arrow = soup.find('a', class_ = 'paginationNext')['href']
				if arrow != 'javascript: void(0)': driver.get(arrow)

			break
		l = l + pages + 1
		journals_cit.TOT_ART[journalSource_ISSN] = journals_cit.TOT_ART[journalSource_ISSN] + 1

		articles_cit.to_csv('outputs/articles_cit_ID_J_%s.csv' % journalSource_id)
		journals_cit.to_csv('outputs/journals_cit_ID_J_%s.csv' % journalSource_id)
		citations.to_csv('outputs/citations_ID_J_%s.csv' % journalSource_id)

	return articles_cit, journals_cit, citations, articleSource_id