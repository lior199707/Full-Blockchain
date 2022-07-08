import json
import funcoin.blockchain
from time import time
from marshmallow import Schema, fields, validates_schema, ValidationError


class Transaction(Schema):
    """
    schema for a Transaction
    """
    timestamp = fields.Int()
    sender = fields.Str()
    receiver = fields.Str()
    amount = fields.Int()
    signature = fields.Str()

    class Meta:
        ordered = True


class Block(Schema):
    """
    schema for a Block
    """
    mined_by = fields.Str(required=False)
    transactions = fields.Nested(Transaction(), many=True)
    height = fields.Int(required=True)
    difficulty = fields.Int(required=True)
    hash = fields.Str(required=True)
    previous_hash = fields.Str(required=True)
    nonce = fields.Str(required=True)
    timestamp = fields.Int(required=True)

    # TODO: implement a validation method to ensure that any block contained in a message is always valid

    class Meta:
        ordered = True

    # a special decorator indicating that Marshmallow should run ths function as part of its validation process.
    @validates_schema
    def validate_hash(self, data, **kwargs):
        """
        validates a transaction at the point of deserialization to ensure that any transaction is always valid.
        if the transaction is not valid raising Marshmallow.ValidationError(Exception).
        """
        block = data.copy()
        # Remove the hash key and its matching value
        block.pop("hash")

        # "dumps" serializes to a string(json)
        # if it's not the same string
        if data["hash"] != json.dumps(block, sort_keys=True):
            raise ValidationError("Fraudulent block: hash is wrong")


class Peer(Schema):
    """
    schema for a Peer
    """
    ip = fields.Str(required=True)
    port = fields.Int(required=True)
    last_seen = fields.Int(missing=lambda: int(time()))


class Ping(Schema):
    """
    Schema for a Ping
    """
    block_height = fields.Int()
    peer_count = fields.Int()
    is_miner = fields.Bool()
