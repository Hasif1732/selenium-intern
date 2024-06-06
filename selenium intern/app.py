from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymongo
import uuid
from datetime import datetime
import requests
import time

app = Flask(__name__)

@app.route('/run_selenium_script', methods=['POST'])
def run_selenium_script():
    try:
        # Set up ProxyMesh credentials
        username = "@shaik95580"
        password = "Taharnisha@999"
        hostname = "us-wa.proxymesh.com"
        port = 31280

        # Set up Chrome options with ProxyMesh
        options = webdriver.ChromeOptions()
        options.add_argument(f"--proxy-server=http://{username}:{password}@{hostname}:{port}")

        # Create a new Chrome driver instance
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Navigate to the Twitter homepage
        driver.get("https://twitter.com/")
        time.sleep(5)  # Give the browser 5 seconds to load the page

        # Log in to Twitter (replace with your own credentials)
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "input"))
        )
        username_input.send_keys("@HShaik958865388")

        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@role, 'button')]"))
        )
        next_button.click()

        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@name, 'password')]"))
        )
        password_input.send_keys("Taharnisha@999")

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@data-testid, 'LoginForm_Login_Button')]"))
        )
        login_button.click()

        # Wait for the page to load
        time.sleep(5)

        # Find the "What's Happening" section
        whats_happening = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-testid='WhatsHappening']"))
        )

        # Find the top 5 trending topics
        trending_topics = whats_happening.find_elements(By.XPATH, "//div[@data-testid='Trend']")[:5]

        # Create a unique ID for this run
        unique_id = uuid.uuid4()

        # Get the current date and time
        end_time = datetime.now()

        # Get the IP address used
        ip_address = requests.get('https://api.ipify.org').text

        # Create a document to store in MongoDB
        document = {
            "_id": unique_id,
            "trend1": trending_topics[0].text,
            "trend2": trending_topics[1].text,
            "trend3": trending_topics[2].text,
            "trend4": trending_topics[3].text,
            "trend5": trending_topics[4].text,
            "end_time": end_time,
            "ip_address": ip_address
        }

        # Connect to MongoDB
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["twitter_trends"]
        collection = db["trends"]

        # Insert the document into MongoDB
        collection.insert_one(document)

        # Return the results as JSON
        results = {
            "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "ip_address": ip_address,
            "trend1": trending_topics[0].text,
            "trend2": trending_topics[1].text,
            "trend3": trending_topics[2].text,
            "trend4": trending_topics[3].text,
            "trend5": trending_topics[4].text
        }
        return jsonify(results)

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)})

    finally:
        # Close the browser
        driver.quit()

if __name__ == '__main__':
    app.run(debug=True)