from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from database.config_db import host, user, password, db_name
from database.bd import Balance, Database_curr, History

from config import TOKEN

balance = Balance(host, user, password, db_name)
history = History(host, user, password, db_name)
currency_db = Database_curr(host, user, password, db_name)

storage = MemoryStorage()


bot = Bot(TOKEN)
dp = Dispatcher(bot=bot,storage=storage)
