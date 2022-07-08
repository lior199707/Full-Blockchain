from marshmallow import Schema, fields, post_load
from marshmallow_oneofschema import OneOfSchema

from funcoin.schema import Peer, Block, Transaction, Ping


class PeerMessage(Schema):
    """
    Peer message schema.
    """
    payload = fields.Nested(Peer(many=True))

    @post_load
    def add_name(self, data, **kwargs):
        # indicating it's a peer message for identification.
        data["name"] = "peers"
        return data


class BlockMessage(Schema):
    """
    Block message schema.
    """
    payload = fields.Nested(Block())

    @post_load
    def add_name(self, data, **kwargs):
        # indicating it's a peer message for identification.
        data["name"] = "block"
        return data


class TransactionMessage(Schema):
    """
    Transaction message schema.
    """
    payload = fields.Nested(Transaction())

    @post_load
    def add_name(self, data, **kwargs):
        # indicating it's a peer message for identification.
        data["name"] = "transaction"
        return data


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
