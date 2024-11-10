# from channels.generic.websocket import JsonWebsocketConsumer

# class MyJsonWebsocketConsumer(JsonWebsocketConsumer):
#     def connect(self):
#         print("websocket connected...")
#         self.accept()
    
#     def receive_json(self, content, **kwargs):
#         print("msg received from client", content)
#         print("Message:",content," , type:",type(content))
#         self.send_json({
#             'message': content['message']
#         })
        
#     def close(self, code=None, reason=None):
#         print("websocket closed...", code)
    
#     def disconnect(self, code):
#         print("websocket disconnected...", code)
    
from channels.consumer import SyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync

class MySyncConsumer(SyncConsumer):
    def websocket_connect(self,event):
        print("websocket connected..", event)
        print("channel layer...", self.channel_layer)
        print("channel name...", self.channel_name)
        async_to_sync(self.channel_layer.group_add)(
            'programmers',
            self.channel_name
        )
        self.send({'type': 'websocket.accept'})
    def websocket_disconnect(self,event):
        print("websocket disconnected...", event)
        print("channel layer...", self.channel_layer)
        print("channel name...", self.channel_name)
        async_to_sync(self.channel_layer.group_discard)(
            'programmers',
            self.channel_name
        )
        raise StopConsumer()
    def websocket_receive(self,event):
        print('message receive from client...', event['text'])
        print('type of message receive from client...', type(event['text']))
        async_to_sync(self.channel_layer.group_send)(
            'programmers',
            {
                'type': 'chat.message',
                'message': event['text']
            }
        )
    def chat_message(self,event):
        print("event..", event)
        print("Actual data..", event['message'])
        print("Type of Actual data..", type(event['message']))
        self.send({
            'type': 'websocket.send',
            'text': event['message']
        })