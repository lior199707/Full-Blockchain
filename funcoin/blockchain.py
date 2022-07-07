import asyncio
import json
import math
import random
from hashlib import sha256
from time import time
import structlog

import funcoin.blockchain

logger = structlog.getLogger("blockchain")


class Blockchain(object):
    """
    class Blockchain handles a blockchain.
    """
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.target = "0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
        # create the genesis block
        logger.info("creating genesis block")
        self.chain.append(self.new_block())

    def new_block(self):
        """
        creates a new block.

        :return: the block.
        """
        # Generates a new block
        block = self.create_block(
            index=len(self.chain),
            transactions=self.pending_transactions,
            previous_hash=self.last_block['hash'] if self.last_block else None,
            nonce=format(random.getrandbits(64), "x"),
            target=self.target,
            timestamp=time(),
        )
        # Reset the list of pending transactions
        self.pending_transactions = []
        return block

    @staticmethod
    def create_block(index: int, transactions: list, previous_hash: str, nonce: str, target: str,
                     timestamp: float = None):
        """
        creates a new block.

        :param index: the index of the block
        :param transactions: the transactions stored in the block
        :param previous_hash: the hash of the previous block in the chain
        :param nonce: random 64 bits str in hexadecimal
        :param target: hexadecimal 64 bits number, the hash of every block created
        should be less than the target in order to be added to the blockchain.
        :param timestamp: float value of the time.
        :return: dictionary representing a block.
        """
        block = {'index': index,
                 'transactions': transactions,
                 'previous_hash': previous_hash,
                 'nonce': nonce,
                 'target': target,
                 'timestamp': timestamp or time(),
                 }
        # Get the hash of the new block, and add it to the block
        block['hash'] = funcoin.blockchain.Blockchain.hash(block)
        return block

    @staticmethod
    def hash(block: dict):
        """
        gets a block and returns its hash calculates by sha256.

        :param block: the block to generate it hash.
        :return:
        """
        # Hashes a block
        # We ensure the dictionary is sorted, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return sha256(block_string).hexdigest()

    @staticmethod
    def valid_block(block):
        return block["hash"].startswith("0000")

    @property
    def last_block(self):
        """
        Returns the last block in the chain (if there are blocks)

        :return: the last block if exists, otherwise None.
        """
        return self.chain[-1] if self.chain else None

    def new_transaction(self, sender, recipient, amount):
        # Adds a new transaction to the list of pending transactions
        self.pending_transactions.append({"recipient": recipient, "sender": sender, "amount": amount})

    def proof_of_work(self):
        # mining algorithm that generates new blocks adn add hem to the chain
        # generate blocks until a valid one is found(starts with 4 zeroes)
        while True:
            new_block = self.new_block()
            if self.valid_block(new_block):
                break
        # add the valid block to the chain
        self.chain.append(new_block)
        print("Found a new block: ", new_block)


    def valid_hash(self):
        pass