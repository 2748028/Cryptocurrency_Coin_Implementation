#!/usr/bin/python3
import json
import copy
import time
import random
import hashlib
import os
import binascii
from flask import Flask, request, Response
import uuid

# Example Queries:
# Creates 1 unique wallet.
# http://0.0.0.0:8080/create_wallet
# Shows all present wallets on the block-chain.
# http://0.0.0.0:8080/show_balances
# Allows us to specify a sender, receiver, and amount to be sent in a transaction.
# http://0.0.0.0:8080/create_transaction?from=a32ebc7a110d4503?to=11e61f70037d4230?amount=10

## TO BE FIXED ##
# Transactions fail to occur, why?

app = Flask(__name__)

class Blockchain:

    def __init__(self):
        self.chain = [] # Contains all of the objects (blocks) within the chain.
        self.wallets = [] # Contains all the objects (pub/priv/currency wallets) generated on the chain.
        self.mempool = [] # Contains all the objects (pending transactions and their info) pending for inclusion on the chain.
        self.difficulty_target = 4 # Sets number of consecutive leading 0's we wish to see in the winning hash.
        self.mine_block() # Instantiates the generation of the genesis block.

#NEW-----------------------------------------------------------------------------------------------------

    def create_wallet(self):
        public_key = uuid.uuid4().hex
        public_key = str(public_key[0:len(public_key)//2]) # Cuts the initially 32 character hex string into 16 Hex char str.
        private_key = uuid.uuid4().hex
        private_key = str(private_key[0:len(private_key)//2]) # Cuts the initially 32 character hex string into 16 Hex char str.
        balance = 10

        new_wallet = { 'public_key' : public_key,
            'private_key' : private_key,
            'balance' : balance
        } # Instantiates new wallet dictionary.

        self.wallets.append(new_wallet)

        print ('Your Public Key Is: ' + str(public_key))
        print ('Your Private Key Is: ' + str(private_key))
        print ('Your Initial Balance Is: ' + str(balance) + ' Coin(s)')
        print ('########################')

        return new_wallet
        # Define wallet with fields: public_key, private_key, balance *Check
        # Add new wallet to self.wallets *Needs verification.
        # Return the wallet to caller *Needs verification.
        pass

    def hash_transaction(self, transaction):

        transaction_pre_hash = transaction
        transaction_id = hashlib.sha256()  # Selects sha256 to be our means of hashing.
        transaction_id.update(transaction_pre_hash.encode('utf-8'))  # Ensures that the hashed transaction is placed within the var 'transaction_id' in UTF-8 format (important).
        return str(transaction_id.hexdigest())
        print ('Successfully created the following Transaction ID: ' + str(transaction_id))
        # Hash transaction *Needs verification.
        # Return hash *Needs verification.
        pass

    def add_transaction_to_mempool(self, transaction_id, transaction):

        print ('Made it to the transaction block!')
        transaction_success = None
        # This function works to first determine that the sending party (pub-key) matches.
        for wallet in blockchain.wallets:
            if wallet.has_key('public_key') and wallet('public_key') == transaction('from'): # If the pub-key field is present in the current wallet and that pub-key is equal to the public key of the sender in the transaction continue.
                sender_priv_key = wallet('private_key') # Saves the senders private address associated to the provided pub-key.
                sender_current_balance = wallet('balance')

                if sender_current_balance <= transaction('amount'): # Tests to see the sender has the balance required to send what they want to send.
                    print ('Sending the transaction of amount into the Mem-Pool: ' + str(transaction('amount')))
                    transaction_success = True

                    confirmed_transaction = {  # Transferring fields to the new transaction data structure for placement into the mem-pool.
                        'time': int(transaction('time')),  # Passes the original transaction time.
                        'from': str(transaction('from')),  # Saves the confirmed public-key address of our sender.
                        'to': str(transaction('to')),  # Saves the public-key address of our recipient.
                        'amount': request.args.get('amount', type=float), # Saves the amount the sender wishes the receiver have.
                        'is_success' : transaction_success
                    }

                    # Push the transactions into the mem-pool.
                    self.mempool.append(confirmed_transaction)

                return transaction_success

            elif wallet.has_key_('public_key') and wallet('public_key') != transaction('from'):
                print ('Nice try falsifying this transaction kiddo.')
                transaction_success = False
                return transaction_success

            else:
                print ('Looks like this was not the public-key we were looking for.')
                transaction_success = False
                continue

        # Validate transaction *Needs verification.
        # Add transaction to self.mempool *Needs verification.
        # Return OK or BAD *Needs verification.
        pass

    def choose_transactions_from_mempool(self):

        maximum_transactions = 0
        confirmed_transactions = []
        for transaction in self.mempool:
            if transaction or maximum_transactions != 10: # If there exists a transaction in the mem-pool and the presently appended amount of transactions are not greater than 10.
                if transaction.has_key('is_success') and transaction('is_success') == True: # If the transaction has the 'is_success' field and has been marked as genuine.
                    confirmed_transactions.append(transaction) # Push the transaction into a list to be appended to the next found block.

                    sender_public_key = transactions('from') # Used to find our sending party.
                    for wallet in self.wallets: # Checks for the wallet associated with the sending party in the chosen transaction.
                        if wallet('public_key') == sender_public_key:
                            to_be_subtracted = wallet('balance') # Subtracts the sent amount from their wallet balance.
                            to_be_subtracted = to_be_subtracted - transaction('amount')
                            wallet_balance['balance'] = to_be_subtracted
                            print ('Sent coins have been subtracted from the senders balance.')
                            break # Ends once the destined wallet has been found.
                        else:
                            continue

                    receiver_public_key = transactions('to')
                    for wallet in self.wallets: # Checks for the wallet associated with the receiving party in the chosen transaction.
                        if wallet('public_key') == receiver_public_key:
                            to_be_added = wallet('balance') # Adds the sent amount from the other users wallet balance.
                            to_be_added = to_be_added + transaction('amount')
                            wallet_balance['balance'] = to_be_added
                            print ('Sent coins have been added from the senders balance.')
                            break  # Ends once the destined wallet has been found.
                        else:
                            continue
                    del (transaction) # Removes the present transaction we just processed.
                    maximum_transactions = maximum_transactions + 1 # Ensures we only add 10 transactions at most to the block.
                    continue
            else:
                print ('It appears there are no pending transactions left in the Mem-Pool!')
                break

        return confirmed_transactions
        # Choose 10 random transactions *Needs to be verified.
        # Check if the balance allows spending the amount asked *Needs verification / Done in the transaction func.
        # Change the balance for the sender *Needs verification.
        # Change the balance for the recipient *Needs verification.
        # Remove transactions from mempool.
        # Return transaction to caller *Needs verification.
        pass


    def calculate_merkle_root(self, block):
        # Calculate the merkle root
        # Return the merkle root (hash)
        pass


    def check_merkle_root(self, block):
        # Check merkle root
        # Return OK or BAD
        pass


#Previously Created Functions----------------------------------------------------------------------------#

    def hash_block_header(self, block):
        hashId = hashlib.sha256() # Selects SHA256 to be our means of hashing.
        hashId.update(repr(block['header']).encode('utf-8')) # Ensures that the hashed block is placed within the object representation of key 'header' in UTF-8 format (important).
        return str(hashId.hexdigest())

    def get_last_block(self):
        return self.chain[-1] # Returns the last entire block object on the chain.

    def create_block(self):

        block = {
            'header' : {
                'block_number': len(self.chain),
                'block_time': int(time.time()), # Appends the exact creation time of the block.
                'block_nonce': None, # This should have a nonce.
                'previous_block_hash': (None if len(self.chain) == 0 else self.get_last_block()['hash']), # Grabs the last blocks hash so long as it is not the genesis block.
                'merkle_root': None # This should contain the Merkle root.
            },
            'transactions' : {}, # This should contain the selected transactions pulled from mem-pool.
            'hash' : None # This should contain a hash of the entire new block.
        }

        return block # Returns the completed block for insertion into the chain dict.


    def mine_block(self):

        block = self.create_block()

        block['transactions'] = self.choose_transactions_from_mempool() # Function used to to select which transactions to sppend to the newly found block.
        block['header']['merkle_root'] = self.calculate_merkle_root(block)

        while True:
            block['header']['block_nonce'] = str(binascii.b2a_hex(os.urandom(8))) # Used to seed a random value for the block nonce.
            block['hash'] = self.hash_block_header(block)

            if block['hash'][:self.difficulty_target] == '0' * self.difficulty_target: # Used to check for the number of leading zeroes we want.
                break

        self.chain.append(block)

        return block

    def check_chain(self):

        for block_number in reversed(range(len(self.chain))):

            current_block = self.chain[block_number]

            if not current_block['hash'] == self.hash_block_header(current_block):
                return False

            if block_number > 0 and not current_block['header']['previous_block_hash'] == self.chain[block_number - 1]['hash']:
                return False

            if not self.check_merkle_root(current_block):
                return False

        return True

#END OF OLD----------------------------------------------------------------------------------------------#


#Flask Func Definitions----------------------------------------------------------------------------------#

@app.route('/create_wallet', methods = ['GET'])
def create_wallet():
    return Response(json.dumps(blockchain.create_wallet()), status=200, mimetype='application/json')

@app.route('/show_balances', methods = ['GET'])
def show_balances():

    wallet_count = 0 # Used to identify the wallet owner, reset every func call.
    temp_wallets = [] # Holds the initial wallets that still contain their private address.
    temp_wallets = blockchain.wallets

    for wallet in temp_wallets:
        print ('Wallet Owner: ' + str(wallet_count))
        print ('Wallet Public Address: ' + str(wallet['public_key']))
        print ('Wallet Balance: ' + str(wallet['balance']))
        print ('#----------------#')
        wallet_count = wallet_count + 1

    sensitive_wallet_addresses = [] # Holds the now numbered wallets that still have a private address value.
    cleaned_wallet_addresses = [] # Used for holding the scrubbed wallets.
    sensitive_wallet_addresses = blockchain.wallets
    trashbin = [] # Used to hold popped private addresses, wiped every function call and end.

    for wallet in sensitive_wallet_addresses:
        if 'private_key' in wallet: # Matches if the wallet contains a priv-key field.
            trashbin = wallet.pop('private_key')
            cleaned_wallet_addresses.append(wallet)
            print ('Private key was successfully found for the wallet! Removing.')

        elif wallet and 'private_key' not in wallet: # Matches if there exists a wallet, but it has already had the priv-key field stripped.
            cleaned_wallet_addresses.append(wallet)
            print ('Wallet has already been cleaned, appending!')

        else: # Base case for when there exists no wallets to process.
            print ('Private address has already been removed.')
            break
    print (cleaned_wallet_addresses)

    return Response(json.dumps(cleaned_wallet_addresses), status=200, mimetype='application/json')
    # clean wallets of private_keys here *Check

@app.route('/create_transaction', methods = ['GET'])
def create_transaction():

    try:
        transaction = { # Creation of transaction dictionary data structure.
            'time': int(time.time()), # Saves the current request time of the transaction.
            'from': request.args.get('from', type = str), # Saves the public-key address of our sender.
            'to': request.args.get('to', type = str), # Saves the public-key address of our recipient.
            'amount': request.args.get('amount', type = float) # Saves the amount the sender wishes the receiver have.
        }

        # The following ensures that the sending party in-fact controls the wallet they are sending funds from.
        private_key = request.args.get('private_key', default = '', type = str) # Get private-key.

        print ('none modified' + str(blockchain.wallets))

        for wallet in blockchain.wallets:
            print ('oof')
            print (blockchain.wallets)
            if wallet['private_key'] == private_key and transaction['from'] == wallet['public_key']: # God I love redundancy.
                print ('Matching wallet found for transaction!')
                pass
                break

            elif wallet:
                print ('Non-matching wallet, continuing to next...')
                continue

            else:
                print ('oof')
                continue

            raise ('No matching wallet was found for this requested transaction!')
        #assert private_key == blockchain.wallets[transaction['public_key']]['private_key'] # Ensure priv-key matches sender pub-key.

    except:
        print ('Looks like something went wrong there.')
        return Response(json.dumps({'Error': 'Invalid transaction'}), status=400, mimetype='application/json')

    print ('Passed successfully.')
    # Ensures that the entirety of the transaction data-structure is hashed using SHA256.
    transaction_id = blockchain.hash_transaction(transaction)
    # Ensures that the hashed, and un-touched dict is pushed into the mem-pool.
    transaction_ok = blockchain.add_transaction_to_mempool(transaction_id, transaction)

    if transaction_ok: # If the 'transaction_ok' var exists proceed to return the hashed ID to the user.
        return Response(json.dumps({'Result': transaction_id}), status=200, mimetype='application/json')
        print ('Your transaction ID (Hash) Is: ' + str(transaction_id))
    else:
        return Response(json.dumps({'Error': 'Invalid transaction'}), status=400, mimetype='application/json')
        print ('Uh-oh, looks like something went wrong here.')

@app.route('/show_mempool', methods = ['GET'])
def show_mempool():
    return Response(json.dumps(blockchain.mempool), status=200, mimetype='application/json')

#--------------------------------------------------------------------------------------------------------      

@app.route('/mine_block', methods = ['GET'])
def mine_block():
    block = blockchain.mine_block()
    return Response(json.dumps(block), status=200, mimetype='application/json')

@app.route('/check_blockchain', methods = ['GET'])
def check_blockchain():
    if blockchain.check_chain:
        return Response(json.dumps({'Result': 'OK'}), status=200, mimetype='application/json')
    else:
        return Response(json.dumps({'Result': 'Invalid blockchain'}), status=200, mimetype='application/json')

@app.route('/show_blocks', methods = ['GET'])
def show_blocks():
    return Response(json.dumps(blockchain.chain), status=200, mimetype='application/json')

@app.route('/show_block', methods = ['GET'])
def show_block():
    try:
        block_number = request.args.get('number', default = 0, type = int)
        block = blockchain.chain[block_number]
    except:
        return Response(json.dumps({'Error': 'Invalid block number'}), status=400, mimetype='application/json')

    return Response(json.dumps(block), status=200, mimetype='application/json')

#--------------------------------------------------------------------------------------------------------

blockchain = Blockchain()
app.run(host = '0.0.0.0', port = 8080)
