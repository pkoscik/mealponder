import logging
import os

DATA_DIR = "data"
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
DB_FILE = os.path.join(DATA_DIR, "app.db")

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}

# Logger Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mealponder")