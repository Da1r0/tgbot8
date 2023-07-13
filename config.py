import os
from dataclasses import dataclass
import dotenv


@dataclass
class TGBot:
    token: str


dotenv.load_dotenv()

config = TGBot(token=os.getenv('BOT_TOKEN'))