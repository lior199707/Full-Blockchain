

"""import asyncio
from textwrap import dedent


async def handle_connection(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    # get a nickname for the new Client
    writer.write("> Choose your nickname: ".encode())
    response = await reader.readuntil(b"\n")

    # set the Clients nickname
    writer.nickname = response.decode().strip()

    # add the Client to the pool and send a welcome message
    connection_pool.add_new_user_to_pool(writer)
    connection_pool.send_welcome_message(writer)

    # Announce the arrival of this new user
    connection_pool.broadcast_user_join(writer)

    # keep the user connected to the server until he quits
    while True:
        try:
            data = await reader.readuntil(b"\n")
        except asyncio.exceptions.IncompleteReadError:
            connection_pool.broadcast_user_quit(writer)
            break
        message = data.decode().strip()
        if message == "/quit":
            connection_pool.broadcast_user_quit(writer)
            break
        elif message == "/list":
            connection_pool.list_users(writer)
        else:
            connection_pool.broadcast_new_message(writer, message)

        await writer.drain()
        if writer.is_closing():
            break

    # Close the connection and clean up
    writer.close()
    await writer.wait_closed()
    connection_pool.remove_user_from_pool(writer)


async def main():
    server = await asyncio.start_server(handle_connection, "0.0.0.0", 8888)
    async with server:
        await server.serve_forever()


connection_pool = ConnectionPool()
asyncio.run(main())
# telnet 127.0.0.1 8888"""