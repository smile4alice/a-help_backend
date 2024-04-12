# A-Help API + Admin

## Локальне налаштування

### **Віртуальне середовище**

Створіть віртуальне середовище за допомогою:

```
python -m venv venv
```
Або використовуючи альтернатівні рішення. Налаштуйте інтерпритатор вашої IDE на використання.

### **Встановлення залежностей**

Щоб встановити пакети виконайте наступні команди:

* Оновіть `pip` у віртуальному середовищі до останьої версії:
    ```
    (venv) > pip install --upgrade pip
    ```
* Встановіть пакети за допомогою файла для розробки:
    ```
    (venv) > pip install -r requirements-dev.txt
    ```
    > Офіційний пакет `flask-admin` на цей час має декілька багів. Ми вирішили цю проблему та запакували "фікс" у `.whl` дистрибутив, додавши його локально. Коли проблему буде вирішено офіційно - Вам надішлють інструкції, як оновити репозиторій.

### **База даних**
Для того щоб розпочати розробку нам потрібно запустити базу даних. З кореню проекту у терміналі Linux (або WSL) запустити:

```shell
docker-compose -f docker-compose-dev.yml up -d
```

### **Первина міграція даних до бази**:

Файл `.flaskenv` містить змінну оточення (Environment Variable) `DATABASE_URI` зі значенням 

```python
postgresql://local:dev%lop3R@127.0.0.1:5432/teamN
```
Де, `teamN` - це номер команди, що займалася розробкою.Це значення бази даних співпадає у `docker-compose-dev.yml` та у `.flaskenv`

Оновлення БД здійснене за допомогою декількох інструментів:
- Alembic
- SQL Alchemy

Щоб оновити вашу базу даних з моделями Flask (директорія ahelp/models) у вас є **дві** опції:

- За допомогою `Makefile` виконайте команди:
    ```
    (venv) > make upgrade-db
    ```
    - Вручну:
        ```
        (venv) > flask db upgrade
        ```
    ```
    (venv) > make start-develop
    ```
    - Вручну:
        ```
        (venv) > flask init
        (venv) > flask db migrate
        (venv) > flask db upgrade
    ```
    Пояснення :
    1. `flask db upgrade` - Виконує сгенерований скріпт міграції
    2. `flask init` - аналізує файл `manage.py` та додає користувачів за замовчуванням до Бази Даних
    3. `flask db migrate` - аналізує зміни у моделях (namespace models) та створює скріпт міграції на створення/зміну структури БД. Скріпт зберігається у директорію `migrations`


### **Запуск застосунку**

Для запуску застосунку використовуйте команду :

```
(venv) > flask run
```

Для запуску у режимі налагодження(debug) використовуйте аргумент `--debug`:
```
(venv) > flask --debug run
```
У цьому режимі кожна зміна у `.py` файл перезавантажує застосунок.

