from dotenv import load_dotenv
import os

load_dotenv()

URL_BASE = os.getenv('URL_BASE')
AUTH_BASIC = os.getenv('AUTH_BASIC')
