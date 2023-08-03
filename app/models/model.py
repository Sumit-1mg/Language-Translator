from tortoise.models import Model
from tortoise import fields, Tortoise

class TranslationRequest(Model):
    id = fields.IntField(pk=True)
    source_language = fields.CharField(max_length=50)
    target_language = fields.CharField(max_length=50)
    api_used = fields.CharField(max_length=100)
    translation_success = fields.BooleanField()
    timestamp = fields.DatetimeField()

    class Meta:
        table = "translation_requests"

class InitDatabase:
    @classmethod
    async def init_db(cls):
        await Tortoise.init(
            db_url='sqlite://db.sqlite3',
            modules={'models': ['app.models.model']}
        )
        await Tortoise.generate_schemas()