import os

# Runs before pytest imports any test module, so modules that read
# DATABASE_URL at import time (src/database/connection.py) find it set.
# Overrides any value from the shell so tests never touch a real database.
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
