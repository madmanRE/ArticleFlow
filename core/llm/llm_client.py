from openai import OpenAI


class LLMClient:
    def __init__(
            self,
            base_url: str,
            api_key: str,
            model: str,
            temperature: float = 0.5
    ) -> None:
        self._base_url = base_url
        self._api_key = api_key
        self._model = model
        self._temperature = temperature
        self._client = self._get_client()

    def _get_client(self):
        return OpenAI(base_url=self._base_url, api_key=self._api_key)

    def make_response(self, messages) -> str:
        response = self._client.chat.completions.create(
            model=self._model, messages=messages, temperature=self._temperature
        )
        data = response.choices[0].message.content

        return data
