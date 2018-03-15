# Web of Science (WoS)

Extração dos dados do WoS para montar uma rede de citações.

**OBS:** Os códigos foram feitos para serem rodados em uma VM com acesso à rede da FGV. Uma outra opção seria fazer isso de fora utilizando meu login de aluna, mas daria um pouco mais de trabalho. Outros links de acesso também podem ser utilizados, para isso basta alterar o `APPS` e a função `login` do arquivo [`wos.py`](https://github.com/anacwagner/WOS/blob/master/wos.py).

## Passo a Passo da Extração dos Dados

1. No topo da [página do WoS](http://apps-webofknowledge.ez91.periodicos.capes.gov.br/WOS_GeneralSearch_input.do?product=WOS&search_mode=GeneralSearch&SID=6AgbLVGDqDb6ylCWiE5&preferencesSaved=), ir em `Journal Citation Reports`. Abre uma nova guia.
2. Selecionar a opção de visualização dos *journals* `Categories By Rank`. 
3. Escolher uma categoria para montar a rede de citações (foi escolhida a `Mathematical & Computational Biology`).
4. Lista todos os *journals* desta categoria (foram selecionados somente os anos de `2010` a `2017`);
5. Para cada *journal*:
		i) Ir na página inicial e fazer uma `Advanced Search`. Digitar no campo de busca informações sobre o título (**SO** - `Publication Name`), anos a serem considerados (**PY** - `Year Published`) e o tipo de documento (**DT** - `Document Type`), no caso, artigo. 
		ii) Para cada artigo da lista gerada, listar todos os artigos citados, assim como informações relevantes para a construção da rede e possíveis consultas futura. 

## Instalações Requeridas

O Web Scraping do WoS foi feito utilizando [`Python 3`](https://www.python.org/downloads/). Os pacotes necessários são:

* [NumPy](http://www.numpy.org);
* [Pandas](https://pandas.pydata.org);
* [json](https://docs.python.org/3/library/json.html);
* [csv](https://docs.python.org/3/library/csv.html);
* [Selenium](http://www.seleniumhq.org);
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/);
* [time](https://docs.python.org/3/library/time.html);
* [getpass](https://docs.python.org/3.6/library/getpass.html) - para o caso de precisar um login.

Para utilizar o Selenium, é necessário de uma API [WebDriver](http://www.seleniumhq.org/projects/webdriver/), como por exemplo, o [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) (uma implementação que controla um navegador Chrome executado na máquina local) ou [PhantomJs](http://phantomjs.org/download.html). Foi utilizada a primeira opção. 

## Versão Teste x Versão Total

Ao tentar executar a versão teste para todos os **50.223 artigos** extraídos a partir das publicações dos **59 journals** entre os **anos de 2010 e 2017** pertencentes a categoria selecionada, alguns erros ocorreram e houve a necessidade de alterações em algumas funções. 

A primeira observação feita é que o WoS tem um limite de links a serem acessados. Dessa forma, houve a necessidade de realizar as buscas em partes de modo que ao atingir o limite, o Google Drive fechasse e reiniciasse o processo continuando de onde parou. Sendo assim, novos parâmetros e novas variáveis foram inseridas.

Outra ponto observado foi que ao reabrir o Google Drive, os links salvos ficam quebrados. Na verdade, eles estão associados aos resultados da `Advanced Search` já realizada anteriormente. Dessa forma, sempre que reiniciamos o processo, há a necessidade de refazer essa busca avançada. Outro ponto observado foi que como a busca envolve 59 periódicos, não tem como armazenar os resultados pela opção oferecida pelo próprio WoS, pois o limite é de 40 buscas. 

As funções que sofreram alterações foram: `allArticles`, `extractInfo` e `allCitations`. 

Além disso, as bases com as informações sobre as citações foram alteradas. Houve a necessidade de mudar os índices dos artigos e periódicos armazenados. Em vez de usar um sequencial numérico, os artigos passaram a utilizar como índice o código do próprio WoS e os periódicos, o ISSN. Dessa forma, a etapa de montagem da rede de citações pode ser dividida. 

## *Outputs*

