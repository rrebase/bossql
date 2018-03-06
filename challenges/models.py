import json
import psycopg2

from django.db import models

from .utils import get_env_db_conn


class ChallengeTopic(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class Challenge(models.Model):
    topic = models.ForeignKey(ChallengeTopic,
                              on_delete=models.PROTECT,
                              related_name="challenges")
    name = models.CharField(max_length=200)
    description = models.TextField()
    additional_info = models.TextField(blank=True)
    available = models.BooleanField(default=True)

    def attempt(self, sql):
        try:
            with get_env_db_conn() as conn:
                with conn.cursor() as cur:
                    for source_table in self.source_tables.all():
                        source_table.create_table(cur)
                    cur.execute(sql)
                    result_column_names = [col.name for col in cur.description]
                    result_content_rows = [list(row) for row in cur.fetchall()]
                conn.rollback()
        except psycopg2.ProgrammingError:
            return (False, None, None)
        return (result_column_names == json.loads(self.result_table.column_names_json)
                and result_content_rows == json.loads(self.result_table.content_rows_json),
                result_column_names, result_content_rows)

    def __str__(self):
        return self.name


class ChallengeSourceTable(models.Model):
    challenge = models.ForeignKey(Challenge,
                                  on_delete=models.CASCADE,
                                  related_name="source_tables")
    name = models.CharField(max_length=200)
    creation_sql = models.TextField()
    column_names_json = models.TextField(default="", editable=False)
    content_rows_json = models.TextField(default="", editable=False)

    def create_table(self, cur):
        cur.execute(self.creation_sql)

    def drop_table(self, cur):
        cur.execute("DROP TABLE {};".format(self.name))

    def get_column_names(self):
        return json.loads(self.column_names_json)

    def get_content_rows(self):
        return json.loads(self.content_rows_json)

    def _store_representation(self, cur):
        self.create_table(cur)
        cur.execute("SELECT * FROM {};".format(self.name))
        column_names = [column.name for column in cur.description]
        self.column_names_json = json.dumps(column_names)
        self.content_rows_json = json.dumps(cur.fetchall())

    def save(self, *args, **kwargs):
        old_creation_sql = None
        if self.pk:
            old_instance = ChallengeSourceTable.objects.get(pk=self.pk)
            old_creation_sql = old_instance.creation_sql
        if self.creation_sql != old_creation_sql:
            with get_env_db_conn() as conn:
                with conn.cursor() as cur:
                    self._store_representation(cur)
                conn.rollback()
        super().save(*args, **kwargs)

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
