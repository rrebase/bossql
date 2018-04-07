from django.contrib import admin

from .models import Challenge, ChallengeTopic, TopicSourceTable, ChallengeResultTable


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ("name", "topic")

admin.site.register(ChallengeTopic)

@admin.register(TopicSourceTable)
class TopicSourceTableAdmin(admin.ModelAdmin):
    list_display = ("name", "topic")

admin.site.register(ChallengeResultTable)
