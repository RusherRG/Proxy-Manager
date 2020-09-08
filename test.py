import time
from tests.runner import setup, run
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    setup()
    time.sleep(4)
    run()
