from django.conf import settings
import os
import requests
import numpy as np


class APIEmbeddings:
    def __init__(self):
        self.token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
        if self.token == "your-token-here":
            self.token = None
        self.model = settings.EMBEDDING_MODEL
        self.api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{self.model}"
        self.headers = {}
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"

    def embed_documents(self, texts):
        return [self._embed(text) for text in texts]

    def embed_query(self, text):
        return self._embed(text)

    def _embed(self, text):
        response = requests.post(
            self.api_url,
            headers=self.headers,
            json={"inputs": text}
        )
        if response.status_code != 200:
            raise Exception(f"Embedding API error: {response.status_code} {response.text}")
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            if isinstance(result[0], list):
                return [float(x) for x in np.mean(result, axis=0)]
            return [float(x) for x in result]
        return result
