from gen_cpp.match import MatchService
from gen_cpp.match.ttypes import User

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

def operate(op,id,name,score):
    # Make socket
    transport = TSocket.TSocket('localhost', 9090)

    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = MatchService.Client(protocol)

    # Connect!
    transport.open()

    user = User(id=id, name=name, score=score)

    if op == "add":
        client.addUser(user, "")
    elif op == "remove":
        client.removeUser(user, "")
    else:
        print("操作类型错误，支持的操作: add, remove")

    # Close!
    transport.close()

def main():
    while True:
        try:
            # 读取一行输入并分割
            line = input().strip()
            if not line:
                continue
            
            parts = line.split()
            if len(parts) != 4:
                print("输入格式错误，需要4个字段: op id name score")
                continue
            
            op = parts[0]
            id = int(parts[1])
            name = parts[2]
            score = int(parts[3])
            
            # 调用操作函数
            operate(op, id, name, score)
            
        except ValueError:
            print("输入格式错误: id和score必须是整数")
        except EOFError:
            break
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()