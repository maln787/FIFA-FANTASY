from main import app
import os

if __name__ == "__main__":
    app.run(port=int(os.getenv('APP_PORT')))
