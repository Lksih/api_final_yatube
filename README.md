## Как запустить проект:

### Клонировать репозиторий:
```
git clone https://github.com/Lksih/api_final_yatube.git
```

### Перейти в директорию с проектом:
```
cd api_final_yatube
```

### Cоздать и активировать виртуальное окружение:

На Windows:
```
python -m venv env
```
```
source env/Scripts/activate
```

На Linux и macOS:
```
python3 -m venv env
```
```
source env/bin/activate
```

### Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

### Выполнить миграции:
На Windows:
```
python manage.py migrate
```

На Linux и macOS:
```
python3 manage.py migrate
```

### Запустить проект:
На Windows:
```
python manage.py runserver
```

На Linux и macOS:
```
python3 manage.py runserver
```
