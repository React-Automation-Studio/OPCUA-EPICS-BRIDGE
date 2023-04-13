import asyncio

from asyncua import Client
from time import sleep
url = "opc.tcp://0.0.0.0:4840/freeopcua/server/"
namespace = "http://examples.freeopcua.github.io"

print("client here")
async def main():
    
    print(f"Connecting to {url} ...")
    async with Client(url=url) as client:
        # Find the namespace index
        nsidx = await client.get_namespace_index(namespace)
        print(f"Namespace Index for '{namespace}': {nsidx}")

        # Get the variable node for read / write
        var = await client.nodes.root.get_child(
            ["0:Objects", f"{nsidx}:MyObject", f"{nsidx}:MyVariable"]
        )
        var2 = await client.nodes.root.get_child(
            ["0:Objects", f"{nsidx}:MyObject", f"{nsidx}:MyVariable2"]
        )
        value = await var.read_value()
        print(f"Value of MyVariable ({var}): {value}")

        value2 = await var2.read_value()
        print(f"Value of MyVariable2 ({var2}): {value2}")
        new_value = value- 50
        print(f"Setting value of MyVariable to {new_value} ...")
        await var.write_value(new_value)
        # res = await client.nodes.objects.call_method(f"{nsidx}:ServerMethod", 5)

        while(1):
            value = await var.read_value()
            value2 = await var2.read_value()
            print(f"Value of MyVariable ({var}): {value}")
            print(f"Value of MyVariable2 ({var2}): {value2}")
            new_value = value +1
            new_value2 = value2 +1
            print(f"Setting value of MyVariable to {new_value} ...")
            await var.write_value(new_value)
            print(f"Setting value of MyVariable to {new_value2} ...")
            await var2.write_value(new_value2)
            # # Calling a method
            # res = await client.nodes.objects.call_method(f"{nsidx}:ServerMethod", 5)
            # print(f"Calling ServerMethod returned {res}")
            await asyncio.sleep(1)
            


if __name__ == "__main__":
    asyncio.run(main())