> [Адмінка](http://localhost:5000/admin) доступна за адресою:
`
http://localhost:5000/admin
`

Стандартні логін та пароль користувачів знаходяться у файлі `.flaskenv`

## Запуск тестів:

Для запуску тестів використовуйте утіліту [tox](https://tox.wiki/en/latest/#)
Запуск тестів через `tox`:
```
(venv) > tox -e test
```

## Робота з frontend командою:

Для того щоб frontend команда могла робити запити до нашого API, маємо дотриматись наступної процедури 

![Front End Interaction](docs/img/FrontEndIteraction.png)

> Приклад запитів на API можна знайти у файлі `test_login.http`

1. Виконати POST HTTP запит до сервера API за адерсою:
http://localhost:5000/auth/login
Content-Type: application/json

    У body запита додати `json` з логіном(username) та паролем(password)

    У результаті отримуємо `json` з токенами доступу до методів нашого `api`

    - "access_token" 
        Передаємо в кожен запит у якості HTTP header з ключем `Authorization`
    - "refresh_token"
        Потрібен для оновлення "access_token", коли строк дії закінчився 
        https://blog.loginradius.com/identity/refresh-tokens-jwt-interaction/

2. Виконати запит з HTTP Header на `endpoint` нашого api у форматі :
    
    Authorization: Bearer {access_token}
    > Bearer це ключове слово, яке має використовуватись разом з access_token
    https://reqbin.com/req/adf8b77i/authorization-bearer-header

# Налаштування
> Стандартні дані для налаштувань можна змінити у файлі`.flaskenv`
#### **Користувачі**
```
ADMIN_DEFAULT_LOGIN 
ADMIN_DEFAULT_PASSWORD
USER_DEFAULT_LOGIN
USER_DEFAULT_PASSWORD
```
    Пояснення:
    1. `ADMIN_DEFAULT..` - використовується адміністратором для доступу до панелі керування.
    2. `USER_DEFAULT..` - використувується для отримання токена доступу до передачі даних з серверу(Не має доступу до панелі керування).

#### **Платіжні системи**
**PayPal**
```
PAYPAL_MODE
PAYPAL_CLIENT_ID
PAYPAL_CLIENT_SECRET
```
    Пояснення:
    1. `PAYPAL_CLIENT_ID..` - ідентифікатор клієнта 
    2. `PAYPAL_CLIENT_SECRET` - Секретний ключ доступу
    3. `PAYPAL_MODE` - режим роботи Api. `sandbox` - Тестовий режим. `live` - робочий режим
    3. Щоб отримати `Live` ідентифікатор клієнта `CLIENT_ID`, вам потрібно мати бізнес-аккаунт. Якщо у вас ще немає бізнес-аккаунта необхідно його створити:
    https://wp-express-checkout.com/getting-live-and-sandbox-client-ids/
    
**Fondy**
```
FONDY_MERCHANT_ID
FONDY_SECRET_KEY
```
    Пояснення:
    1. `FONDY_MERCHANT_ID` - Ідентифікатор клієнта 
    2. `FONDY_SECRET_KEY` - Секретний ключ доступу
    3. Якщо у вас немає аккаунту Fondy його можна створити за посиланням:
    https://help.weblium.com/en-us/article/connecting-fondy-as-a-payment-method-1kb20ep/

#### **Пошта**
```
MAIL_USERNAME
MAIL_PASSWORD
MAIL_RECIPIENTS
```
    Пояснення:
    1. `MAIL_USERNAME..` - e-mail адреса аккаунту який використовуватиметься як сервісний для відправки повідомлень.
    2. `MAIL_PASSWORD..` - Ключ двохетапної автентефікації
    3. `MAIL_RECIPIENTS` - Поштові аккаунти, на які надходитимуть повідомлення із сервісного аккаунту в разі, коли відвідувач відправляє фідбек з сайту.
    - Зайти в google аккаунт.
    - На панелі навігації зліва вибрати `Безпека` 
    - Активувати двохетапну автентифікацію.
    - Повернутися на вкладку `Безпека`.
    - Перейти в меню "Паролі додатків" під полем "Двохетапна автентифікація".
    - Вибрати додаток "Пошта" і пристрій "Desktop Windows" і натиснути створити.
    - Скопіювати пароль зразу після генерації. Він використовуватиметься як ключ для відпправлення фідбеку з сайту.

## Додаткова інформація
#### **скрипт для видалення всіх таблиць з БД**
```
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO public;
```
> pgAdmin > пкм database > query tool > run script
#### **Тестові дані для платіжних систем**
**PayPal**
#### sandbox account
```
sb-toqdf25039523@personal.example.com
bg2hbJ=8
```
```
Card Type: Visa
Card Number: 4032032347557040
Expiration Date: 03/2026
CVV: 102
```
**Fondy**
```
Card Type: Visa
5555666644441111
Expiration Date: any/>2020
CVV: any
```