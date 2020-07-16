import asyncio

async def echo_server(reader, writer):
    while True:
        data = await reader.read(100)  # Max number of bytes to read
        if not data:
            break
        msg = data.decode()
        print ("Received: " +str(msg))
        #writer.write(data)
        #await writer.drain()  # Flow control, see later
    writer.close()

async def main(host, port):
    print ("Opening server on " +str(port))
    server = await asyncio.start_server(echo_server, host, port)
    await server.serve_forever()

port = 8888
asyncio.run(main('127.0.0.1', port))
