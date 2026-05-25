namespace cpp match_service
// 结构体:User 
// 属性：id(int),name(string),score(int)
struct User {
    1: i32 id,
    2: string name,
    3: i32 score
}
// thrift远程服务接口定义：增 删
service MatchService {
    // 增：添加用户
    i32 addUser(1: User user, 2: string info);
    // 删：删除用户
    i32 deleteUser(1: User user, 2: string info);
}
