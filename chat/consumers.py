import json

from channels.generic.websocket import AsyncWebsocketConsumer


class StatusConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close()
            return

        await self.channel_layer.group_add(
            "online_users",
            self.channel_name,
        )

        await self.accept()

        await self.channel_layer.group_send(
            "online_users",
            {
                "type": "user_status",
                "username": self.user.username,
                "status": "online",
            },
        )

    async def disconnect(self, close_code):
        if hasattr(self, "user") and self.user.is_authenticated:

            await self.channel_layer.group_send(
                "online_users",
                {
                    "type": "user_status",
                    "username": self.user.username,
                    "status": "offline",
                },
            )

            await self.channel_layer.group_discard(
                "online_users",
                self.channel_name,
            )

    async def user_status(self, event):
        await self.send(
            text_data=json.dumps({
                "username": event["username"],
                "status": event["status"],
            })
        )