# api_yamdb

api_yamdb

# api_yamdb project (v1)

#### Описание

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку. Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка».

#### Установка

Клонировать репозиторий приложения:

```
git clone git@github.com:kgdpete2022/api_yamdb.git
```

Перейти в корневой каталог:

```
cd api_yamdb
```

Создать виртуальное окружение:

```
python3 -m venv venv
```

Активировать виртуальное окружение:

- Linux/macOS

```
source venv/bin/activate
```

-Windows

```
source venv/scripts/activate
```

Обновить pip:

```
python3 -m -pip install --upgrade pip
```

Установить зависимость из файла requirements.txt:

```
pip install -r requirements.txt
```

Произвести миграции:

```
python3 manage.py migrate
```

Импортировать тестовые данные в базу данных:

```
python3 manage.py import_csv_data
```

Запустить проект:

```
python3 manage.py runserver
```

#### Примеры запросов API

Получение списка всех категорий:

```
GET /api/v1/categories/
```

Получение списка всех жанров

```
GET /api/v1/genres/
```

Получение списка всех произведений:

```
GET /api/v1/titles/
```

Получение информации о произведении:

```
GET /api/v1/titles/{titles_id}/
```
