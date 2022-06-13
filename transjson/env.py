from dotenv import load_dotenv
from os import getenv

load_dotenv()

auth_key = getenv("AUTH_KEY")

if languages := getenv("a"): 
    default_languages = list(languages)
else: 
    default_languages = None
