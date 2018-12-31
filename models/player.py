from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Player(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    nick = models.CharField(max_length=100, default='')
    score = models.IntegerField(default=0)

    def get_player(self, user_id):
        return self.objects.get(user_id=user_id)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
    instance.player.save()

#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
    #instance.profile.save()
    #instance.Player.save()