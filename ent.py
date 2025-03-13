import time
import logging
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from telegram import Bot
from telegram.error import TelegramError
# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Telegram Bot Settings
TELEGRAM_BOT_TOKEN = "your-telegram-bot-token"
TELEGRAM_CHAT_ID = "your-chat-id"

def send_telegram_message(message):
    """Send status updates to Telegram"""
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except TelegramError as e:
        logging.error(f"Telegram message failed: {e}")

# Load multiple RentMasseur accounts from a JSON file
def load_accounts():
    with open("accounts.json", "r") as file:
        return json.load(file)

def initialize_driver():
    """Initialize headless Selenium WebDriver"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        return driver
    except Exception as e:
        logging.error(f"Driver initialization failed: {e}")
        return None

def login(driver, email, password):
    """Login to RentMasseur"""
    driver.get("https://rentmasseur.com/login")
    logging.info(f"🌍 Opening RentMasseur login page for {email}")

    try:
        # Wait for login fields to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        
        # Enter credentials
        driver.find_element(By.ID, "email").send_keys(email)
        driver.find_element(By.ID, "password").send_keys(password)
        
        # Click login
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        logging.info(f"🔑 {email} - Login attempt submitted.")

        # Wait for homepage to load
        time.sleep(3)

        # Check for failed login (invalid credentials)
        if "Invalid email or password" in driver.page_source:
            logging.error(f"❌ Login failed for {email} - Invalid credentials.")
            send_telegram_message(f"❌ Login failed for {email} - Invalid credentials.")
            return False
        
        return True

    except Exception as e:
        logging.error(f"⚠️ Login error for {email}: {e}")
        return False

def toggle_availability(driver, email):
    """Click the availability button after login"""
    try:
        availability_button_xpath = "//a[contains(@href, '/availability')]"
        availability_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, availability_button_xpath))
        )
        availability_button.click()
        logging.info(f"✅ {email} - Availability toggled successfully.")
        send_telegram_message(f"✅ {email} - Availability updated.")

    except Exception as e:
        logging.error(f"⚠️ {email} - Failed to toggle availability: {e}")
        send_telegram_message(f"⚠️ {email} - Availability update failed.")

def main():
    """Execute full automation process across multiple accounts"""
    accounts = load_accounts()

    for account in accounts:
        driver = initialize_driver()
        if not driver:
            continue

        try:
            email = account["email"]
            password = account["password"]

            if login(driver, email, password):
                toggle_availability(driver, email)
                send_telegram_message(f"✅ {email} - Profile updated successfully.")
        finally:
            driver.quit()

if __name__ == "__main__":
    main()