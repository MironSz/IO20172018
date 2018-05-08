# IO20172018

## Przydatne komendy
### Przygotowanie środowiska wirtualnego
./venvdjango.sh

### Włączanie środowiska wirtualnego
source py_django/bin/activate

### Wyłączanie środowiska wirtualnego
deactivate

## Uruchamianie serwera
* Włączamy środowisko wirtualne
* Przeprowadzamy migracje, jeśli nie zrobiono tego wcześniej (niektóre crawlery są odpalane w trakcie migracji) </br>
python3 manage.py migrate
* Właczamy serwer </br>
python3 manage.py runserver