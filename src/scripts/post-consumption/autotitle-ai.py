import json
from datetime import datetime

from ollama import Client as OllamaClient

from paperless.postconsumption import PostConsumptionScript


class Script(PostConsumptionScript):
    def run(self):
        self.logger.info(f"Running f{self.name} post-consumption script")

        ollama_base_url = self.getenv("OLLAMA_BASE_URL")
        ollama_model = self.getenv("OLLAMA_MODEL")

        document = self.client.get_document(self.env.document_id)
        self.logger.debug(document)

        ollama = OllamaClient(host=ollama_base_url)

        self.logger.info(f"Pulling model")
        ollama.pull(ollama_model)

        self.logger.info(f"Chatting with model")
        chat_response = ollama.chat(
            model=ollama_model,
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
            format={
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "date": {"type": "string"},
                },
                "required": ["title"],
            },
            keep_alive="15m",
        )

        content = chat_response.message.content
        if not content:
            self.logger.error("Failed to generate title. No content returned.")
            return

        json_content = json.loads(content)

        title = json_content.get("title")
        if not title:
            self.logger.error("Failed to generate title. No title returned.")
            return

        date = json_content.get("date")

        self.logger.info(f"Generated title: {title}")
        self.logger.info(f"Generated date: {date}")
        self.logger.info(f"Updating document")

        document.title = title

        if date:
            try:
                date = datetime.strptime(date, "%d-%m-%Y")
                document.created = date.strftime("%Y-%m-%dT00:00:00Z")
            except Exception as e:
                self.logger.error(f"Failed to parse date: {e}")

        self.client.update_document(document)


if __name__ == "__main__":
    Script("autotitle").run()
