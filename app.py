import logging
from ui.main_ui import run_app
from utils.db_utils import create_tables, load_menu_from_csv

# Configure logging so it always shows in terminal
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True  # Ensures Streamlit doesn't override settings
)

logging.info("✅ Starting app...")
create_tables()
logging.info("✅ Tables created.")
load_menu_from_csv()
logging.info("✅ Menu loaded from CSV.")

run_app()
