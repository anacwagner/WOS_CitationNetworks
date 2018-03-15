from wos import *
from aux import * 


# LISTA DE ANOS DOS AQUIVOS JSON
year_list = range(2010,2017)

# DICIONÁRIO COM TODOS OS PERIÓDICOS EXTRAÍDOS DOS ARQUIVOS
journals_dic = allJournals(year_list)

# FATOR DE IMPACTO DOS PERIÓDICOS
IF = journalsMetrics(journals_dic, 'impact_factor', year_list)
IF.to_csv('outputs/IF.csv')

# EIGENFACTOR DOS PERIÓDICOS
EIG = journalsMetrics(journals_dic, 'eigen_factor', year_list)
EIG.to_csv('outputs/EIG.csv')


# TABELA COM INFORMAÇÕES E LINKS DE TODOS OS PERIÓDICOS DA CATEGORIA SELECIONADA
ID_J = len(journals_dic.keys())		# ID dos journals
journals = pd.DataFrame(index = range(1, ID_J+1), columns = ['TITLE', 'LINK'])
journals.TITLE = journals_dic.keys()
print('Todos os Periódico da Categoria Selecionada')
print(journals.TITLE)


# TABELA COM INFORMAÇÕES E LINKS DE TODOS OS ARTIGOS PUBLICADOS POR TODOS OS  PERIÓDICOS
articles = pd.DataFrame(columns = ['TITLE', 'LINK', 'JOURNAL_ID', 'YEAR', 'LINK_CIT'])


# LOGIN NO WoS PELO LOGIN DA FGV (FORA DA REDE ALUNOS)
# EM wos.py ESCOLHER A OPÇÃO IN OU OUT FGV
driver = login()

print('INÍCIO DA FASE 1 - Buscar Todos os Artigos Publicados Por Cada Periódico')

print('1.1 - Busca Avançada de Todos os Periódicos')

# LIMPA TODOS OS RESULTADOS DE BUSCA ARMAZENADOS NO HISTÓRICO 
# clearSearchHistory()

# BUSCA TODOS OS PERIÓDICOS - ARMAZENA TODOS OS RESULTADOS NO HISTÓRICO
advancedSearch(journals, year_list)

print('1.2 - Armazena os Links com os Resultados de Cada Pesquisa')

# EXTRAI TODOS OS LINKS DO HISTÓRICO DE PESQUISA E SALVA EM CSV
journals, driver = searchHistoryLinks(journals)
journals.to_csv('outputs/journals.csv')

print('1.3 - Listagem de Todos os Artigos de Cada Periódico')
# TODOS OS ARTIGOS ENCONTRADOS DO PERIÓDICO SELECIONADO

ID_J = len(journals)

for journal_id in range(1, ID_J+1):

	articles = allArticles(journals, articles)
	# A CADA ETAPA SALVA OS RESULTADOS EM CSV
	articles.to_csv('outputs/articles.csv')
	print('Artigos do Periódico ' + str(journal_id) + ' Armazenados!')

print('1.4 - Extraindo Informações de Todos os Artigos')

# PARA CADA JOURNAL, EXTRAI INFORMAÇÕES DE TODOS OS ARTIGOS
for journal_id in range(1, ID_J+1):

	articles = extractInfo(articles,journal_id)
	# A CADA ETAPA SALVA OS RESULTADOS EM CSV
	articles.to_csv('outputs/articles.csv')
	print('Informações dos Artigos do Periódico ' + str(journal_id) + ' Extraídas!')



print('INÍCIO DA FASE 2 - ARMAZENAR TODAS AS CITAÇÕES FEITAS POR CADA ARTIGO')

# TABELA COM INFORMAÇÕES GERAIS DOS PERIÓDICOS UTILIZADOS PARA A CONSTRUÇÃO DA REDE DE CITAÇÕES
journals_cit = pd.DataFrame(columns = ['TITLE', 'TOT_DEGREE', 'TOT_ART'])
journals_cit.TITLE = journals.TITLE 
journals_cit.TOT_DEGREE = 0
journals_cit.TOT_ART = 0

journals_cit.head()


# TABELA COM INFORMAÇÕES GERAIS DOS ARTIGOS UTILIZADOS PARA A CONSTRUÇÃO DA REDE DE CITAÇÕES
articles_cit = pd.DataFrame(columns = ['TITLE', 'JOURNAL_ID', 'YEAR', 'CITED_IN', 'CITED_OUT'])
articles_cit.TITLE = articles.TITLE
articles_cit.JOURNAL_ID = articles.JOURNAL_ID
articles_cit.YEAR = articles.YEAR
articles_cit.CITED_IN = 0
articles_cit.CITED_OUT = 0

articles_cit.head()


# TABELA COM INFORMAÇÕES GERAIS DAS CITAÇÕES
citations = pd.DataFrame(columns = ['SOURCE_A', 'SOURCE_J', 'TARGET_A', 'TARGET_J', 'YEAR'])


print('2.1 - Listando Todas as Citações Realizadas por Cada Artigo')
articles_cit, journals_cit, citations = allCitations(articles, articles_cit, journals_cit, citations)
# SALVA OS RESULTADOS EM CSV
articles_cit.to_csv('outputs/articles_cit.csv')
journals_cit.to_csv('outputs/journals_cit.csv')
citations.to_csv('outputs/citations.csv')