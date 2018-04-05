from django.contrib import admin

from .models import Challenge, ChallengeTopic, TopicSourceTable, ChallengeResultTable

admin.site.register(Challenge)
admin.site.register(ChallengeTopic)
admin.site.register(TopicSourceTable)
admin.site.register(ChallengeResultTable)
