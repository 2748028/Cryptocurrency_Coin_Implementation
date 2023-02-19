#!/usr/bin/python3

import json
import time
import hashlib
import os
import binascii
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficultytarget = 4
        # Mine the genesis block
        genesisblock = self.createblock("Genesis")
        self.chain.append(genesisblock)

    def getlast(self):
        return self.chain[-1]

    def hashheader(self, block):
        # Put it into json'd version of itself
        # Convert it to bytes
        jsond = json.dumps(block['header']).encode('utf-8')
        # Hash & return it
        return hashlib.sha256(jsond).hexdigest()

    def createblock(self, data = None):

        if len(self.chain) == 0:
            isgenesis = True
        else:
            isgenesis = False

        block = {
            'header' : {
                'num' : len(self.chain),
                'time' : int(time.time()),
                'nonce' : None,
                'prevhash' : (None if isgenesis else self.getlast()['hash'])
            },
            'data' : data,
            'hash' : None
        }

        # Set nonce to none.
        # Hash header of this block and insert it.
        block['hash'] = self.hashheader(block)

        return block

    def mineblock(self, block):
        while True:
            # GET A NONCE, put nonce in the header
            block['header']['nonce'] = binascii.b2a_hex(os.urandom(8)).decode("utf-8")
            # Hash header w/ nonce
            maybehash = self.hashheader(block)
            # Check if hash starts with 0000
            if maybehash[0:4] == '0000':
                # If yes, add hash to block['hash'], add to chain and return block to user
                block['hash'] = maybehash
                self.chain.append(block)
                return block

    def checkchain(self):

        reversechain = self.chain[::-1]
        # For block in list.
        for blocknum in range(len(reversechain)):
            # Print("Block No. {0}/{1}".format(blocknum + 1, len(reversechain)))
            # If (block is genesis (ie, nonce is None))
            if reversechain[blocknum]['header']['nonce'] == None:
                # Print("GENESIS BLOCK")
                return True
            # If (check block's stored hash to the newly compiled hash of the block's header)
            elif reversechain[blocknum]['hash'] == self.hashheader(reversechain[blocknum]):
                # Print("Passed self-check. {0} == {1}".format(reversechain[blocknum]['hash'], self.hashheader(reversechain[blocknum])))
                # If (check nextblock's stored has with blocks's header's prevhash)
                if reversechain[blocknum + 1]['hash'] == reversechain[blocknum]['header']['prevhash']:
                    # Print("Passed next-check. {0} == {1}".format(reversechain[blocknum + 1]['hash'], reversechain[blocknum]['header']['prevhash']))
                    pass
                else:
                    # Print("Failed next-check. {0} != {1}".format(reversechain[blocknum + 1]['hash'], reversechain[blocknum]['header']['prevhash']))
                    return False
            else:
                # Print("Failed self-check. {0} != {1}".format(reversechain[blocknum]['hash'], self.hashheader(reversechain[blocknum])))
                return False

@app.route('/')
def home():
    return 'Hello!'

@app.route('/mineblock/', methods = ['GET'])
def mineblock():

    blockdata = request.args.get('data', default = '', type = str)
    block = blockchain.createblock(blockdata)
    blockchain.mineblock(block)
    return render_template('mineblocks.html', block=block), 200

@app.route('/checkchain/', methods = ['GET'])
def checkchain():
    return str(blockchain.checkchain()), 200

@app.route('/getblocks/', methods = ['GET'])
def getblocks():
    # Returns all blocks
    return render_template('getblocks.html', blockchain=blockchain), 200

@app.route('/getblock/', methods = ['GET'])
def getblock():
    # Returns single block

    # Get number from args, if its not there, default to last block
    numdata = request.args.get('num', default = len(blockchain.chain) -1, type = int)
    # If user input is invalid, default to last block as well
    if numdata > len(blockchain.chain) -1 or numdata < 0:
        numdata = len(blockchain.chain) -1
    return render_template('getblock.html', block=blockchain.chain[numdata]), 200

blockchain = Blockchain()

app.run(host = 'localhost', port = '8080')
