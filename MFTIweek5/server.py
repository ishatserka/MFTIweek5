import asyncio

warehouse = dict()

def run_server(host, port):
    pass

def get_data(key):
    result = None
    if "*" in key:
        for key in warehouse:
            for data in warehouse[key]:
                result = f"{key} {data[0]} {data[1]}\n"
    else:
        for data in warehouse[key]:
            result = f"{key} {data[0]} {data[1]}\n"
            
    return result

def put(data):
    key, value, timestamp = data[4:].split(" ")
    if key in warehouse:
        warehouse[key].append((value, timestamp))
    else:
        warehouse[key] = [(value, timestamp)] 
    return "ok\n\n"

def get(key):
    key = key[4:]
    result = "ok\n"
    result = f"{result}{get_data(key)}\n"
        

"""
put test_key 13.0 1503319739
ok

get test_key 
ok
test_key 13.0 1503319739
test_key 12.0 1503319740
 
"""

async def handle_echo(reader, writer):
    data = await reader.read(1024)
    message = data.decode("utf-8")
    result = None
    if "get" in message:
        result = get(message)
    elif "put" in message:
        result = put(message)
    else:
        result = "error\nwrong command\n\n"
    writer.write(result.encode("utf-8"))
    writer.close()
    
loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, "127.0.0.1", 10001, loop=loop)
server = loop.run_until_complete(coro)
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
