import requests
import base64

class GeminiService:
    def __init__(self):
        self.API_KEY = "96565cca3262ef86d682243522f70acc3969235e4d8cf055f6116e6f5a4871190b5d988feb254771c46115fc3fd89e52"

    def generate_image(self, prompt, style="No specific style"):
        try:
            response = requests.post(
                "https://clipdrop-api.co/text-to-image/v1",
                headers={
                    "x-api-key": self.API_KEY
                },
                files={
                    "prompt": (None, prompt)
                }
            )

            # ❗ Error check
            if response.status_code != 200:
                return False, response.text

            # Convert image to base64
            img_base64 = base64.b64encode(response.content).decode()

            return True, img_base64

        except Exception as e:
            return False, str(e)

    def generate_prompt_suggestions(self, category=None):
        return [
            "A cyberpunk city at night",
            "A futuristic robot",
            "A dragon flying in the sky",
            "A realistic human portrait",
            "A fantasy world landscape"
        ]