from dotenv import load_dotenv
import os

load_dotenv()

URL_BASE = os.getenv('URL_BASE')
AUTH_BASIC = os.getenv('AUTH_BASIC')

headers = {'Authorization': f"Basic {AUTH_BASIC}"}

DEEPL_AUTH_KEY = os.getenv('DEEPL_AUTH_KEY')
DEEPL_LANG = os.getenv('DEEPL_LANG', 'ES')
