import os

from sqlalchemy.ext.asyncio import create_async_engine
from database.models import ORDER, ADMIN_USER


DB_USER = os.getenv("USER")
DB_PASS = os.getenv("PASS")
DB_HOST = os.getenv("HOST")
DB_PORT = os.getenv("PORT")
DB_NAME = os.getenv("NAME")

ADMIN_ID = os.getenv("ADMIN_ID")


url = f"mssql+aioodbc://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_async_engine(url)


async def add_order(order, qr_id):
    statement = ORDER.insert().values(OrderNum=order, QrId=qr_id)
    async with engine.connect() as conn:
        await conn.execute(statement)
        await conn.commit()


async def get_order_qr(order):
    statement = (
        ORDER.select().where(ORDER.c.OrderNum == order).with_only_columns(ORDER.c.QrId)
    )
    async with engine.connect() as conn:
        res = await conn.execute(statement)
        res = res.fetchall()
    return res[0][0]


async def get_members():
    statement = (
        ADMIN_USER.select()
        .with_only_columns(ADMIN_USER.c.TgUserId)
        .where(ADMIN_USER.c.TgAdminId == ADMIN_ID)
    )
    async with engine.connect() as conn:
        res = await conn.execute(statement)
        res = [i[0] for i in res.fetchall()]
        res.append(ADMIN_ID)

    return res
