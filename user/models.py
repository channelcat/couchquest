from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(primary_key=True)
    email = fields.CharField(max_length=255, unique=True)
    name = fields.CharField(max_length=255)
    picture = fields.CharField(max_length=1024, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    last_login_at = fields.DatetimeField(null=True)


class ExternalAccount(Model):
    id = fields.IntField(primary_key=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="external_accounts", null=True
    )
    provider = fields.CharField(max_length=255, choices=["google"])
    external_id = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255)
    name = fields.CharField(max_length=255)
    picture = fields.CharField(max_length=1024, null=True)

    class Meta:
        unique_together = (("provider", "external_id"),)
