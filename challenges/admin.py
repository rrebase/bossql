from django.contrib import admin

from .models import Challenge, ChallengeTopic, ChallengeSourceTable, ChallengeResultTable

admin.site.register(Challenge)
admin.site.register(ChallengeTopic)
admin.site.register(ChallengeSourceTable)
admin.site.register(ChallengeResultTable)
