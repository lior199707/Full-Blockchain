import asyncio
from textwrap import dedent

# communication protocol of the server:
# When a user connects, they should be prompted for their nickname.
# When a user connects, their arrival should be broadcast to every connected user (except themselves).
# If a user sends any message, their message is broadcast to every connected user (except themselves).
# If a user sends the message /list, they should see a list of all connected users.
# If a user sends the message /quit, they should be disconnected,
# and a message saying “<nickname> has quit” should be broadcast to all connected users.

class ConnectionPool:
    """
    class ConnectionPoll, manages the pool of connected clients, supports the protocol mentioned above
    """

    def __init__(self):
        self.connection_pool = set()

    def send_welcome_message(self, writer: asyncio.StreamWriter):
        """
        Sends a welcome message to a newly connected client
        :param writer: asyncio StreamWriter object, responsible for writing to an underlying connection
        :return:
        """
        message = dedent(f"""
        \r=== 
        \rWelcome {writer.nickname}!
        \r
        \rThere are {len(self.connection_pool) - 1} user(s) here beside you
        \r            
        \rHelp: 
         \r- Type anything to chat
         \r- /list will list all the connected users
         \r- /quit will disconnect you
        \r===
        """)
        writer.write(f"{message}\n\r".encode())

    def broadcast(self, writer: asyncio.StreamWriter, message: str):
        """
        Broadcasts a general message to the entire pool
        :param writer: asyncio StreamWriter object, responsible for writing to an underlying connection,
        represents the sender of the message.
        :param message: the message to send
        """
        for user in self.connection_pool:
            # don't send the message back to the sender
            if user != writer:
                user.write(f"{message}\n\r".encode())

    def broadcast_user_join(self, writer: asyncio.StreamWriter):
        """
        Calls the broadcast method with a "user joining" message
        :param writer: asyncio StreamWriter object, responsible for writing to an underlying connection
        represents the new user that has joined the server
        :return:
        """
        self.broadcast(writer, f"{writer.nickname} just joined")

    def broadcast_user_quit(self, writer: asyncio.StreamWriter):
        """
        Calls the broadcast method with a "user quitting" message
        :param writer: asyncio StreamWriter object, responsible for writing to an underlying connection
        represents the user that quit the server
        :return:
        """
        self.broadcast(writer, f"{writer.nickname} just quit")

    def broadcast_new_message(self, writer: asyncio.StreamWriter, message: str):
        """
        Calls the broadcast method with a user's chat message
        :param writer: asyncio StreamWriter object, responsible for writing to an underlying connection
        represents the sender of the message
        :param message:
        """
        self.broadcast(writer, f"[{writer.nickname}]: {message}")

    def list_users(self, writer: asyncio.StreamWriter):
        """
        Lists all the users in the pool
        :param writer: asyncio StreamWriter object, responsible for writing to an underlying connection
        :return:
        """
        message = "===\n\r"
        message += "Currently connected users:"
        for user in self.connection_pool:
            message += f"\n\r - {user.nickname}"
            if user == writer:
                message += " (you)"
        message += "\n\r==="
        writer.write(f"{message}\n\r".encode())

    def add_new_user_to_pool(self, writer: asyncio.StreamWriter):
        """
        Adds a new user to our existing pool
        :param writer: asyncio StreamWriter object, responsible for writing to an underlying connection
        :return:
        """
        self.connection_pool.add(writer)

    def remove_user_from_pool(self, writer: asyncio.StreamWriter):
        """
        Removes an existing user from our pool
        :param writer: asyncio StreamWriter object, responsible for writing to an underlying connection
        :return:
        """
        self.connection_pool.remove(writer)