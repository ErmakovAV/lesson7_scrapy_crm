# Начало работы со scrapy:
# 1. Корректное создание нового проекта.
# 2. Установка scrapy в терминале: PS C:\Users\Дмитрий\PycharmProjects\lesson6_scrapy> pip install scrapy
# 3. Создание проекта с указанием корневой папки, той, в которой мы сейчас находимся:
# PS C:\Users\Дмитрий\PycharmProjects\lesson6_scrapy> scrapy startproject jobparser .
# 4. Создание паука, важно указать метод genspider,
# и 2 параметра: название паука по имени домена и сам домен второго уровня:
# PS C:\Users\Дмитрий\PycharmProjects\lesson6_scrapy> scrapy genspider hhru hh.ru
# В директории spiders появился паук hhru.py, а в терминале:
# Created spider 'hhru' using template 'basic' in module:
#   jobparser.spiders.hhru


# Переходим к настройке файла: settings.py
# 1. Здесь помечаем все домены, с которыми работаем через "зпт": SPIDER_MODULES = ['jobparser.spiders']
# 2. Здесь указан непосредственно наш домен: NEWSPIDER_MODULE = 'jobparser.spiders'
# 3. Вносим версию c chrome://version:
# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
#              '(KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'
# 4. ROBOTSTXT_OBEY = False - отключаем, работает некорректно, сами будем писать логику сбора данных
# 5. Количество запросов в такт работы к серверу:
# CONCURRENT_REQUESTS = 16, лучше поставим по умолчанию - 16,
# может заблокироваться сайт на парсинг, в среднем на час
# 6. Задержка перед блоком запросов 5. в секундах: DOWNLOAD_DELAY = 0.5 выставим по минимуму
# 7. Работаем с куками, сайты будут относиться дружелюбней:
# COOKIES_ENABLED = True
# 8. Добавим логи, будут выливать подсказки в процессе работы:
# LOG_ENABLED = True
# LOG_LEVEL = 'DEBUG' # INFO WARN ERROR CRITICAL
# Остальные пока не трогаем, рассмотрим дальше во втором и третьем занятии

# Переходим в файл паука: hhru.py
# 1. Создаёт несколько точек входа: start_urls = ['http://hh.ru/']
# На hh.ru 10624 вакансии, возможности парсинга ограничиваются 2000 вакансиями.
# Попробуем разбить запросы по городам и получим уже более хорошие результаты.
# Для начала выставим поиск по 20 вакансий.
# Теряем на Москве, так как там 4800 вакансий, а с СПб уже потерь нет, там 1600 вакансий всего.
# далее через ЗПТ указываем интересующие нас города или другие объекты и соберём до 80% информации.
# 2. Теперь запрос составим к print(response.url) и вызовем паука в терминале, где hhru - имя нашего паука:
#    def parse(self, response):
#         print(response.url)
# PS C:\Users\Дмитрий\PycharmProjects\lesson6_scrapy> scrapy crawl hhru
# В результате запроса получим url адреса по которым проводили запросы:
# 2022-04-18 13:22:29 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://spb.hh.ru/search/vacancy?area=1&search_field=name&search_field=company_name&
# search_field=description&text=Python&order_by=relevance&search_period=0&items_on_page=20&no_magic=true&L_save_area=true> (referer: None)
# https://spb.hh.ru/search/vacancy?area=1&search_field=name&search_field=company_name&search_field=description&text=Python&order_by=relevance&search_peri
# od=0&items_on_page=20&no_magic=true&L_save_area=true
# 2022-04-18 13:22:30 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://spb.hh.ru/search/vacancy?area=2&search_field=name&search_field=company_name&
# search_field=description&text=python&order_by=relevance&search_period=0&items_on_page=20&no_magic=true&L_save_area=true> (referer: None)
# https://spb.hh.ru/search/vacancy?area=2&search_field=name&search_field=company_name&search_field=description&text=python&order_by=relevance&search_peri
# od=0&items_on_page=20&no_magic=true&L_save_area=true


# Для вызова паука в режиме отладки создадим ещё один файл
# внутри блока jobparser: runner.py - запускальщик
# Заполнили его:
# from twisted.internet import reactor
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging
# from scrapy.utils.project import get_project_settings
#
# from jobparser.spiders.hhru import HhruSpider
#
# if __name__ == '__main__':
#     configure_logging()
#     settings = get_project_settings()
#     runner = CrawlerRunner(settings)
#     runner.crawl(HhruSpider)
#
#     reactor.run()

# затем, заглушив: print(response.url) на hhru.py вызовем отладчик Debug, и пошлём 2 запроса:
# >>> response
# PyDev console: starting.
# <200 https://spb.hh.ru/search/vacancy?area=2&search_field=name&search_field=company_name&search_field=description&text=python&order_by=relevance&search_period=0&items_on_page=20&no_magic=true&L_save_area=true>
# >>> response.url
# 'https://spb.hh.ru/search/vacancy?area=2&search_field=name&search_field=company_name&search_field=description&text=python&order_by=relevance&search_period=0&items_on_page=20&no_magic=true&L_save_area=true'
# >>> response.text
# Сначала вернулся html код с area=2,
# Повторное обращение к >>> response.url откроет html код с area=1


# Далее в hhru вызовем:
# >>> response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href")
# а, затем, >>> response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").getall() - з
# десь получим полный список ссылок на вакансии одной страницы вызвав в Debug
# добавим наш запрос в переменную links и будем с ней работать



# В settings.ру раскомментируем пайплайн по написании кода
# ITEM_PIPELINES = {
#    'jobparser.pipelines.JobparserPipeline': 300,
# }
# Поставим заглушку на принте и вызовем отладчик от runner.py
# class JobparserPipeline:
#     def process_item(self, item, spider):
#         print()
#         return item
# Как только отладчик отработает, выполним запрос:
# >>> item
# и получим результат:
# {'name': 'Data Scientist',
#  'salary': ['от ', '300\xa0000', ' ', 'руб.', ' на руки'],
#  'url': 'https://spb.hh.ru/vacancy/54795186?from=vacancy_search_list&hhtmFrom=vacancy_search_list&query=python'}

# Установим МонгоДБ на пайплайнз:
# PS C:\Users\Дмитрий\PycharmProjects\pythonProjectAPI\lesson6_scrapy> pip install pymongo

# Зайдём через сайт Монго на страничку и посмотрим сохранённые вакансии, обновлялись 4 раза vacancy1204
# _id
# 625d6f750da7a1dcfd98900b
# name
# "Senior data scientist"
#
# salary
# Array
# url
# "https://spb.hh.ru/vacancy/54418768?from=vacancy_search_list&hhtmFrom=v…"
#
#
#
#
#
# _id
# 625d6f780da7a1dcfd98900c
# name
# "Middle QA специалист в команду Биллинга"
#
# salary
# Array
# url
# "https://spb.hh.ru/vacancy/47251783?from=vacancy_search_list&hhtmFrom=v…"
# _id
# 625d6f7c0da7a1dcfd98900d
# name
# "Senior Data Scientist"
#
# salary
# Array
# url
# "https://spb.hh.ru/vacancy/54780569?from=vacancy_search_list&hhtmFrom=v…"
# _id
# 625d6f800da7a1dcfd98900e
# name
# "Разработчик C/C++"
#
# salary
# Array
# url
# "https://spb.hh.ru/vacancy/54783772?from=vacancy_search_list&hhtmFrom=v…"
