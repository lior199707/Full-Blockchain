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
    """
    Ping message schema.
    """
    payload = fields.Nested(Ping())

    @post_load
    def add_name(self, data, **kwargs):
        # indicating it's a peer message for identification.
        data["name"] = "ping"
        return data


class MessageDisambiguation(OneOfSchema):
    type_field = "name"
    type_schemas = {
        "ping": PingMessage,
        "peers": PeerMessage,
        "block": BlockMessage,
        "transaction": TransactionMessage,
    }

    def get_obj_type(self, obj):
        if isinstance(obj, dict):
            return obj.get("name")


class MetaSchema(Schema):
    """
    Schema of a meta
    """
    address = fields.Nested(Peer())
    client = fields.Str()


class BaseSchema(Schema):
    """
    Base Schema of a general message.
    """
    meta = fields.Nested(MetaSchema())
    message = fields.Nested(MessageDisambiguation())


def meta(ip, port, version="funcoin-0.1"):
    """

    :param ip: the public IP of the peer
    :param port: the port the peer is listening on
    :param version: the version
    :return: dictionary containing 2 keys, "client", "address"
    address is also a dictionary of 2 keys: "ip", "port".
    """
    return {
        "client": version,
        "address": {"ip": ip, "port": port},
    }


def create_peers_message(external_ip, external_port, peers):
    """
    Generates a message containing peer(s).

    :param external_ip: the public IP of the peer
    :param external_port: the port the peer is listening on
    :param peers: list containing Peer(s).
    :return: JSON encoded string of the transaction message.
    """
    return BaseSchema().dumps(
        {
            "meta": meta(external_ip, external_port),
            "message": {"name": "peers", "payload": peers},
        }
    )


def create_block_message(external_ip, external_port, block):
    """
    Generates a message containing a block.

    :param external_ip: the public IP of the peer
    :param external_port: the port the peer is listening on
    :param block: block payload,a dictionary.
    :return: JSON encoded string of the transaction message.
    """
    return BaseSchema().dumps(
        {
            "meta": meta(external_ip, external_port),
            "message": {"name": "block", "payload": block},
        }
    )


def create_transaction_message(external_ip, external_port, tx):
    pass


def create_ping_message(external_ip, external_port, block_height, peer_count, is_miner):
    pass
