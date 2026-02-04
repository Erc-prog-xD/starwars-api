# Star Wars API – PowerOfData

Bem-vindo à **Star Wars API**, uma plataforma para fãs da saga **Star Wars**.  
A API permite explorar informações detalhadas sobre **filmes, personagens, planetas, naves, veículos e espécies**, com filtros avançados e estatísticas.

---

## Tecnologias

- **Python 3.14**
- **FastAPI**
- **Pydantic** (para schemas e validação de dados)
- **Google Cloud Platform** (Cloud Functions + API Gateway)
- **SWAPI** ([https://swapi.dev/](https://swapi.dev/)) como fonte de dados

---
## Explicando uso do Cache

- Foi feito a utilização de cache para fazer o get de todos os tipos no swapi e guarda-los em uma variavel de cache
- Com isso as consultas ficam mais rapidas pois ao invés de enviar requisições a todo momento, enviamos apenas uma vez e tudo de informação fica guardado em uma variavel do próprio codigo para ser utilizada pela função fetch_data().


---
## src/schemas/types_class.py
-   Aqui eu utilizei para criar classes para utilizar nas minhas request e reponses.
---


## src/services/swapi_services.py
- Aqui foi onde houve as chamadas para o swapi e feita a logica para o salvamento em cache
---


## src/utils/filters.py
- Nessa parte foi onde eu fiz a logica de filtros para meus endpoints.
---

Endpoints principais
## Default
- GET **"/"** Usado para obter os dados do swapi, é possível filtrar pelo type e pelo name ou title de cada dado.

## Films

- GET **/films/list_films_by_filters**	Lista filmes com filtros: title, director, producer, episode_id, release_date e nome do personagem (name_people), além de fazer a ordenação e paginação
- GET **/films/by-id/{id}**	Busca filme por ID
- GET **/films/list_with_counts**	Lista filmes com contagem de personagens, planetas, naves, veículos e espécies
- GET **/films/stats/overview**	Estatísticas gerais: total de filmes, episódios e títulos
- GET **/films/stats/movies_most_species**	Filmes com mais espécies
- GET **/films/stats/starships_useds_in_movies**	Filmes com mais starships
- GET **/films/stats/timeline**	Linha do tempo dos filmes
- GET **/films/{id}/characters**	Lista personagens de um filme específico

## Peoples
Endpoint
- GET **/peoples/by-id/{id}**	Busca peoples por ID
- GET **/people/list_people_by_filters**	Lista personagens com filtros: name, gender, hair_color, eye_color, skin_color, birth_year. Além de fazer a ordenação e paginação.
- GET **/people/gender_count**	Estatísticas de gênero (masculino, feminino, sem gênero especificado)
- GET **/people/statistics_height_people**	Estatísticas de altura (média, mínima, máxima) por gênero
- GET **/people/statistics_mass_people**	Estatísticas de massa (média, mínima, máxima) por gênero

## Planets
Endpoint
- GET **/planets/by-id/{id}**	Busca planets por ID
- GET **/planets/list_planets_by_filters** Lista planets com filtros: name, climate, terrain, min_population. Além de fazer a ordenação e paginação.
- GET **/planets/population_statistics** Pega todos os planets e faz as estatísticas numericas dos dados, da população e do planeta em si.
- GET **/planets/top_population** Busca os planets e ranqueia conforme o tamanho da população.
- GET **/planets/top_residents** Ranqueia os planets que tem mais residents nos seus dados

## Starships
Endpoint
- GET **/starships/by-id/{id}**	Busca starships por ID
- GET **/starships/list_starships_by_filters** Lista starships com filtros: name, model, manufacturer, starship_class. Além de fazer a ordenação e paginação.
- GET **/starships/stats/overview** Overview das starships e classes de distribuição
- GET **/starships/stats/most_appared_in_movies** starships que mais apareceram nos filmes

## Species
Endpoint
- GET **/species/by-id/{id}**	Busca species por ID
- GET **/species/list_species_by_filters** Lista species com filtros: name, classification, designation, language. Além de fazer a ordenação e paginação.
- GET **/species/stats/overview** Overview das species sobre classifications e designations
- GET **/species/stats/height** Estátisticas sobre a altura das species
- GET **/species/stats/lifespan** Estátisticas sobre o tempo de vida das species
- GET **/species/stats/most_appared_in_movies** species que mais apareceram nos filmes
- GET **/species/stats/people** Mostra a specie de cada people
- GET **/species/stats/people** Lista a linguagem de cada specie

## Vehicles
Endpoint
- GET **/vehicles/by-id/{id}**	Busca vehicles por ID
- GET **/vehicles/list_vehicles_by_filters** Lista vehicles com filtros: name, model, manufacturer, vehicle_class. Além de fazer a ordenação e paginação.
- GET **/vehicles/stats/overview** Overview das vehicles sobre vehicle_classes e manufacturers
- GET **/vehicles/stats/cost** Estátisticas sobre o custo dos vehicles
- GET **/vehicles/stats/cargo** Estátisticas sobre a capacidade de carga dos vehicles
- GET **/vehicles/stats/speed** Estátisticas sobre a velocidade dos vehicles
- GET **/vehicles/stats/most_appared_in_movies** vehicles que mais apareceram nos filmes


## GCP link
https://starwars-api-936602274704.southamerica-east1.run.app/docs

## Rodando a API localmente

1. Clone o projeto:

```bash
git clone <seu-repositorio>
cd starwars-api/src

python -m venv venv
# Windows
source venv/Scripts/activate
# Linux / Mac
source venv/bin/activate

pip install -r requirements.txt

uvicorn main:app --reload


## Estrutura do Projeto

```text
starwars-api/
├── .dockerignore
├── .git/
├── .vscode/
├── Dockerfile
├── README.md
└── src/
    ├── .gitignore
    ├── main.py
    ├── requirements.txt
    ├── routers/
    ├── schemas/
    ├── services/
    ├── utils/
    └── venv/
