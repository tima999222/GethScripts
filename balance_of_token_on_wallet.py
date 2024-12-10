import sys
from web3 import Web3
import argparse
import json


# Функция для получения баланса токенов
def get_token_balance(w3, token_contract, wallet_address):
    balance = token_contract.functions.balanceOf(wallet_address).call()
    return balance


# Основная функция
def main():
    # Настройка парсинга аргументов
    parser = argparse.ArgumentParser(description="Получить баланс токенов на указанном кошельке")
    parser.add_argument("provider", help="URL провайдера Geth (например, http://127.0.0.1:8545)")
    parser.add_argument("token_address", help="Адрес контракта токена")
    parser.add_argument("wallet_address", help="Адрес кошелька")
    parser.add_argument("decimals", type=int, default=18, help="Количество десятичных знаков токена (по умолчанию 18)")

    args = parser.parse_args()

    # Подключение к Geth
    w3 = Web3(Web3.HTTPProvider(args.provider))
    if not w3.is_connected():
        print("Не удалось подключиться к Geth.")
        sys.exit(1)

    # Минимальная часть ABI для функции balanceOf
    token_abi = json.loads(
        '''[{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"uint256","name":"_initialSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint8","name":"decimals_","type":"uint8"}],"name":"setupDecimals","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]''')

    # Создание контракта
    token_contract = w3.eth.contract(address=args.token_address, abi=token_abi)

    # Получение баланса
    balance = get_token_balance(w3, token_contract, args.wallet_address)

    # Конвертация баланса в основной формат токенов
    balance_in_units = balance / (10 ** args.decimals)

    print(f"Баланс токенов на адресе {args.wallet_address}: {balance_in_units} токенов")


# Запуск основного кода
if __name__ == "__main__":
    main()
