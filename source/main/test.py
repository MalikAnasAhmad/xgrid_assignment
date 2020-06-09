# print('16'.isdigit())
# print('16.9'.isdigit())
import json
import time
import socket
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
# print("Your Computer Name is:" + hostname)
# print("Your Computer IP Address is:" + IPAddr)

# print(client_id.rsplit(':',1))

from source.logic.server_storage import *

r = connect_redis()
r.flushall()
# print(r)
r.set("msg:hello", "Hello Redis!!!")
msg = r.get("msg:hello")
# print(msg)

print(r.keys())

players = "Players"
score       = 56
playerName  = "Player1"
r.zadd(players, {playerName:score})

score = int(time.time()*1000000)
client_id = "1.1.1.1:2356"
message = "hello"
r.zadd("chat_log_plain", {"@"+client_id+":"+message:score})
# time.sleep(1)sudo systemctl status redis
score = int(time.time()*1000000)
print(score)
r.zadd("chat_log_plain", {"@"+client_id+":"+message+'b':score})
# time.sleep(1)
score = int(time.time()*1000000)
print(score)
r.zadd("chat_log_plain", {"@"+client_id+":"+message+'a':score})

# print(int(time.time()*1000000))
# print(r.lrange("chat_log_plain",{-100,-1}))


print(r.zrange('chat_log_plain',0,-1))
print("zscore = > ",r.zscore("chat_log_plain", "@"+client_id+":"+message))

# logger.info(f"my_list: {r.lrange('my_list', 0, -1)}")


Epoch = int(time.time()*1000000)
client_id = "1.1.1.1:2356"
message = "hello"
print('Epoch => ', Epoch)
# data = {"Epoch":Epoch, "client_id" : client_id, "message" :  message}
data_1 = {'Epoch':Epoch, 'client_id' : client_id, 'message' :  message}
# data = {"client_id" : client_id, "message" :  message}
r.hmset("chat_log_plain_2", data_1)

Epoch = int(time.time()*1000000)
print('Epoch => ', Epoch)
data = {'Epoch':Epoch, 'client_id' : client_id, 'message' :  message}
r.hmset("chat_log_plain_2", data)
# r.hmset("chat_log_plain_1", {'a':'b','c':'d'})
# r.zadd("chat_log_plain", {"@"+client_id+":"+message+'a':score})

print(r.hgetall("chat_log_plain_2"))
# print(r.sort("chat_log_plain_2",'Epoch'))
print(r.get('chat_log_plain_2:client_id'))


chat_id_1 = "1.1.1.1:1254"
message_1 = "hello"
chat_id_1_for_storage = chat_id_1+"_"+str(time.time())
data = {chat_id_1_for_storage:  message_1}
r.lpush("chat_ids", chat_id_1_for_storage)
r.hmset("message_storage", data)

chat_id_2 = "1.1.1.1:1255"
message_2 = "hi"
chat_id_2_for_storage = chat_id_2+"_"+str(time.time())
data = {chat_id_2_for_storage:  message}
r.lpush("chat_ids", chat_id_2_for_storage)
r.hmset("message_storage",data)


print("list of chat-ids : ",r.lrange("chat_ids",0,-1))
print("messages : ",r.hmget("message_storage",r.lrange("chat_ids",0,-1)))
print(r.hgetall("message_storage"))
print(r.hkeys("message_storage"))
print(r.hget("message_storage",'1.1.1.1:12541591683025.487051'))
print(r.hmget("message_storage",r.lrange("chat_ids",0,-1)))
# print(r.keys())
# print(r.mget(r.keys()))
# print(r.hscan("message_storage",r.lrange("chat_ids",0,-1)))
list1 = r.lrange("chat_ids",0,-1)
list3 = [i.split('_', 1)[1] for i in list1]
print("time_stamps => ", list3)
list1 = [i.split('_', 1)[0] for i in list1]
list2 = r.hmget("message_storage",r.lrange("chat_ids",0,-1))
dictA = dict(zip(list1, list2))

print(dictA)

print([ { 'user_id': x, 'time': y, 'message': z } for x, y, z in zip(list1, list3,list2) ])
print(json.dumps([ { 'user_id': x, 'time': y, 'message': z } for x, y, z in zip(list1, list3,list2) ]))
print(type(json.dumps([ { 'user_id': x, 'time': y, 'message': z } for x, y, z in zip(list1, list3,list2) ])))

