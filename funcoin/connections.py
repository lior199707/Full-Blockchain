import structlog
from more_itertools import take

logger = structlog.getLogger(__name__)


class ConnectionPool:
    """
    Class ConnectionPool handles all the users connected to the server
    has a dictionary with:
    keys - user addresses (ip:port)
    value - the user, asyncio StreamWriter object
    """
    def __init__(self):
        self.connection_pool = dict()

    def broadcast(self, message):
        """
        sends a message to all the user connected to the server
        :param message:  the message to send
        """
        for user in self.connection_pool:
            user.write(f"{message}".encode())

    @staticmethod
    def get_address_string(writer):
        """
        returns the address of the user as ip:port

        :param writer: asyncio StreamWriter object, the user.
        :return: String representation of the address
        """
        ip = writer.address["ip"]
        port = writer.port["port"]
        return f"{ip}:{port}"

    def add_peer(self, writer):
        """adds a user to the dictionary of the connected users"""
        address = self.get_address_string(writer)
        self.connection_pool[address] = writer
        logger.info("Added new peer to pool", address=address)

    def remove_peer(self, writer):
        """Removes a user from the dictionary of the connected users"""
        address = self.get_address_string(writer)
        self.connection_pool.pop(address)
        logger.info("Removed peer from pool", address=address)

    def get_alive_peers(self, count):
        """

        :param count: the number of wanted users.
        :return: list containing the first 'count' users in the pool
        """
        # TODO (Reader): Sort these by most active,
        #  but let's just get the first *count* of them for now
        return take(count, self.connection_pool.items())
