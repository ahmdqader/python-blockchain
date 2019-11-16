from utitity.verification import Verification
from blockchain import Blockchain
from uuid import uuid4
from wallet import Wallet

class Node:
    def __init__(self):
        self.wallet = Wallet()
        self.blockchain = None
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)

    def get_user_choice(self):
        user_choice = input('Your choice: ')
        return user_choice

    def get_transaction_value(self):
        recipient = input('Enter recipient name: ')
        amount = float(input('Enter transaction\'s value: '))

        return recipient, amount

    def listen_for_input(self):
        while True:
            print('Please choose')
            print('1: Add new transaction')
            print('2: Mine block')
            print('3: Output the blockchain blocks ')
            print('4: Output the particepants blocks ')
            print('5: create wallet')
            print('6: load wallet')
            print('7: save wallet')
            print('8: get balance')
            print('v: verify the blockchain')
            print('q: Quite the APP')

            user_choice = self.get_user_choice()
            if user_choice == '1':
                recipient, amount = self.get_transaction_value()
                signtaure = self.wallet.sign_transaction(self.wallet.public_key, recipient, signtaure, amount)
                self.blockchain.add_transaction(recipient, self.wallet.public_key, signtaure, amount)
            elif user_choice == '2':
                self.blockchain.mine_block()
            elif user_choice == '3':
                print(self.blockchain.chain)
            elif user_choice == '4':
                print(self.blockchain.participants)
            
            elif user_choice == '5':
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)

            elif user_choice == '6':
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)

            elif user_choice == '7':
                self.wallet.save_keys()

            elif user_choice == '8':
                balance = self.blockchain.get_balance(self.wallet.public_key)
                print(str(balance) + ' ELIXIR')

            elif user_choice == 'v':
                if not Verification.verify_chain(self.blockchain.chain):
                    print(self.blockchain.chain)
                    print('invalid blockchain')
                    break
                else:
                    print('valid blockchain')

            elif user_choice == 'q':
                break
            else:
                print('Enter a valid option, please!')


if __name__ == "__main__":
    node = Node()
    node.listen_for_input()