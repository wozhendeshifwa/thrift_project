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
    #  字段匹配 输入合法性验证
    for line in stdin:
        line = line.strip()
        if not line:
            continue
        
        parts = line.split()
        if len(parts) != 4:
            print("输入格式错误，需要4个字段: op id name score")
            continue
        
        op, id_str, name, score_str = parts
        
        # 验证操作类型
        if op not in ['add', 'remove']:
            print(f"操作类型错误: {op}，只能是 add 或 remove")
            continue
        # 验证id为整数
        try:
            id = int(id_str)
        except ValueError:
            print(f"id必须是整数: {id_str}")
            continue
        # 验证score为整数
        try:
            score = int(score_str)
        except ValueError:
            print(f"score必须是整数: {score_str}")
            continue
        # 调用操作
        operate(op, id, name, score)
        
if __name__ == '__main__':
    main()
     