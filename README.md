# COVID-19-api
Esta api usa como fonte de dados o web site [WorldoMeter](https://www.worldometers.info/coronavirus/),
utilizando a raspagem web, mais conhecida como ***Web Scraping***.

A dois tipos de dados obtidos pela api:

- Numero de casos mundias, ```http://covid19.lucas-martins.com/api/v1/all_cases```  
- Numero de casos por paises, ```http://covid19.lucas-martins.com/api/v1/all_countries```

## Instalação

Requisitos:

- Python >= 3.6
- Python-venv

Primeiro passo é clonar o repositório:

```$ git clone https://github.com/lucasmcast/COVID19-api.git```

Ir para o diretório do projeto:

```$ cd COVID-19-api```

Criar um ambiente virtual:

```$ python3 -m venv venv```

Ativar o ambiente virtual no bash. Certifique que você esteja no diretório raiz do projeto:

```$ source venv/bin/activate```

Instalar as dependências do projeto:

```$ pip install -r requeriments/prod.txt```

Criar a variável de ambiante flask:

```$ export FLASK_APP=flasky.py```

Fazer deploy da apliação configurando todas as tabelas:

```$ flask deploy```

Executar projeto:

```$ flask run```


## Histórico de Lançamento

- 0.1.0
  - Verão inicial funcionando a api corretamente. Porém não foi implementado uma pagina para visualizar os dados.
  
 ## Objetivos
 
 - [x] Obter os dados da pagina web usando o método web Scraping
 - [x] Salvar dados obtidos no banco de dados.
 - [x] Criar tarefa para buscar dados em determinado tempo.
 - [x] Atualizar os dados em determinado tempo somente do dia atual, caso contrário, fazer a inserção.
 - [x] Disponibilizar os dados através da api.
 - [ ] Criar página para visualizar os dados obtidos.
 - [ ] Disponibilizar informações de países específicos, ```/api/v1/country/<país>```
 - [ ] Disponibilizar informações dos dados gerais e de países por data específica. ```/api/v1/date/country/<data>``` ou ```/api/v1/date/all_cases/<data>```
 - [ ] Implantar projeto.
 
## Meta

Lucas Martins de Castro - lucas.martins.c03@gmail.com
