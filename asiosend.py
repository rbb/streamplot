import asyncio
import random
import argparse
#import time

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('-f', '--file', dest ='fname', default=None)
parser.add_argument('--host', default='127.0.0.1')
parser.add_argument('-p', '--port', dest='port', default=8888)
parser.add_argument('-i', '--interval', default=1)

args = parser.parse_args()
print("file: " +str(args.fname))
print("host: " +str(args.host))
print("port: " +str(args.port))


async def send_data(host, port):
    print ("Opening connection to " +str(host) +":" +str(port))
    reader, writer = await asyncio.open_connection(host, port)

    x = 0
    while True:
        x = x +1
        data = str(x) +", " +str(random.random())
        print(data)
        writer.write(data.encode())
        await writer.drain()  # Flow control, see later
        await asyncio.sleep(args.interval)

    writer.close()


async def send_file(fname, host, port):
    print ("opening " +fname)
    try:
        fp = open(fname)
        # do stuff with fp


        print ("Opening connection to " +str(host) +":" +str(port))
        reader, writer = await asyncio.open_connection(host, port)

        line = fp.readline().strip()
        while line:
            print("Line: " +line)

            writer.write(line.encode())
            await writer.drain()  # Flow control, see later
            await asyncio.sleep(args.interval)
            line = fp.readline()

        writer.close()
    finally:
        fp.close()



if args.fname:
    asyncio.run(send_file(args.fname, args.host, args.port))
else:
    asyncio.run(send_data(args.host, args.port))

