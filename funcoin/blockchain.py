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
            height=len(self.chain),
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
    def create_block(height: int, transactions: list, previous_hash: str, nonce: str, target: str,
                     timestamp: float = None):
        """
        creates a new block.

        :param height: the index of the block
        :param transactions: the transactions stored in the block
        :param previous_hash: the hash of the previous block in the chain
        :param nonce: random 64 bits str in hexadecimal
        :param target: hexadecimal 64 bits number, the hash of every block created
        should be less than the target in order to be added to the blockchain.
        :param timestamp: float value of the time.
        :return: dictionary representing a block.
        """
        block = {'height': height,
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

    @property
    def last_block(self):
        """
        Returns the last block in the chain (if there are blocks)

        :return: the last block if exists, otherwise None.
        """
        return self.chain[-1] if self.chain else None

    def valid_block(self, block:dict):
        """
        checks if a block is valid

        :param block: the block to check if valid.
        :return: True id the block is valid, false otherwise.
        """
        # Check if a block's hash is less that the target
        return block["hash"] < self.target

    def add_block(self, block:dict):
        """
        gets a clock and add it to the chain

        :param block: dictionary, the block to add
        """
        # TODO: Add proper validation logic here!
        self.chain.append(block)

    def recalculate_target(self, block_index):
        """

        :return: the number we need to get below to mine a new block
        """
        # Check if we need to recalculate the target
        if block_index % 10 == 0:
            # Expected time span of 10 blocks
            expected_timespan = 10 * 10

            # Calculate the actual time span
            actual_timespan = self.chain[-1]["timestamp"] - self.chain[-10]["timestamp"]

            # Figure out what the offset is
            ratio = actual_timespan / expected_timespan

            # Now let's adjust the ratio to not be too extreme( between 0.25 to 4)
            ratio = max(0.25, ratio)
            ratio = min(4.00, ratio)

            # Calculate the new target by multiplying the current one by the ratio
            new_target = int(self.target, 16) * ratio
            self.target = format(math.floor(new_target), "x").zfill(64)
            logger.info(f"Calculated new mining target: {self.target}")
            return self.target

    async def get_blocks_after_timestamp(self, timestamp:float):
        """

        :param timestamp: float value representing the timestamp
        :return: a list of all the blocks whose timestamps are bigger than the timestamp received.
        """
        for index, block in enumerate(self.chain):
            if timestamp < block["timestamp"]:
                return self.chain[index:]

    async def mine_new_block(self):
        """
        proof of work algorithm, try to mine a block until a valid one is found
        than adds it to the chain.
        """
        self.recalculate_target(self.last_block["height"] + 1)
        while True:
            new_block = self.new_block()
            if self.valid_block(new_block):
                break
            await asyncio.sleep(0)
        self.chain.append(new_block)
        logger.info("Found a new block:", new_block)

    def new_transaction(self, sender, recipient, amount):
        # Adds a new transaction to the list of pending transactions
        self.pending_transactions.append({"recipient": recipient, "sender": sender, "amount": amount})

