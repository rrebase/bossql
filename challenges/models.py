import json
import psycopg2

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from accounts.models import CustomUser
from .utils import get_env_db_conn


class ChallengeTopic(models.Model):
    name = models.CharField(max_length=200)
    summary = models.TextField()
    description = models.TextField()
    available = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class Challenge(models.Model):
    topic = models.ForeignKey(ChallengeTopic,
                              on_delete=models.PROTECT,
                              related_name="challenges")
    name = models.CharField(max_length=200)
    description = models.TextField()
    hints = models.TextField(blank=True)
    solution_sql = models.TextField()
    evaluation_sql = models.TextField(blank=True)
    available = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def get_query_result(self, sql, fail_silently=False):
        result_column_names = None
        result_content_rows = None
        try:
            with get_env_db_conn() as conn:
                with conn.cursor() as cur:
                    for source_table in self.topic.source_tables.order_by("creation_order"):
                        source_table.create_table(cur)
                    cur.execute(sql)
                    if self.evaluation_sql:
                        cur.execute(self.evaluation_sql)
                    result_column_names = [col.name for col in cur.description]
                    result_content_rows = [list(row) for row in cur.fetchall()]
                    conn.rollback()
        except psycopg2.ProgrammingError:
            if not fail_silently:
                raise
        return {"column_names": result_column_names, "content_rows": result_content_rows}

    def attempt(self, sql, user):
        result = self.get_query_result(sql, fail_silently=True)
        is_successful = (result["column_names"] == json.loads(self.result_table.column_names_json)
                         and result["content_rows"] == json.loads(self.result_table.content_rows_json))

        if not user.is_authenticated:
            return is_successful, result["column_names"], result["content_rows"]

        attempt = self.attempts.filter(user=user).first()
        if not attempt:
            attempt = ChallengeAttempt(
                challenge=self,
                user=user
            )
        if sql and sql != attempt.tried_sql and (is_successful or not attempt.is_successful):
            # Proceed, if a non-empty SQL was provided that is not equal to the last one tried.
            # Do not overwrite existing successful attempt, unless the new attempt is successful.
            attempt.tried_sql = sql
            attempt.attempted_at = timezone.now()
            if not attempt.is_successful and is_successful:
                user.completed_challenges += 1
                user.save()
            elif not is_successful:
                attempt.fail_count += 1
            attempt.is_successful = is_successful
            attempt.save()

        return is_successful, result["column_names"], result["content_rows"]

    def recreate_result_table(self, fail_silently=False):
        result = self.get_query_result(self.solution_sql, fail_silently)
        if result["column_names"] and result["content_rows"]:
            if not hasattr(self, 'result_table'):
                self.result_table = ChallengeResultTable.objects.create(
                    challenge=self,
                    column_names_json=json.dumps(result["column_names"]),
                    content_rows_json=json.dumps(result["content_rows"])
                )
            else:
                self.result_table.column_names_json = json.dumps(result["column_names"])
                self.result_table.content_rows_json = json.dumps(result["content_rows"])
                self.result_table.save()

    def clean(self):
        super().clean()
        try:
            self.recreate_result_table(fail_silently=False)
        except (psycopg2.Error, psycopg2.Warning) as e:
            raise ValidationError({
                "solution_sql": str(e)
            })

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.recreate_result_table(fail_silently=False)

    def __str__(self):
        return self.name


class ChallengeAttempt(models.Model):
    challenge = models.ForeignKey(Challenge,
                                  on_delete=models.CASCADE,
                                  related_name="attempts")
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             related_name="challenge_attempts")
    tried_sql = models.TextField()
    is_successful = models.BooleanField(default=False)
    fail_count = models.IntegerField(default=0)
    attempted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Attempt for challenge '{challenge}' by user '{user}'".format(
            challenge=self.challenge,
            user=self.user
        )


class TopicSourceTable(models.Model):
    topic = models.ForeignKey(ChallengeTopic,
                              on_delete=models.CASCADE,
                              related_name="source_tables")
    name = models.CharField(max_length=200)
    creation_sql = models.TextField()
    column_names_json = models.TextField(default="", editable=False)
    content_rows_json = models.TextField(default="", editable=False)
    creation_order = models.IntegerField(default=0)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def drop_table(self, cur):
        cur.execute("DROP TABLE IF EXISTS {};".format(self.name))

    def create_table(self, cur):
        self.drop_table(cur)
        cur.execute(self.creation_sql)

    def get_column_names(self):
        return json.loads(self.column_names_json)

    def get_content_rows(self):
        return json.loads(self.content_rows_json)

    def _store_representation(self):
        old_creation_sql = None
        if self.pk:
            old_instance = TopicSourceTable.objects.get(pk=self.pk)
            old_creation_sql = old_instance.creation_sql
        if self.creation_sql != old_creation_sql:
            with get_env_db_conn() as conn:
                with conn.cursor() as cur:
                    self.create_table(cur)
                    cur.execute("SELECT * FROM {};".format(self.name))
                    column_names = [column.name for column in cur.description]
                    self.column_names_json = json.dumps(column_names)
                    self.content_rows_json = json.dumps(cur.fetchall())
                    conn.rollback()
            for challenge in self.topic.challenges.all():
                challenge.recreate_result_table()

    def clean(self):
        try:
            self._store_representation()
        except (psycopg2.Error, psycopg2.Warning) as e:
            raise ValidationError({
                "creation_sql": str(e)
            })

    def __str__(self):
        return self.name


class ChallengeResultTable(models.Model):
    challenge = models.OneToOneField(Challenge,
                                     on_delete=models.CASCADE,
                                     related_name="result_table")
    column_names_json = models.TextField(default="")
    content_rows_json = models.TextField(default="")

    def get_column_names(self):
        return json.loads(self.column_names_json)

    def get_content_rows(self):
        return json.loads(self.content_rows_json)

    def __str__(self):
        return "ChallengeResultTable for challenge {}".format(self.challenge)
