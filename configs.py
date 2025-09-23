import os 
from dotenv import load_dotenv

load_dotenv()

dark_humor_channel_id = int(os.getenv('DARK_HUMOUR_CHANNEL_ID'))
quran_file = "assets/quran.txt"
sunnah_file = "assets/sunnah.txt"
quotes_file = "assets/quote.txt"