from marshmallow import Schema, fields, post_load
from marshmallow_oneofschema import OneOfSchema

from funcoin.schema import Peer, Block, Transaction, Ping


class PeerMessage(Schema):
    pass


class BlockMessage(Schema):
    pass


class TransactionMessage(Schema):
    pass


class PingMessage(Schema):
    pass


class MessageDisambiguation(OneOfSchema):
    pass


class MetaSchema(Schema):
    pass


class BaseSchema(Schema):
    pass


def meta():
    pass


def create_peers_message(external_ip, external_port, peers):
    pass


def create_block_message(external_ip, external_port, block):
    pass


def create_transaction_message(external_ip, external_port, tx):
    pass


def create_ping_message(external_ip, external_port, block_height, peer_count, is_miner):
    pass
