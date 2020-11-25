from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
import json

from channels.layers import get_channel_layer


class OrderResult(AsyncWebsocketConsumer):
    async def connect(self):
        self.service_uid = self.scope['url_route']['kwargs']['service_uid']
        self.chat_group_name = f'chat_{self.service_uid}'
        # 收到连接时处理, 加入到群组
        print(self.chat_group_name, '***************')
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # 关闭channel时候处理, 将关闭的连接从群组中移除
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    # 收到消息
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print('收到消息--》', message)
        # 信息群发
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'client_message',
                'message': message
            }
        )

    # 处理客户端发来的消息
    async def client_message(self, event):
        message = event['message']
        print('发送消息。。。', message)
        # 发送消息到 WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

class ServiceConsumer(object):
    pass

class BeatServer(SyncConsumer):
    def test_print(self, message):
        self.room_group_name = 'chat_123'
        print(self.room_group_name)
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {
            'type': 'chat_message',
            'message': 'Update'
        })
        print(message)


# 同步方式，仅作示例，不使用
# class SyncConsumer(WebsocketConsumer):
#     def connect(self):
#         # 从打开到使用者的WebSocket连接的chat/routing.py中的URL路由中获取'room_name'参数。
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         print('WebSocket建立连接：', self.room_name)
#         # 直接从用户指定的房间名称构造通道组名称
#         self.room_group_name = 'msg_%s' % self.room_name
#
#         # 加入房间
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )  # async_to_sync(…)包装器是必需的，因为ChatConsumer是同步WebsocketConsumer，但它调用的是异步通道层方法。(所有通道层方法都是异步的。)
#
#         # 接受WebSocket连接。
#         self.accept()
#         simple_username = self.scope["session"]["session_simple_nick_name"]  # 获取session中的值
#
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': '@{} 已加入房间'.format(simple_username)
#             }
#         )
#
#     def disconnect(self, close_code):
#         print('WebSocket关闭连接')
#         # 离开房间
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )
#
#     # 从WebSocket中接收消息
#     def receive(self, text_data=None, bytes_data=None):
#         print('WebSocket接收消息：', text_data)
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#
#         # 发送消息到房间
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )
#
#     # 从房间中接收消息
#     def chat_message(self, event):
#         message = event['message']
#
#         # 发送消息到WebSocket
#         self.send(text_data=json.dumps({
#             'message': message
#         }))

def send_group_msg(service_uid, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'chat_{service_uid}',
        {
            'type': 'client_message',
            'message': message
        }
    )

if __name__ == '__main__':
    import os
    if not os.getenv('DJANGO_SETTINGS_MODULE'):
        os.environ['DJANGO_SETTINGS_MODULE'] = 'message.settings'
    send_group_msg('bbb', 'hello world')