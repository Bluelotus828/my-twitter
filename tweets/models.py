from django.db import models
from django.contrib.auth.models import User
from utils.time_helpers import utc_now


class Tweet(models.Model):
    # foreign key, thus SET_NULL as default
    # styling tip: one parameter a line, last with ','
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        help_text= 'who posted this content',
    )
    content = models.CharField(max_length=255)
    # parameter automatically give timestamp once created
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = (('user', 'created_at'),)
        ordering = ('user', '-created_at')

    @property
    def hours_to_now(self):
        # created_at has time zone information, datetime.now does not
        # contain time zone information. Thus the two does not
        # calculate directly
        return (utc_now() - self.created_at).seconds // 3600

    def __str__(self):
        # when executed, this funtion prints the instance Tweet
        return f'{self.created_at} {self.user}: {self.content}'