from dotenv import load_dotenv
import os

load_dotenv()

os.environ["TMDB_LANGUAGE"] = ""

URL_BASE = os.getenv('WP_URL_BASE')
AUTH_BASIC = os.getenv('WP_AUTH_BASIC')

headers = {'Authorization': f"Basic {AUTH_BASIC}"}

DEEPL_AUTH_KEY = os.getenv('DEEPL_AUTH_KEY')
DEEPL_LANG = os.getenv('DEEPL_LANG', 'ES')
DEEPL_FROM_TO_LANG = os.getenv('DEEPL_FROM_TO_LANG', 'FR')

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# https://developers.cloudflare.com/images/cloudflare-images/api-request/
CF_ACCOUNT_ID = os.getenv('CF_ACCOUNT_ID')
CF_API_TOKEN = os.getenv("CF_API_TOKEN")
cf_headers = {'Authorization': f"Bearer {CF_API_TOKEN}"}
