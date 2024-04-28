order_msg = """
Создан QR для заказа - `{order}`

qrId - `{qrId}`
payload - [ссылка на qr]({payload})
qrUrl - [ссылка на qr]({qrUrl})

Для оплаты - https://pay.raif.ru/pay/rfuture/#/
"""


wrong_order_msg = (
    "Неверный номер заказа. Проверьте введеный номер заказа и попробуйте еще раз."
)


status_msg = """
Заказ - `{order}`

qrId - `{qr_id}`
Статус - `{status}`
"""
