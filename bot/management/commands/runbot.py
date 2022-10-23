from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from todolist import settings
from goals.models import Goal


class Command(BaseCommand):
    help = "run bot"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.BOT_TOKEN)

    def handle(self, *args, **kwargs):
        offset = 0
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message)

    def handle_unverified_user(self, msg: Message, tg_user: TgUser):
        tg_user.set_verification_code()
        tg_user.save(update_fields=["verification_code"])
        self.tg_client.send_message(
            msg.chat.id, f" Ваш код - {tg_user.verification_code}"
        )

    def fetch_tasks(self, msg: Message, tg_user: TgUser):
        goals = Goal.objects.filter(user=tg_user.user)
        if goals.count() > 0:
            resp_msg = [f"#{item.id} {item.title}" for item in goals]
            self.tg_client.send_message(msg.chat.id, "\n".join(resp_msg))
        else:
            self.tg_client.send_message(msg.chat.id, "Ваш список целей пуст!")

    def handle_user_with_verification(self, msg: Message, tg_user: TgUser):
        if not msg.text:
            return
        if "/goals" in msg.text:
            self.fetch_tasks(msg, tg_user)
        else:
            self.tg_client.send_message(msg.chat.id, "Неизвестная команда!")

    def handle_message(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(
            tg_id=msg.from_.id,
            defaults={"username": msg.from_.username}
        )
        if created:
            self.tg_client.send_message(msg.chat.id, "Вы зарегистрированы!")

        if tg_user.user:
            self.handle_user_with_verification(msg, tg_user)
        else:
            self.handle_unverified_user(msg, tg_user)
