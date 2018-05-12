from django.contrib import admin
from django.template.loader import render_to_string

from .models import Challenge, ChallengeAttempt, ChallengeResultTable, TopicSourceTable, ChallengeTopic


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ("name", "topic")
    readonly_fields = ("source_tables",)
    fields = ("topic", "name", "description", "hints", "points", "source_tables", "solution_sql", "evaluation_sql")

    class Media:
        js = ("challenges/js/admin_challenge.js",)

    @staticmethod
    def source_tables(instance):
        source_tables = instance.topic.source_tables.all()
        return render_to_string("challenges/_admin_topic_source_tables.html",
                                {"tables": source_tables})


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
