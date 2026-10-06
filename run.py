from dotenv import load_dotenv

load_dotenv()

# pylint: disable=wrong-import-position
from src.main.server.server import app  # noqa: E402

# pylint: enable=wrong-import-position


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
