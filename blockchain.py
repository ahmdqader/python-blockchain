import json
from block import Block
from transaction import Transaction
from utitity.verification import Verification
from utitity.hash_util import hash_block

MINING_REWARD = 10

class Blockchain:
    def __init__(self, hosting_node_id):
        self.chain = []
        self.opened_transactions = []
        self.owner = "Ahmed"
        self.participants = {"Ahmed"}
        self.load_data()
        self.hosting_node = hosting_node_id

    def load_data(self):
        updated_blockchain = []

        try:
            with open('blockchain.txt', mode='r') as f:
                file_content = f.readlines()
                blockchain = json.loads(file_content[0][:-1])
                for block in blockchain:
                    converted_transactions = [Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in
                                              block['transactions']]
                    updated_block = Block(
                        block['index'],
                        block['previous_hash'],
                        converted_transactions,
                        block['proof'],
                        block['timestamp']
                    )

                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain
                opened_transactions = json.loads(file_content[1])
                updated_transactions = []
                for tx in opened_transactions:
                    converted_transaction = Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount'])
                    updated_transactions.append(converted_transaction)
                self.opened_transactions = updated_transactions

        except (IOError, IndexError):
            # will give it 0 timestamp
            # cause we don't we don't want it to constantly update with current time
            init_block = Block(0, "", [], 100, 0)
            self.chain = [init_block]

    def save_data(self):
        try:
            with open('blockchain.txt', mode='w') as f:
                savable_chain = [block.__dict__.copy() for block in [Block(block_el.index, block_el.previous_hash, [tx.to_ordered_dict() for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in self.chain]]
                f.write(json.dumps(savable_chain))
                f.write('\n')
                savable_tx = [tx.__dict__.copy() for tx in self.opened_transactions]
                f.write(json.dumps(savable_tx))
        except IOError:
            print("saving data failed")

    def proof_of_work(self):
        last_block = self.chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(self.opened_transactions, last_hash, proof):
            proof += 1
        return proof

    def get_balance_by_participant(self, type, participant):
        amount = 0
        if type == "recipient":
            transactions = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in self.chain]
        else:
            transactions = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in self.chain]
        for transaction in transactions:
            for mnt in transaction:
                amount += mnt
        return amount

    def get_balance(self, participant):
        sender_tx = self.get_balance_by_participant('sender', participant)
        recipient_tx = self.get_balance_by_participant('recipient', participant)
        return recipient_tx - sender_tx

    def get_last_blockchain_value(self):
        if len(self.chain) < 1:
            return None
        return self.chain[-1]

    def add_transaction(self, recipient, sender, signature, amount=1.0):
        transaction = Transaction(sender, recipient, signature, amount)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.opened_transactions.append(transaction)
            self.participants.add(sender)
            self.participants.add(recipient)
            self.save_data()
        else:
            return False

    def clear_transactions(self):
        self.opened_transactions = []

    def mine_block(self):
        last_block = self.chain[-1]
        proof = self.proof_of_work()
        reward_transaction = Transaction('MINING', self.hosting_node, '', MINING_REWARD)
        copied_transactions = self.opened_transactions[:]
        copied_transactions.append(reward_transaction)
        block = Block(len(self.chain), hash_block(last_block), copied_transactions, proof)
        self.chain.append(block)
        self.clear_transactions()
        self.save_data()

        print(self.chain)
