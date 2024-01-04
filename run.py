from aiogram import executor
from handler import commands, statistic, costs, balance
from create import dp


def start():
    statistic.register_cost(dp)
    balance.register_balance(dp)
    commands.register_commands(dp)
    costs.register_cost(dp)


if __name__ == "__main__":
    print('БОТ УСПІШНО ЗАПУСТИВСЯ')
    start()
    executor.start_polling(dp, skip_updates=True)
    