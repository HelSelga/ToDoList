from django.db import models
import random

CODE_VOCABULARY = "1234567890abcdefgihjklmnopqrstuvwxyz"


class TgUser(models.Model):
    tg_user_id = models.BigIntegerField(verbose_name="telegram user id", unique=True)

    tg_chat_id = models.BigIntegerField(
        verbose_name="telegram chat id",
        null=True,
        blank=True,
        default=None
    )

    username = models.CharField(
        max_length=512,
        verbose_name="telegram username",
        null=True,
        blank=True,
        default=None
    )

    user = models.ForeignKey(
        "core.User",
        models.PROTECT,
        null=True,
        blank=True,
        default=None,
        verbose_name="app user"
    )
    verification_code = models.CharField(max_length=32, verbose_name="access code")

    def set_verification_code(self):
        code = "".join([random.choice(CODE_VOCABULARY) for _ in range(12)])
        self.verification_code = code
        
    class Meta:
        verbose_name = "telegram-пользователь"
        verbose_name_plural = "telegram-пользователи"
