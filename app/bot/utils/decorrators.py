from functools import wraps
import database.database as db


def restricted(func):
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        allowed_users = await db.get_members()
        user_id = update.effective_user.id
        if str(user_id) in allowed_users:
            return await func(update, context, *args, **kwargs)
        else:
            pass

    return wrapped
