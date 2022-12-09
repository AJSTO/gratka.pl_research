import scrapy
import uuid
import os
from datetime import date
import re
import psycopg2

from scrapy import signals
from pydispatch import dispatcher
#import json # If wanted to save records in json file.


class GratkaSpider(scrapy.Spider):
    # Connecting to database.
    name = "gratka"
    start_urls = ["https://gratka.pl/motoryzacja/osobowe?page=1"]
    conn = psycopg2.connect(
        database=os.getenv('POSTGRES_DB'),
        user='postgres',
        password=os.getenv('PASSWORD'),
        host='localhost',
        port='5432')
    cur = conn.cursor()
    # Global values.
    page = 1  # Starting page, will be increased through crawling.
    scraped_advertisments = {}  # Dict for capturing metadata.
    index_record = 0  # Index of records in dict of captured metadata.

    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def parse(self, response):
        for ad in response.css("div.listing__teaserWrapper > a::attr('href')"):
            advertise_url = ad.get()
            yield scrapy.Request(url=advertise_url, callback=self.parseAdPage)
        self.page += 1
        next_page = f'https://gratka.pl/motoryzacja/osobowe?page={self.page}'
        yield response.follow(next_page, callback=self.parse)

    def parseAdPage(self, response):
        # Getting metadata.
        miasto = response.css(
            'ul.parameters__singleParameters > li > b.parameters__value > a::text'
                                ).getall()[0]
        wojewodztwo = response.css(
            'ul.parameters__singleParameters > li > b.parameters__value > a::text'
                                    ).getall()[-1]
        cena = response.css('span.priceInfo__value::text').get()
        cena = cena.strip('\n ')
        cena = cena.replace(' ', '')
        marka = response.css('a.breadcrumbs__link::text').getall()[3]
        model = response.css('a.breadcrumbs__link::text').getall()[-1]
        model = model.strip(marka)
        id_gratka = re.search(r'\d{5,8}', str(response)).group()
        id_uuid = uuid.uuid4()
        ad_info_basic = {
            'id_uniq': id_uuid,
            'id_gratka': id_gratka,
            'miasto': miasto,
            'wojewodztwo': wojewodztwo,
            'cena': cena, #### GDY PUSTA WARTOSC DAC JAKIES ROZWIAZANIE.
            'marka': marka,
            'model': model.replace("'", "").strip(),
            'link': response.url,
            'date_of_scrap': str(date.today())
                         }
        params = response.css('ul.parameters__singleParameters > li > span::text').getall()
        params = [elem.lower().replace(' ', '_').replace('[', '').replace(']', '')
                  for elem in params if elem not in ['Lokalizacja', 'Dodane', 'Zaktualizowane']]
        describe = response.css('ul.parameters__singleParameters > li > b::text').getall()
        describe = [elem for elem in describe if not re.match('\n|,| ', elem)]

        ad_info = dict(zip(params, describe))
        ad_info = dict(ad_info_basic, **ad_info)

        # Formatting string be ready loaded like numeric: price, mileage, engine size.
        try:
            ad_info['pojemność_silnika_cm3'] = ad_info['pojemność_silnika_cm3'].strip(' cm')
        except KeyError:  # If there is no that type of metadata in scrapped values skip.
            pass
        try:
            ad_info['cena'] = float(ad_info['cena'].replace(',', '.') or 0)
        except KeyError:
            pass
        try:
            ad_info['przebieg'] = ad_info['przebieg'].replace(',', '.')
        except KeyError:
            pass
        # Saving HTML file of each ad, adding metadata to dict of dict, increase index.
        self.scraped_advertisments[self.index_record] = ad_info
        self.index_record += 1
        file = open(f'/gratkascrap/HTML_FILES/{id_uuid}.html', 'wb')
        file.write(response.body)

    def spider_closed(self, spider):
        # Lines created to eventually drop results to json file.
        #with open('/gratkascrap/HTML_FILES/ogloszenia.json', 'w') as fp:
            #json.dump(self.scraped_advertisments, fp)

        data_to_load = self.scraped_advertisments.values()  # From dict of dict getting dict.
        for record in data_to_load:
            try:
                self.cur.execute(
                f'''INSERT INTO auctions({', '.join(map(str, record.keys()))}) VALUES{tuple(record.values())}'''
                                )
                self.conn.commit()  # Committing queries.
            except:
                pass

      ### STAN NA 02.12.2022R GODZ 22:00 ### BACKUP
        """
        import scrapy
import uuid
import os
from datetime import date
import re
import psycopg2

from scrapy import signals ###
from pydispatch import dispatcher ###
import json ##

class GratkaSpider(scrapy.Spider):
    name = "gratka"
    start_urls = ["https://gratka.pl/motoryzacja/osobowe?page=1"]
    page = 1
    results = []
    reess ={}###
    inde = 0 ###
    conn = psycopg2.connect(
        database='cars-db',
        user='postgres',
        password=os.getenv('PASSWORD'),
        host='localhost',
        port='5432')
    cur = conn.cursor()
    ##########
    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)
########
    def parse(self, response):
        for ad in response.css("div.listing__teaserWrapper > a::attr('href')"):
            advertise_url = ad.get()
            yield scrapy.Request(url=advertise_url, callback=self.parseAdPage)

        for record in self.results:
            self.cur.execute(
                f'''INSERT INTO auctions({', '.join(map(str, record.keys()))}) VALUES{tuple(record.values())}'''
            )
        self.conn.commit()
        self.results = []

        self.page += 1
        next_page = f'https://gratka.pl/motoryzacja/osobowe?page={self.page}'
        yield response.follow(next_page, callback=self.parse)

    def parseAdPage(self, response):
        miasto = response.css('ul.parameters__singleParameters > li > b.parameters__value > a::text').getall()[0]
        wojewodztwo = response.css('ul.parameters__singleParameters > li > b.parameters__value > a::text').getall()[-1]
        cena = response.css('span.priceInfo__value::text').get()
        cena = cena.strip('\n ')
        cena = cena.replace(' ', '')
        marka = response.css('a.breadcrumbs__link::text').getall()[3]
        model = response.css('a.breadcrumbs__link::text').getall()[-1]
        model = model.strip(marka)
        id_gratka = re.search(r'\d{8}', str(response)).group()
        id_uuid = uuid.uuid4()
        ad_info_basic = {
            'id_uniq': id_uuid,
            'id_gratka': id_gratka,
            'miasto': miasto,
            'wojewodztwo': wojewodztwo,
            'cena': cena,
            'marka': marka,
            'model': model.replace("'", ""),
            'link': response.url,
            'date_of_scrap': str(date.today())
                         }
        params = response.css('ul.parameters__singleParameters > li > span::text').getall()
        params1 = response.css('ul.parameters__singleParameters > li > span::text').getall() ####
        params = [elem.lower().replace(' ', '_').replace('[', '').replace(']', '')
                  for elem in params if elem not in ['Lokalizacja', 'Dodane', 'Zaktualizowane']]
        describe = response.css('ul.parameters__singleParameters > li > b::text').getall()
        describe1 = response.css('ul.parameters__singleParameters > li > b::text').getall() ####
        describe = [elem for elem in describe if not re.match('\n|,| ', elem)]
        ad_info = dict(zip(params, describe))
        ad_info = dict(ad_info_basic, **ad_info)
        
        self.results.append(ad_info)
        self.reess[self.inde] = dict(zip(params1,describe1)) #####
        self.inde+= 1 #####
        file = open(f'/gratkascrap/HTML_FILES/{id_uuid}.html', 'wb')
        file.write(response.body)
#################################
    def spider_closed(self, spider):
        with open('/gratkascrap/HTML_FILES/secik.json', 'w') as fp:
            json.dump(self.reess, fp)
            ######
        
        """
        """
class GratkaSpider(scrapy.Spider):
    name = "gratka"
    start_urls = ["https://gratka.pl/motoryzacja/osobowe?page=310"] #zmienic na 1
    page = 310 # dodane |zmienic na 1
    results = []
    conn = psycopg2.connect(database='cars-db', user='postgres', password='gratka_pass', host='localhost', port='5432')
    cur = conn.cursor()


    def parse(self, response):
        for ad in response.css("div.listing__teaserWrapper > a::attr('href')"):
            advertise_url = ad.get()
            time.sleep(1.5)
            yield scrapy.Request(url=advertise_url, callback=self.parseAdPage)

        self.cur.execute('SELECT id FROM auctions')  # sprawdzenie czy to id istnieje w bazie
        ids = self.cur.fetchall()
        ids = np.array(sum(ids, ()))

        for record in self.results:
            if record['id'] not in ids:
                self.cur.execute(f'''INSERT INTO auctions({', '.join(map(str, record.keys()))}) 
                                        VALUES{tuple(record.values())}''')
                self.conn.commit()
            else:
                continue
        self.results = []

        self.page+=1
        next_page = f'https://gratka.pl/motoryzacja/osobowe?page={self.page}'
        yield response.follow(next_page, callback=self.parse)

        '''
        try:
            self.page+=1
            if self.page < 400: #only for testing for shorten time.
                next_page = f'https://gratka.pl/motoryzacja/osobowe?page={self.page}'
                yield response.follow(next_page, callback=self.parse)
        except:
            pass
        '''    

    def parseAdPage(self, response):
        miasto = response.css('ul.parameters__singleParameters > li > b.parameters__value > a::text').getall()[0]
        wojewodztwo = response.css('ul.parameters__singleParameters > li > b.parameters__value > a::text').getall()[-1]
        cena = response.css('span.priceInfo__value::text').get()
        cena = cena.strip('\n ')
        cena = cena.replace(' ', '')
        marka = response.css('a.breadcrumbs__link::text').getall()[3]
        model = response.css('a.breadcrumbs__link::text').getall()[-1]
        model = model.strip(marka)
        #ID = response.css('p.contact__offerId > span::text').get() #wyrzucone ze wzgledu na blad na str 22, bylo brak id aukcji w prawym gornym okienku
        #ID = re.split(r'/', str(response))[-1] # do sprawdzenia
        ID = re.search(r'\d{8}',str(response)).group()
        ad_info_basic = {'id': ID,'miasto': miasto, 'wojewodztwo': wojewodztwo,
                         'cena': cena, 'marka': marka, 'model': model.replace("'","")}
        params = response.css('ul.parameters__singleParameters > li > span::text').getall()#[1:-2]
        params = [elem.lower().replace(' ', '_').replace('[','').replace(']','')
                  for elem in params if elem not in ['Lokalizacja','Dodane','Zaktualizowane']]
        describe = response.css('ul.parameters__singleParameters > li > b::text').getall()#[4:]
        describe = [elem for elem in describe if not re.match('\n|,| ',elem)]
        ad_info = dict(zip(params, describe))
        ad_info = dict(ad_info_basic, **ad_info)

        self.results.append(ad_info)  
        """
