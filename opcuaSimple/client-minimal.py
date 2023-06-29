import asyncio

from asyncua import Client
from time import sleep

url = "opc.tcp://0.0.0.0:4840/freeopcua/server/"
namespace = "http://examples.freeopcua.github.io"

print("client here")
async def main():
    
    print(f"Connecting to {url} ...")
    async with Client(url=url) as client:
        await client.set_security_string("Basic256Sha256,SignAndEncrypt,../certificates/my_cert.der,../certificates/my_private_key.pem")
        # Find the namespace index
        nsidx = await client.get_namespace_index(namespace)
        print(f"Namespace Index for '{namespace}': {nsidx}")

        # Get the variable node for read / write
        var = await client.nodes.root.get_child(
            ["0:Objects", f"{nsidx}:OpcuaTests", f"{nsidx}:AiInt64_1"]
        )
        var2 = await client.nodes.root.get_child(
            ["0:Objects", f"{nsidx}:OpcuaTests", f"{nsidx}:AiInt64_2"]
        )

        var3 = await client.nodes.root.get_child(
            ["0:Objects", f"{nsidx}:OpcuaTests", f"{nsidx}:Bi2"]
        )
        value = await var.read_value()
        print(f"Value of AiInt64_1 ({var}): {value}")

        value2 = await var2.read_value()
        print(f"Value of AiInt64_2 ({var2}): {value2}")
        new_value = value- 50
        print(f"Setting value of AiInt64_1 to {new_value} ...")
        await var.write_value(new_value)
        # res = await client.nodes.objects.call_method(f"{nsidx}:ServerMethod", 5)

        while(1):
            value = await var.read_value()
            value2 = await var2.read_value()
            print(f"Value of AiInt64_1 ({var}): {value}")
            print(f"Value of AiInt64_2 ({var2}): {value2}")
            new_value = value +1
            new_value2 = value2 +1
            print(f"Setting value of AiInt64_1 to {new_value} ...")
            await var.write_value(new_value)
            print(f"Setting value of AiInt64_1 to {new_value2} ...")
            await var2.write_value(new_value2)
            value3 = await var3.read_value()
            await var3.write_value(not value3)
            # # Calling a method
            # res = await client.nodes.objects.call_method(f"{nsidx}:ServerMethod", 5)
            # print(f"Calling ServerMethod returned {res}")
            await asyncio.sleep(1)
            


if __name__ == "__main__":
    asyncio.run(main())