import asyncio
import logging

from asyncua import Server, ua
from asyncua.common.methods import uamethod


@uamethod
def func(parent, value):
    print(f'func {value}')
    return value * 2


async def main():
    _logger = logging.getLogger(__name__)
    # setup our server
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

    # set up our own namespace, not really necessary but should as spec
    uri = "http://examples.freeopcua.github.io"
    idx = await server.register_namespace(uri)

    # populating our address space
    # server.nodes, contains links to very common nodes like objects and root
    myobj = await server.nodes.objects.add_object(idx, "MyObject")
    myvar = await myobj.add_variable(idx, "MyVariable", 6)
    myvar2 = await myobj.add_variable(idx, "MyVariable2", 6)
    # Set MyVariable to be writable by clients
    await myvar.set_writable()
    await myvar2.set_writable()
    # await server.nodes.objects.add_method(
    #     ua.NodeId("ServerMethod", idx),
    #     ua.QualifiedName("ServerMethod", idx),
    #     func,
    #     [ua.VariantType.Int64],
    #     [ua.VariantType.Int64],
    # )
    _logger.info("Starting server!")
    async with server:
        while True:
            await asyncio.sleep(1)
            val = await myvar.get_value()
            val2 = await myvar2.get_value()
            print("server val:",val)
            print("server val2:",val2)
            # _logger.info("Set value of %s to %.1f", myvar, new_val)
            # print("Set value of %s to %.1f", myvar, new_val)
            # await myvar.write_value(new_val)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    asyncio.run(main(), debug=False)