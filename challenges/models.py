from django.db import models


class Challenge(models.Model):
    challenge_id = models.IntegerField(primary_key=True)
    challenge_name = models.CharField(max_length=200)
    challenge_desc = models.TextField()
    challenge_text = models.TextField()
    challenge_available = models.BooleanField(default=True)

    def __str__(self):
        return self.challenge_name
