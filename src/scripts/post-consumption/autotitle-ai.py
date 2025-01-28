import json
from datetime import datetime

from openai import OpenAI
from pydantic import BaseModel

from paperless.postconsumption import PostConsumptionScript


class ResponseFormat(BaseModel):
    title: str
    date: str


class Script(PostConsumptionScript):
    def run(self):
        self.logger.info(f"Running {self.name} post-consumption script")

        openai_base_url = self.getenv("OPENAI_BASE_URL", "")
        openai_api_key = self.getenv("OPENAI_API_KEY", "")
        openai_model = self.getenv("OPENAI_MODEL")

        document = self.client.get_document(self.env.document_id)

        openai_client = OpenAI(
            base_url=openai_base_url or None,
            api_key=openai_api_key or None,
        )

        self.logger.info(f"Chatting with model")
        completion = openai_client.beta.chat.completions.parse(
            messages=[
                {
                    "role": "system",
                    "content": "You are given the content of a document. Generate a title for it. Find the date of the document if there is one. Return a JSON object with the title and the date of the document. Format the date as a string in the format DD-MM-YYYY.",
                },
                {
                    "role": "user",
                    "content": document.content,
                },
            ],
            response_format=ResponseFormat,
            model=openai_model,
            max_tokens=512,
            temperature=0.7,
            top_p=0.7,
            presence_penalty=0,
        )

        result = completion.choices[0].message.parsed
        if not result:
            self.logger.error("Failed to generate title. No content returned.")
            return

        if not result.title:
            self.logger.error("Failed to generate title. No title returned.")
            return

        self.logger.info(f"Generated title: {result.title}")
        self.logger.info(f"Generated date: {result.date}")
        self.logger.info(f"Updating document")

        document.title = result.title

        if result.date:
            try:
                date = datetime.strptime(result.date, "%d-%m-%Y")
                document.created = date.strftime("%Y-%m-%dT00:00:00Z")
            except Exception as e:
                self.logger.error(f"Failed to parse date: {e}")

        self.client.update_document(document)


if __name__ == "__main__":
    Script("autotitle").run()
