from sqlalchemy import Table, String, MetaData, Column, Integer, ForeignKey, Boolean

metadata = MetaData(schema="dbo")


ADMIN = Table(
    "Admin",
    metadata,
    Column("TgAdminId", Integer(), primary_key=True, autoincrement=False),
    Column("MerchantId", String()),
    Column("SecretKey", String()),
)


BOT = Table(
    "Bot",
    metadata,
    Column("BotId", Integer(), primary_key=True, autoincrement=True),
    Column("Description", String()),
    Column("Token", String()),
    Column("BotName", String()),
    Column("TgAdminId", ForeignKey(ADMIN.c.TgAdminId)),
)


USER = Table(
    "User",
    metadata,
    Column("TgUserId", Integer(), primary_key=True, autoincrement=False),
    Column("Name", String()),
    Column("IsWorking", Boolean()),
)


ADMIN_USER = Table(
    "AdminUser",
    metadata,
    Column("TgAdminId", ForeignKey(ADMIN.c.TgAdminId)),
    Column("TgUserId", ForeignKey(USER.c.TgUserId)),
)


ORDER = Table(
    "Order_",
    metadata,
    Column("OrderId", Integer(), primary_key=True),
    Column("OrderNum", String()),
    Column("QrId", String()),
)
