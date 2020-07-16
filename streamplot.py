import datetime as dt
#import matplotlib
import matplotlib.pyplot as plt
import asyncio
import random
import time
import argparse
import sys

#matplotlib.use('Qt5Agg')

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('--send', action='store_true')
parser.add_argument('--host', dest='host', default='127.0.0.1')
parser.add_argument('-p', '--port', dest='port', default=8888)
parser.add_argument('-s', '--sep', default=',')
parser.add_argument('-N', '--num_values_plot', default=None)
parser.add_argument('-D', '--x_axis_dates', action='store_true')
parser.add_argument('-C', '--num_columns', dest='num_plots', default=1)
parser.add_argument('-Y', '--y_label', default='')

args = parser.parse_args()
print("send: " +str(args.send))
print("host: " +str(args.host))
print("port: " +str(args.port))
print("sep:  " +str(args.sep))



# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(args.num_plots, 1, 1)
plt.ion()
xs = []
ys = []

def animate(x, y):
    global xs
    global ys

    if type(x) == type('string'):
        if ':' in x:
            args.x_axis_dates = True

    # Add x and y to lists
    #xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    xs.append(x)
    ys.append(y)

    # Limit x and y lists to 20 items
    if args.num_values_plot:
        xs = xs[-args.num_values_plot:]
        ys = ys[-args.num_values_plot:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    #plt.xticks(rotation=45, ha='right')
    #plt.subplots_adjust(bottom=0.30)
    if args.x_axis_dates:
        plt.gcf().autofmt_xdate()
    #plt.title('TMP102 Temperature over Time')
    plt.ylabel(args.y_label)

    plt.draw()
    #fig.canvas.draw()
    #fig.canvas.draw_idle()
    plt.pause(0.001)


async def echo_server(reader, writer):
    while True:
        data = await reader.read(100)  # Max number of bytes to read
        if not data:
            print ("no new data")
            break
        msg = data.decode()
        msg = str(msg)
        print ("Received: " +msg)

        # Update graph data
        dl = msg.split(sep=args.sep)
        try:
            x = float(dl[0])
        except:
            x = dl[0]
        try:
            y = float(dl[1])
        except:
            y = dl[1]

        animate(x, y)
        
    writer.close()

async def init_server(host, port):
    print ("Opening server on " +str(port))
    server = await asyncio.start_server(echo_server, host, port)
    await server.serve_forever()


async def send_data(host, port):
    await asyncio.sleep(1)
    print ("Opening connection to " +str(host) +":" +str(port))
    send_reader, send_writer = await asyncio.open_connection(host, port)

    x = 0
    while True:
        x = x +1
        data = str(x) +", " +str(random.random()) +", " +str(random.random()) +", " +str(random.random())
        #print("Sending: " +data)
        send_writer.write(data.encode())
        await send_writer.drain()  # Flow control, see later
        await asyncio.sleep(2)

#animate(0,0)
plt.show()
loop = asyncio.get_event_loop()
loop.create_task(init_server(args.host, args.port))
if args.send:
    loop.create_task(send_data(args.host, args.port))
#loop.create_task(plt.show())

loop.run_forever()
loop.close()

# TODO: look at StreamEngine: https://pypi.org/project/stream-engine/

