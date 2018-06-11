# IO20172018

## Przydatne komendy
### Przygotowanie środowiska wirtualnego
./venvdjango.sh

### Włączanie środowiska wirtualnego
source py_django/bin/activate

### Wyłączanie środowiska wirtualnego
deactivate

### Pobieranie obrazu splasha (docker)
sudo docker pull scrapinghub/splash

### Właczanie splasha
sudo docker run --restart always -p 8050:8050 -p 5023:5023 scrapinghub/splash --max-timeout=180

### Uruchamianie serwera
* Włączamy środowisko wirtualne
* Przeprowadzamy migracje, jeśli nie zrobiono tego wcześniej (niektóre crawlery są odpalane w trakcie migracji) </br>
python3 manage.py migrate
* Właczamy serwer </br>
python3 manage.py runserver

### Pobieranie danych ze strony
scrape crawl wp


### Dokumentacja i linki
* https://github.com/scrapy-plugins/scrapy-splash
* http://splash.readthedocs.io/en/stable/
* https://doc.scrapy.org/en/latest/
* http://ruddra.com/2016/01/03/django-1-7-scrapy/
