# Estruturas dos *Data Frames* 

Os *outputs* são salvos em formato `csv`. 

## *Journals*
Temos dois data frames que armazenam os periódicos: **(1)** o primeiro com os *journals* que estamos fazendo as buscas (todos os *journals* extraídos da categoria selecionada) e **(2)** o outro com todos os *journals* utilizados na construção da rede de citações.

Para `journals`, temos:

* `TITLE` - nome do periódico;
* `LINK` - resultado da busca por periódico (resultado de todos os artigos publicados pelo periódico).

O `journals_cit` começa a partir de uma cópia do `journals` para que se mantenham os ID's já utilizados. Só será iniciado depois de finalizada a estrutura de `journals`. Para `journals_cit`, temos:

* `TITLE` - nome do periódico;
* `TOT_DEGREE` - grau de entrada total;
* `TOT_ART` - total de artigos publicados.

### Fator de Impacto

O data frame `FI`, contém o fator de impacto (FI) de cada *journal* em cada ano escolhido para a extração. 

### *Eigenfactor*

O data frame `EIG`, contém o *eigenfactor* de cada *journal* em cada ano escolhido para a extração. 


## Artigos

Temos dois data frames que armazenam os artigos: **(1)** o primeiro com os artigos que estamos fazendo as buscas (todos os atrtigos publicados por cada *journal* extraído da categoria selecionada) e **(2)** o outro com todos os artigos utilizados na construção da rede de citações.

Para `articles`, temos:

* `TITLE` - nome do artigo;
* `LINK` - *link* com as informações do artigo;
* `JOURNAL_ID` - ID do journal que publicou o artigo;
* `YEAR` - ano que o artigo foi publicado;
* `LINK_CIT` - *link* com as informações dos artigos que citou.

O `articles_cit` começa a partir de uma cópia do `articles` para que se mantenham os ID's já utilizados. Só será iniciado depois de finalizada a estrutura de `articles`. Para `articles_cit`, temos:

* `TITLE` - nome do artigo;
* `JOURNAL_ID` - ID do *journal* que publicou o artigo;
* `YEAR` - ano que o artigo foi publicado;
* `CITED_IN` - quantidade de citações recebidas (artigos que citaram ele);
* `CITED_OUT` - quantidade de citações realizadas (artigos que ele citou - que usou em sua referência).

## Citações

A construção da rede de citações, ocorre a partir da finalização de `articles_cit`. O data frame `citations` contém as informações da rede.

* `SOURCE_A` - ID do artigo que está citando;
* `SOURCE_J` - ID do *journal* que contém o artigo que está citando;
* `TARGET_A` - ID do artigo que está sendo citado;
* `TARGET_J` - ID do *journal* que contém o artigo que está sendo citado;
* `YEAR` - ano da citação.