from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from telegram import ReplyKeyboardMarkup, Update
from telegram.constants import ParseMode
import uuid
import re
import os
from bot.utils.messages import order_msg, wrong_order_msg, status_msg
from bot.utils.decorrators import restricted
import database.database as db
from bot.sbp_requests import create_qr, qr_status
from bot.logger.logger import logger

ORDER_INPUT = "order_input"
SEND_QR_STATUS = "send_qr_status"

MERCHANT_ID = os.getenv("MERCHANT_ID")
SECRET_KEY = os.getenv("SECRET_KEY")


@restricted
async def start_handler(upd: Update, ctx: ContextTypes):
    user_id = upd.effective_user.id

    logger.info(f"{user_id} запустил приложение.")
    keyboard = [["Создать QR"], ["Проверить статус оплаты"]]

    reply_markup = ReplyKeyboardMarkup(keyboard)

    await ctx.bot.send_message(
        upd.effective_chat.id,
        "Этот бот позволяет посмотреть статус оплаты qr sbp",
        reply_markup=reply_markup,
    )

    return ConversationHandler.END


@restricted
async def create_test_qr(upd: Update, ctx: ContextTypes):
    order = str(uuid.uuid4())
    user_id = upd.effective_user.id
    logger.info(f"{user_id} создал тестовый QR на заказ {order}.")

    data = {
        "order": order,
        "qrType": "QRDynamic",
        "sbpMerchantId": MERCHANT_ID,
        "amount": 100,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {SECRET_KEY}",
    }

    qr_data = await create_qr(data, headers)

    await db.add_order(str(order), qr_data["qrId"])

    logger.info(f'{qr_data["qrId"]} - id тестового QR для заказа {order}.')
    msg = order_msg.format(
        order=order,
        qrId=qr_data["qrId"],
        payload=qr_data["payload"],
        qrUrl=qr_data["qrUrl"],
    )

    await ctx.bot.send_message(upd.effective_chat.id, msg, ParseMode.MARKDOWN)
    return ConversationHandler.END


@restricted
async def get_qr_status(upd: Update, ctx: ContextTypes):
    await ctx.bot.send_message(upd.effective_chat.id, "Введите номер заказа.")
    return ORDER_INPUT


async def order_input(upd: Update, ctx: ContextTypes):
    order = upd.message.text
    order_pattern = r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"

    if order in (
        "/start",
        "/test_qr",
        "/qr_status",
        "Создать QR",
        "Проверить статус оплаты",
    ):
        pass

    elif not re.fullmatch(rf"{order_pattern}", order):
        await ctx.bot.send_message(
            upd.effective_chat.id,
            wrong_order_msg,
        )

    else:
        ctx.user_data["order"] = order
        qr_id = await db.get_order_qr(str(order))
        headers = {"Authorization": f"Bearer {SECRET_KEY}"}

        resp_json = await qr_status(qr_id, headers)
        status = resp_json["paymentStatus"]

        user_id = upd.effective_user.id
        logger.info(
            f"Пользователь {user_id} запросил статус для заказа {order}. Статус - {status}"
        )

        msg = status_msg.format(order=order, qr_id=qr_id, status=status)
        await ctx.bot.send_message(upd.effective_chat.id, msg, ParseMode.MARKDOWN)

    return ConversationHandler.END


async def order_status_interrupt(upd: Update, ctx: ContextTypes):
    user_data = ctx.user_data

    if "order" in user_data:
        del user_data["order"]

    user_data.clear()
    return ConversationHandler.END


def run_bot():
    TOKEN = os.getenv("TOKEN")
    bot = ApplicationBuilder().token(TOKEN).build()
    bot.add_handler(CommandHandler("start", start_handler))
    bot.add_handler(CommandHandler("test_qr", create_test_qr))
    bot.add_handler(MessageHandler(filters.Regex("Создать QR"), create_test_qr))
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("qr_status", get_qr_status),
            MessageHandler(filters.Regex("Проверить статус оплаты"), get_qr_status),
        ],
        states={
            ORDER_INPUT: [MessageHandler(filters.TEXT, order_input)],
        },
        fallbacks=[MessageHandler(filters.COMMAND, order_status_interrupt)],
    )
    bot.add_handler(conv_handler)
    bot.run_polling()
