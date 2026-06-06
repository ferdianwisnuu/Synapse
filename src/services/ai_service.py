import os
import aiohttp
from src.utils.logger import setup_logger

logger = setup_logger("Service")

class AIService:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.history = {}

    def _get_user_history(self, user_id: int):
        if user_id not in self.history:
            self.history[user_id] = [
                {
                    "role": "system", 
                    "content": (
                        "Kamu adalah Synapse, asisten digital serba bisa untuk ekosistem server Discord"
                        "Gaya bicaramu cerdas, responsif, kasual, dan ramah. "
                        "Wajib memberikan jawaban yang ringkas, informatif, dan mudah dipahami dalam sekali baca. "
                        "Selalu optimalkan format Markdown, dan berikan snippet kode yang efisien serta terdokumentasi jika membahas pemrograman."
                    )
                }
            ]
        return self.history[user_id]

    def add_message(self, user_id: int, role: str, content: str):
        history = self._get_user_history(user_id)
        history.append({"role": role, "content": content})
        self.history[user_id] = [history[0]] + history[1:][-10:]

    def clear_user_memory(self, user_id: int) -> bool:
        if user_id in self.history:
            del self.history[user_id]
            logger.info(f"Memori percakapan {user_id} dibersihkan.")
            return True
        return False

    async def generate_response(self, user_id: int, username: str, channel_name: str, user_message: str) -> str:
        contextual_message = f"[Pesan dari @{username} di channel #{channel_name}]: {user_message}"
        self.add_message(user_id, "user", contextual_message)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "your models",
            "messages": self.history[user_id],
            "temperature": 0.4
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.base_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        answer = data['choices'][0]['message']['content']
                        self.add_message(user_id, "assistant", answer)
                        logger.info(f"Berhasil memproses pesan dari @{username}")
                        return answer
                    else:
                        logger.warning(f"OpenRouter mengembalikan status HTTP {response.status}")
                        if user_id in self.history and len(self.history[user_id]) > 1:
                            self.history[user_id].pop()
                        raise Exception("API Error")
            except Exception as e:
                logger.error(f"Gagal menghubungi OpenRouter: {e}")
                if user_id in self.history and len(self.history[user_id]) > 1:
                    self.history[user_id].pop()
                raise Exception("API Error")
