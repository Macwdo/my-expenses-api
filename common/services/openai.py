

import openai
from django.conf import settings


class OpenAiService:
    def __init__(self):
        self._api_key = settings.OPENAI_API_KEY
        self._organization = settings.OPENAI_ORGANIZATION
        self._model = "gpt-4o-mini"
        _instance = openai
        _instance.api_key = self._api_key
        _instance.organization = self._organization

        self.instance = _instance
    
    def prompt(self, text):
        completion = self.instance.chat.completions.create(
            model=self._model,
            messages=[
                {
                    "role": "system",
                    "content": text,
                }
            ],
        )
    
        return completion.choices[0].message.content