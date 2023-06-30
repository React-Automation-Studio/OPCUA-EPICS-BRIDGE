import asyncio
import logging
import os
from asyncua import Server, ua
from asyncua.common.methods import uamethod
from asyncua.crypto.permission_rules import SimpleRoleRuleset
from asyncua.server.user_managers import CertificateUserManager

@uamethod
def func(parent, value):
    print(f'func {value}')
    return value * 2


async def main():
    _logger = logging.getLogger(__name__)
    # setup our server
    secure = os.getenv("secure", False)=="True"
    if secure:
        cert_user_manager = CertificateUserManager()
        await cert_user_manager.add_admin("../certificates/client.der", name='admin')
        server = Server(user_manager=cert_user_manager)
    else:
        server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
    if secure:
        server.set_security_policy([ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt],
                                permission_ruleset=SimpleRoleRuleset())
        # load server certificate and private key. This enables endpoints
        # with signing and encryption.

        await server.load_certificate("../certificates/server.der")
        await server.load_private_key("../certificates/server_private_key.pem")
    # set up our own namespace, not really necessary but should as spec
    uri = "http://examples.freeopcua.github.io"
    idx = await server.register_namespace(uri)

    # populating our address space
    # server.nodes, contains links to very common nodes like objects and root
    OpcuaTests = await server.nodes.objects.add_object(idx, "OpcuaTests")
    AiInt64_1 = await OpcuaTests.add_variable(idx, "AiInt64_1", 0,varianttype=ua.VariantType.Int64)
    await AiInt64_1.set_writable()
    AiInt64_2 = await OpcuaTests.add_variable(idx, "AiInt64_2", 0,varianttype=ua.VariantType.Int64)
    await AiInt64_2.set_writable()
    AoInt64_1 = await OpcuaTests.add_variable(idx, "AoInt64_1", 0,varianttype=ua.VariantType.Int64)
    await AoInt64_1.set_writable()
    AoInt64_2 = await OpcuaTests.add_variable(idx, "AoInt64_2", 0,varianttype=ua.VariantType.Int64)
    await AoInt64_2.set_writable()
    AiInt32 = await OpcuaTests.add_variable(idx, "AiInt32", 0,varianttype=ua.VariantType.Int32)
    await AiInt32.set_writable()
    AoInt32 = await OpcuaTests.add_variable(idx, "AoInt32", 0,varianttype=ua.VariantType.Int32)
    await AoInt32.set_writable()
    AiInt16 = await OpcuaTests.add_variable(idx, "AiInt16", 0,varianttype=ua.VariantType.Int16)
    await AiInt16.set_writable()
    AoInt16 = await OpcuaTests.add_variable(idx, "AoInt16", 0,varianttype=ua.VariantType.Int16)
    await AoInt16.set_writable()
    AiByte = await OpcuaTests.add_variable(idx, "AiByte", 0,varianttype=ua.VariantType.Byte)
    await AiByte.set_writable()
    AoByte = await OpcuaTests.add_variable(idx, "AoByte", 0,varianttype=ua.VariantType.Byte)
    await AoByte.set_writable()
    Bi = await OpcuaTests.add_variable(idx, "Bi",False, varianttype=ua.VariantType.Boolean)
    await Bi.set_writable()
    Bo = await OpcuaTests.add_variable(idx, "Bo", False,varianttype=ua.VariantType.Boolean)
    await Bo.set_writable()
    Bi2 = await OpcuaTests.add_variable(idx, "Bi2",True, varianttype=ua.VariantType.Boolean)
    await Bi2.set_writable()
    # Set MyVariable to be writable by clients
    
    
    
    
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
            val = await AiInt64_1.get_value()
            val2 = await AiInt64_2.get_value()
            print("server AiInt64_1:",val)
            print("server AiInt64_2:",val2)
            val3 = await AoInt64_1.get_value()
            val4 = await AoInt64_2.get_value()
            print("server AoInt64_1:",val3)
            print("server AoInt64_2:",val4)
            val5 = await Bi.get_value()
            print("server Bi:",val5)
            val5 = await Bi.write_value(not val5)
            val6 = await Bi2.get_value()
            print("server Bi2:",val6)
            val7 = await Bo.get_value()
            print("server Bo:",val7)
            # _logger.info("Set value of %s to %.1f", AiInt64_1, new_val)
            # print("Set value of %s to %.1f", AiInt64_1, new_val)
            # await AiInt64_1.write_value(new_val)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    asyncio.run(main(), debug=False)