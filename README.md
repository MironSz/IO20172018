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
sudo docker run -p 8050:8050 -p 5023:5023 scrapinghub/splash


## Uruchamianie serwera
* Włączamy splasha
* Włączamy środowisko wirtualne
* Przeprowadzamy migracje, jeśli nie zrobiono tego wcześniej (niektóre crawlery są odpalane w trakcie migracji) </br>
python3 manage.py migrate
* Właczamy serwer </br>
python3 manage.py runserver


### Dokumentacja i linki
* https://github.com/scrapy-plugins/scrapy-splash
* http://splash.readthedocs.io/en/stable/
* https://doc.scrapy.org/en/latest/
