# Система управления заказами и товарами

Проект представляет собой базу данных для управления товарами, категориями, клиентами и заказами с примером SQL-запросов для аналитики.
---

## Требования

- Docker и Docker Compose  
- Python 3.12 (если запускать локально без докера)

---
## Структура базы данных

### Таблицы

#### 1. Категории (`categories`)
```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    parent_id INT REFERENCES categories(id) ON DELETE CASCADE
);
```
---

#### 2. Номенклатура (`products`)
```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL CHECK (quantity >= 0),
    price NUMERIC(10,2) NOT NULL CHECK (price >= 0),
    category_id INT REFERENCES categories(id)
);
```
---

#### 3. Клиенты (`clients`)
```sql
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT
);
```
---

#### 4. Клиенты (`clients`)
```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    client_id INT NOT NULL REFERENCES clients(id),
    created_at TIMESTAMP DEFAULT NOW()
);
```
---

#### 5. Состав заказов (`order_items`)
```sql
CREATE TABLE order_items (
    order_id INT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id INT NOT NULL REFERENCES products(id),
    quantity INT NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (order_id, product_id)
);
```
---

# SQL-запросы
#### Сумма товаров по каждому клиенту
```sql
SELECT c.name AS client_name,
       SUM(oi.quantity * p.price) AS total_sum
FROM clients c
JOIN orders o ON o.client_id = c.id
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id
GROUP BY c.name;
```
---

#### Количество дочерних категорий 1-го уровня
```sql
SELECT parent.id AS category_id,
       parent.name AS category_name,
       COUNT(child.id) AS children_count
FROM categories parent
LEFT JOIN categories child ON child.parent_id = parent.id
GROUP BY parent.id, parent.name;
```
---

#### Топ-5 самых продаваемых товаров за последний месяц
```sql
SELECT p.name AS product_name,
       c.name AS category_name,
       SUM(oi.quantity) AS total_sold
FROM order_items oi
JOIN orders o ON o.id = oi.order_id
JOIN products p ON p.id = oi.product_id
JOIN categories c ON c.id = p.category_id
WHERE o.created_at >= NOW() - INTERVAL '1 month'
GROUP BY p.id, p.name, c.name
ORDER BY total_sold DESC
LIMIT 5;
```

---

#  Запуск с Docker Compose

Проект включает конфигурацию Docker Compose для быстрого развертывания:
Требования

- Docker

- Docker Compose

Переменные окружения

Создайте файл .env в корневой директории проекта:

```bash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=mydb
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/mydb
```
---

## Запуск проекта

1. Клонируйте репозиторий

2. Настройте переменные окружения в файле .env

3. Запустите контейнеры:

```bash
docker-compose up --build
```

---

# API Документация

## Документация API доступна по адресу: http://localhost:8000/docs

---

## Особенности:

- Валидация данных на уровне БД (CHECK constraints)

-  Каскадное удаление связанных записей

-  Автоматическая генерация первичных ключей

-  Поддержка иерархических категорий

-  Учет остатков товаров

-  История заказов с временными метками

-  Готовая Docker-конфигурация для разработки и тестирования
