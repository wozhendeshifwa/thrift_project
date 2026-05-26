from sys import stdin

from gen_py.match import MatchService
from gen_py.match.ttypes import User 

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

    # Call the server
    if op == 'add':
        client.addUser(User(id=id,name=name,score=score),"")
    elif op == 'remove':
        client.deleteUser(User(id=id,name=name,score=score),"")
       
    # Close!
    transport.close()


def main():
    # stdin 循环读入一行op id name score
    # 判读输入合法性
    for line in stdin:
        line = line.strip()
        if not line:
            continue
        op, id, name, score = line.split()
        try:
            id = int(id)
            score = int(score)
        except ValueError:
            print("输入格式错误")
            continue
        operate(op,id,name,score)
        
if __name__ == '__main__':
    main()
     