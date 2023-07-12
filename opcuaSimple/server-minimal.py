import asyncio
import logging
import os
from asyncua import Server, ua
from asyncua.common.methods import uamethod
from asyncua.crypto.permission_rules import SimpleRoleRuleset
from asyncua.server.user_managers import CertificateUserManager
import datetime
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
    # uri = "http://examples.freeopcua.github.io"
    # idx = await server.register_namespace(uri)
    idx=4
    # populating our address space
    # server.nodes, contains links to very common nodes like objects and root
    OpcuaTests = await server.nodes.objects.add_object(idx, "OpcuaTests")

    variableName="tick"
    tick = await OpcuaTests.add_variable(f"ns={idx};s=GVL.{variableName}", f"{variableName}", 0,varianttype=ua.VariantType.Int64)
    await tick.set_writable()

    variableName="AoInt64"
    AoInt64= await OpcuaTests.add_variable(f"ns={idx};s=GVL.{variableName}", f"{variableName}", 0,varianttype=ua.VariantType.Int64)
    await AoInt64.set_writable()
  
      
    variableName="AiInt64"
    AiInt64 = await OpcuaTests.add_variable(f"ns={idx};s=GVL.{variableName}", f"{variableName}", 0,varianttype=ua.VariantType.Int64)
    await AiInt64.set_writable()
    

    variableName="AoUInt64"
    AoUInt64= await OpcuaTests.add_variable(f"ns={idx};s=GVL.{variableName}", f"{variableName}", 0,varianttype=ua.VariantType.UInt64)
    await AoUInt64.set_writable()

    variableName="AiUInt64"
    AiUInt64= await OpcuaTests.add_variable(f"ns={idx};s=GVL.{variableName}", f"{variableName}", 0,varianttype=ua.VariantType.UInt64)
    await AiUInt64.set_writable()

    variableName="AiInt32"
    AiInt32 = await OpcuaTests.add_variable( f"ns={idx};s=GVL.{variableName}", f"{variableName}", 0,varianttype=ua.VariantType.Int32)
    await AiInt32.set_writable()

    variableName="AoInt32"
    AoInt32 = await OpcuaTests.add_variable(f"ns={idx};s=GVL.{variableName}", f"{variableName}", 0,varianttype=ua.VariantType.Int32)
    await AoInt32.set_writable()

    variableName="AiUInt32"
    AiUInt32 = await OpcuaTests.add_variable(f"ns={idx};s=GVL.{variableName}", f"{variableName}", 0,varianttype=ua.VariantType.UInt32)
    await AiUInt32.set_writable()

    variableName="AoUInt32"
    AoUInt32 = await OpcuaTests.add_variable(f"ns={idx};s=GVL.{variableName}", f"{variableName}", 0,varianttype=ua.VariantType.UInt32)
    await AoUInt32.set_writable()


    variableName="AiInt16"
    AiInt16 = await OpcuaTests.add_variable(f"ns={idx};s=GVL.{variableName}", f"{variableName}",0,varianttype=ua.VariantType.Int16)
    await AiInt16.set_writable()

    variableName="AoInt16"
    AoInt16 = await OpcuaTests.add_variable(f"ns={idx};s=GVL.{variableName}", f"{variableName}", 0,varianttype=ua.VariantType.Int16)
    await AoInt16.set_writable()

    variableName="AiUInt16"
    AiUInt16 = await OpcuaTests.add_variable(f"ns={idx};s=GVL.{variableName}", f"{variableName}", 0,varianttype=ua.VariantType.UInt16)
    await AiInt16.set_writable()

    variableName="AoUInt16"
    AoUInt16 = await OpcuaTests.add_variable(f"ns={idx};s=GVL.{variableName}", f"{variableName}", 0,varianttype=ua.VariantType.UInt16)
    await AoUInt16.set_writable()

    variableName="AiFloat"
    AiFloat = await OpcuaTests.add_variable(f"ns={idx};s=GVL.{variableName}", f"{variableName}", 0,varianttype=ua.VariantType.Float)
    await AiFloat.set_writable()

    variableName="AoFloat"
    AoFloat = await OpcuaTests.add_variable(f"ns={idx};s=GVL.{variableName}", f"{variableName}", 0,varianttype=ua.VariantType.Float)
    await AoFloat.set_writable()

    variableName="AoDouble"
    AoDouble = await OpcuaTests.add_variable(f"ns={idx};s=GVL.{variableName}", f"{variableName}", 0,varianttype=ua.VariantType.Double)
    await AoDouble.set_writable()

    variableName="AiDouble"
    AiDouble = await OpcuaTests.add_variable(f"ns={idx};s=GVL.{variableName}", f"{variableName}", 0,varianttype=ua.VariantType.Double)
    await AiDouble.set_writable()

    variableName="AiByte"
    AiByte = await OpcuaTests.add_variable(f"ns={idx};s=GVL.{variableName}", f"{variableName}", 0,varianttype=ua.VariantType.Byte)
    await AiByte.set_writable()

    variableName="AoByte"
    AoByte = await OpcuaTests.add_variable(f"ns={idx};s=GVL.{variableName}", f"{variableName}", 0,varianttype=ua.VariantType.Byte)
    await AoByte.set_writable()

    variableName="AiSByte"
    AiSByte = await OpcuaTests.add_variable(f"ns={idx};s=GVL.{variableName}", f"{variableName}",0,varianttype=ua.VariantType.SByte)
    await AiSByte.set_writable()

    variableName="AoSByte"
    AoSByte = await OpcuaTests.add_variable(f"ns={idx};s=GVL.{variableName}", f"{variableName}", 0,varianttype=ua.VariantType.SByte)
    await AoSByte.set_writable()

    variableName="BiBool"
    BiBool = await OpcuaTests.add_variable(f"ns={idx};s=GVL.{variableName}", f"{variableName}",False, varianttype=ua.VariantType.Boolean)
    await BiBool.set_writable()

    variableName="BoBool"
    BoBool = await OpcuaTests.add_variable(f"ns={idx};s=GVL.{variableName}", f"{variableName}", False,varianttype=ua.VariantType.Boolean)
    await BoBool.set_writable()
   
    variableName="test_date"
    test_date = await OpcuaTests.add_variable(f"ns={idx};s=GVL.{variableName}", f"{variableName}", datetime.datetime.now(),varianttype=ua.VariantType.DateTime)
    await test_date.set_writable()

    variableName="StringIn"
    StringIn = await OpcuaTests.add_variable(f"ns={idx};s=GVL.{variableName}", f"{variableName}", "Hello world",varianttype=ua.VariantType.String)
    await StringIn.set_writable()
    
    variableName="StringOut"
    StringOut = await OpcuaTests.add_variable(f"ns={idx};s=GVL.{variableName}" , f"{variableName}","Hello world, edit me",varianttype=ua.VariantType.String)
    await StringOut.set_writable()
    
    
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
            await asyncio.sleep(0.1)
            tick_val = await tick.get_value()
            if tick_val< 10000000:
                tick_val=tick_val+1
            else:
                tick_val=0
           
            await tick.write_value(tick_val)

            AiInt64_val = await AiInt64.get_value()
            if AiInt64_val< 10000000:
                AiInt64_val=AiInt64_val+10000
            else:
                AiInt64_val=-10000000
            await AiInt64.write_value(AiInt64_val)

            AiUInt64_val = await AiUInt64.get_value()
            if AiUInt64_val< 1000000:
                AiUInt64_val=AiUInt64_val+2000
            else:
                AiUInt64_val=0
            await AiUInt64.write_value(AiUInt64_val,ua.VariantType.UInt64)

            AiInt32_val = await AiInt32.get_value()
            if AiInt32_val< 1000000:
                AiInt32_val=AiInt32_val+30
            else:
                AiInt32_val=0
            await AiInt32.write_value(AiInt32_val,ua.VariantType.Int32)

            AiUInt32_val = await AiUInt32.get_value()
            if AiUInt32_val< 100000:
                AiUInt32_val=AiUInt32_val+40
            else:
                AiUInt32_val=0
            await AiUInt32.write_value(AiUInt32_val,ua.VariantType.UInt32)

            AiInt16_val = await AiInt16.get_value()
            if AiInt16_val< 10000:
                AiInt16_val=AiInt16_val+50
            else:
                AiInt16_val=-10000
            await AiInt16.write_value(AiInt16_val,ua.VariantType.Int16)

            AiUInt16_val = await AiUInt16.get_value()
            if AiUInt16_val< 10000:
                AiUInt16_val=AiUInt16_val+60
            else:
                AiUInt16_val=0
            await AiUInt16.write_value(AiUInt16_val,ua.VariantType.UInt16)

            AiFloat_val = await AiFloat.get_value()
            if AiFloat_val< 10000:
                AiFloat_val=AiFloat_val+0.001
            else:
                AiFloat_val=-10000
            await AiFloat.write_value(AiFloat_val,ua.VariantType.Float)

            AiDouble_val = await AiDouble.get_value()
            if AiDouble_val< 1000000:
                AiDouble_val=AiDouble_val+1.001
            else:
                AiDouble_val=-1000000
            await AiDouble.write_value(AiDouble_val,ua.VariantType.Double)

            AiByte_val = await AiByte.get_value()
            if AiByte_val< 255:
                AiByte_val=AiByte_val+1
            else:
                AiByte_val=0
            await AiByte.write_value(AiByte_val,ua.VariantType.Byte)

            AiSByte_val = await AiSByte.get_value()

            if AiSByte_val< 127:
                AiSByte_val=AiSByte_val+1
            else:
                AiSByte_val=-128
            await AiSByte.write_value(AiSByte_val,ua.VariantType.SByte)

            BiBool_val = await BiBool.get_value()

            await BiBool.write_value(not BiBool_val,ua.VariantType.Boolean)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    asyncio.run(main(), debug=False)