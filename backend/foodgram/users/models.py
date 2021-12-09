from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


class Follow(models.Model):
    """
    Модель подписки.
    """
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="follower",
                             verbose_name='подписчик')
    following = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  related_name="following",
                                  verbose_name='автор')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'], name='unique_follow'
            )
        ]

    def clean(self):
        if self.following == self.user:
            raise ValidationError('Нельзя подписаться на себя')
