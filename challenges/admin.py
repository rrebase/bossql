from django.contrib import admin

from .models import Challenge, ChallengeAttempt, ChallengeResultTable, TopicSourceTable, ChallengeTopic


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ("name", "topic")

@admin.register(ChallengeAttempt)
class ChallengeAttemptAdmin(admin.ModelAdmin):
    list_display = ("attempted_at", "user", "is_successful", "challenge", "get_topic")

    def get_topic(self, obj):
        return obj.challenge.topic
    get_topic.short_description = "Topic"
    get_topic.admin_order_field = "challenge__topic"

admin.site.register(ChallengeTopic)

@admin.register(TopicSourceTable)
class TopicSourceTableAdmin(admin.ModelAdmin):
    list_display = ("name", "topic")

admin.site.register(ChallengeResultTable)
