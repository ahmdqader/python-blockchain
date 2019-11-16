import hashlib
from utitity.hash_util import hash_block


class Verification:

    @staticmethod
    def valid_proof(transactions, last_hash, proof):
        transactions_to_dict = [transaction.to_ordered_dict() for transaction in transactions]
        guess = (str(transactions_to_dict) + str(last_hash) + str(proof)).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        print(guess_hash)
        return guess_hash[0:3] == '000'


    @classmethod
    def verify_chain(cls, blockchain):
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index - 1]):
                return False
            if not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print('proof of work is invalid')
                return False
        return True

    @staticmethod
    def verify_transaction(transaction, get_balance):
        print('transaction sender ' + transaction.sender)
        sender_balance = get_balance(transaction.sender)
        print('sender balance')
        print(sender_balance)

        print('transaction amount ' + str(transaction.amount))
        print('verify ' + str(sender_balance >= transaction.amount))
        return sender_balance >= transaction.amount

    @classmethod
    def verify_transactions(cls, opened_transactions, get_balance):
        return all([cls.verify_transaction(tx, get_balance) for tx in opened_transactions])
