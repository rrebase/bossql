from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models import Count
from django.template.loader import render_to_string

from challenges.models import Challenge, ChallengeAttempt, ChallengeResultTable, TopicSourceTable, ChallengeTopic

admin.site.site_header = 'bossql admin'
admin.site.unregister(Group)


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('name', 'topic', 'points', 'added_by')
    readonly_fields = ('source_tables',)
    fields = ('topic', 'name', 'description', 'hints', 'points', 'source_tables', 'solution_sql', 'evaluation_sql', 'order')

    class Media:
        js = ('challenges/js/admin_challenge.js',)

    @staticmethod
    def source_tables(instance):
        source_tables = instance.topic.source_tables.all()
        return render_to_string('challenges/_admin_topic_source_tables.html',
                                {'tables': source_tables})

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # only set added_by during the first save
            obj.added_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ChallengeAttempt)
class ChallengeAttemptAdmin(admin.ModelAdmin):
    list_display = ('attempted_at', 'user', 'is_successful', 'challenge', 'get_topic')
    list_filter = ('challenge', 'is_successful')

    def get_topic(self, obj):
        return obj.challenge.topic

    get_topic.short_description = 'Topic'
    get_topic.admin_order_field = 'challenge__topic'


@admin.register(ChallengeTopic)
class ChallengeTopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'available', 'challenges_count')
    list_filter = ('available',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(challenges_count=Count('challenges', distinct=True))

    def challenges_count(self, obj):
        return obj.challenges_count

    challenges_count.short_description = 'Challenges in topic'
    challenges_count.admin_order_field = 'challenges_count'


@admin.register(TopicSourceTable)
class TopicSourceTableAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_topics')

    def get_topics(self, obj):
        return ', '.join(map(str, obj.topics.all()))

    get_topics.short_description = 'Topics'


admin.site.register(ChallengeResultTable)
