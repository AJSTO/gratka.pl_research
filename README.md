## 👨‍💻 Built with
<img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" /> <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white"/> <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" /> <img src="https://img.shields.io/badge/Jupyter-F37626.svg?&style=for-the-badge&logo=Jupyter&logoColor=white" /> <img src="https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white" /> <img src="https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white" />

##  Descripction about project

This project is created for crawling metadata from auction service with 🚗cars: [Gratka.pl](https://gratka.pl/motoryzacja/osobowe). Metadata like a:
```bash
'marka', 'model', 'cena', 'miasto', 'wojewodztwo', 'stan_techniczny', 'przebieg', 'rodzaj_ogłoszenia', 
'do_negocjacji', 'typ_nadwozia', 'stan_pojazdu', 'rok_produkcji', 'rodzaj_paliwa', 'pojemność_silnika_cm3', 
'moc_silnika', 'skrzynia_biegów', 'zarejestrowany_w_polsce', 'kraj_pierwszej_rejestracji', 'kolor', 
'liczba_drzwi', 'liczba_miejsc', 'numer_vin', 'ważny_przegląd', 'link'
```
This data when spider will end his job will be stored inside the PostgreSQL.
Next step will be data cleansing and visualistaion, which are made with jupyter notebook.

This project using 3 Docker containers:
- **Container with Python and Scrapy**
    - Created gratka spider which inheriting from class scrapy.Spider (Scrapy script created to crawl metadata from every car selling advertisment and
    also saving a HTML file for each ad - in folder)
- **Container with PosgreSQL**

- **Container Jupyter Notebook**
    - Notebook created to cleansing and visualise a data, used libraries: 
      - pandas
      - geopandas
      - numpy
      - matplotlib
      - seaborn
      - pylab
      - psycopg2

## 🌲 Project tree
```bash
├── Database
│   └── create_table.sql
├── docker-compose.yml
├── gratkascrap
│   ├── Dockerfile
│   ├── HTML_FILES
│   │   └── 00a3d318-6fcd-4bb8-9bd7-6c1b7ac4d69c.html
│   ├── __init__.py
│   ├── gratkascrap
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-39.pyc
│   │   │   └── settings.cpython-39.pyc
│   │   ├── items.py
│   │   ├── middlewares.py
│   │   ├── pipelines.py
│   │   ├── settings.py
│   │   └── spiders
│   │       ├── __init__.py
│   │       ├── __pycache__
│   │       │   ├── __init__.cpython-39.pyc
│   │       │   └── gratka.cpython-39.pyc
│   │       └── gratka.py
│   ├── requirements.txt
│   └── scrapy.cfg
├── notebook
│   ├── Dockerfile
│   ├── __pycache__
│   │   └── dash.cpython-310.pyc
│   ├── data_visualisation.ipynb
│   ├── requirements.txt
│   ├── voivodeship.shp
│   └── voivodeship.shx
└── .env-sample
```
## 🔑 Setup your local variables
To run properly this project you should assign a environmental variables in file .env.

In this repo is created .env-sample with variables used to run containers. You need to assign variables below in your .env file:
```bash
DATABASE_PASSWORD=
JUPYER_TOKEN=
POSTGRES_DB=
```
## ⚙️ Run Locally
- Clone the project
- Go to the project directory:
Type in CLI:
```bash
  $ ls
```
You should see this:
```bash
Database    docker-compose.yml	gratkascrap     notebook
```
Change direction to create dockerfile of scrapy:
```bash
  $ cd gratkascrap
```
Build scrapy image: 🚨to run this command docker should be running on your machine🚨
```bash
  $ docker build -t scrapy_gratka .     
```
Change direction to main directory:
```bash
  $ cd ..
```
Change direction to create dockerfile of notebook:
```bash
  $ cd notebook
```
Build notebook image:
```bash
  $ docker build -t notebook_gratka .     
```
Change direction to run docker composer:
```bash
  $ cd ..
```
Run dockercomposer:
```bash
  $ docker-compose up
```
##  📊Data cleansing and visualisation
**Now all three containers are running, it will take about 15-20 minutes for scrapy to crawl all pages, you will see in terminal when scrapy finishes job.**
**When scrapy finished you should open jupyter lab via localhost, type in your browser:**
```bash
  localhost:8888
```
🚨In case the notebook requires a token pass a value which was assigned to JUPYER_TOKEN in .env🚨

Next choose a file 🗒️data_visualisation.ipynb and run all cells to see data analyse.

