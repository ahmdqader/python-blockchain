from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import Crypto.Random
import binascii


class Wallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None

        print('bingo')

    def create_keys(self):
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key

        print('Created new wallet:')
        print('Private key: ' + self.private_key)
        print('Public key: ' + self.public_key)



    def save_keys(self):
        try:
            with open("wallet.txt", mode="w") as f:
                f.write(self.public_key)
                f.write('\n')
                f.write(self.private_key)
        except(IOError, IndexError):
            print('Failed saving the wallet')


    def load_keys(self):
        try:
            with open('wallet.txt', mode="r") as f:
                keys = f.readlines()
                public_key = keys[0][:-1]
                private_key = keys[1]

                self.public_key = public_key
                self.private_key = private_key
        except(IOError, IndexError):
            print('Faild loading the wallet')


    def generate_keys(self):
        random_gen = Crypto.Random.new().read
        private_key = RSA.generate(1024, random_gen)
        public_key = private_key.publickey()

        return (
            binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'),
            binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')
        )



    def sign_transaction(self, sender, recipient, amount):
        signer = PKCS1_v1_5.new(RSA.importKey(binascii.hexlify(self.private_key)))
        h = SHA256.new((str(sender) + str(recipient) + str(amount)).enocde('utf8'))
        signature = signer.sign(h)
        return binascii.hexlify(signature).decode('ascii')