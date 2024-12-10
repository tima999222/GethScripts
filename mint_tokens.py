import sys
import argparse
from web3 import Web3
import json


def mint_tokens(rpc_url, private_key, contract_address, to_address, amount):
    # Подключение к Geth
    web3 = Web3(Web3.HTTPProvider(rpc_url))

    if not web3.isConnected():
        print("Ошибка подключения к RPC")
        sys.exit(1)

    # Проверка валидности адресов
    if not web3.isAddress(contract_address) or not web3.isAddress(to_address):
        print("Один из адресов некорректен")
        sys.exit(1)

    # Чтение ABI контракта (должен быть доступен в локальном файле)
    token_abi = json.loads(
        '''[{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"uint256","name":"_initialSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint8","name":"decimals_","type":"uint8"}],"name":"setupDecimals","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]''')


    # Создание объекта контракта
    contract = web3.eth.contract(address=contract_address, abi=token_abi)

    # Адрес отправителя (владелец контракта)
    from_address = web3.eth.account.from_key(private_key).address

    # Подготовка транзакции
    txn = contract.functions.mint(to_address, int(amount)).buildTransaction({
        'from': from_address,
        'nonce': web3.eth.getTransactionCount(from_address),
        'gas': 200000,
        'gasPrice': web3.toWei('20', 'gwei')
    })

    # Подпись транзакции
    signed_txn = web3.eth.account.sign_transaction(txn, private_key)

    # Отправка транзакции
    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    print(f"Токены успешно чеканены. Хэш транзакции: {web3.toHex(tx_hash)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Чеканка токенов для указанного адреса")
    parser.add_argument("--rpc_url", required=True, help="URL до Geth RPC (например, http://127.0.0.1:8545)")
    parser.add_argument("--private_key", required=True, help="Приватный ключ владельца контракта")
    parser.add_argument("--contract_address", required=True, help="Адрес контракта токена")
    parser.add_argument("--to_address", required=True, help="Адрес кошелька для получения токенов")
    parser.add_argument("--amount", required=True, help="Количество токенов для чеканки")

    args = parser.parse_args()

    mint_tokens(
        rpc_url=args.rpc_url,
        private_key=args.private_key,
        contract_address=args.contract_address,
        to_address=args.to_address,
        amount=args.amount
    )
