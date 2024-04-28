# Телеграм бот позволяющий проверять статус оплаты по номеру заказа.

# Usage
- `docker build -t sbp_bot .`
- `docker run {params} sbp_bot`

# docker params

`TOKEN` = токен бота

`ADMIN_ID` = телеграм id администратора

`MERCHANT_ID` = мерчант id для sbp

`SECRET_KEY` = секретный ключ для sbp

`USER` = юзер базы данных

`PASS` = пароль юзера

`HOST` = хост базы данных

`PORT` = порт базы данных

`NAME` = название базы данных
