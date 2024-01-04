from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
storage = MemoryStorage()

TOKEN = '5694078814:AAED5sPDPRJyRGUFMdLxJSyFsm9Li9g-muo'

bot = Bot(TOKEN)
dp = Dispatcher(bot=bot,storage=storage)
