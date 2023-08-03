from datetime import datetime
from app.models.model import TranslationRequest


class SaveResponse:

    @classmethod
    async def save_translation_request(cls, source_language, target_language, api_used, translation_success):
        timestamp = datetime.utcnow()

        request = TranslationRequest(
            source_language=source_language,
            target_language=target_language,
            api_used=api_used,
            translation_success=translation_success,
            timestamp=timestamp
        )
        await request.save()