import requests
import re
import json
import time
import os
from getpass import getpass  # For securely typing your password

# --- Phase 1: Selenium Imports ---
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- Configuration ---
# You can change these values to search for a different course
TARGET_TERM = "202510"
TARGET_SUBJECT = "ICS"
TARGET_COURSE_NUMBER = "433"
# --------------------

# --- URLs ---
API_URL = "https://banner9-registration.kfupm.edu.sa/StudentRegistrationSsb/ssb/searchResults/searchResults"
# This is the URL we will start at. It requires the term and will redirect to login.
LOGIN_ENTRY_URL = f"https://banner9-registration.kfupm.edu.sa/StudentRegistrationSsb/ssb/classRegistration/classRegistration"
# --------------------


def get_authenticated_session_info(username, password):
    """
    PHASE 1: THE ROBOT BROWSER
    Uses Selenium to automate the login process and scrape the necessary session data.
    
    Returns:
        A tuple containing (unique_session_id, session_cookies) if successful,
        otherwise (None, None).
    """
    print("--- Phase 1: Automating Login with Selenium ---")
    
    # Configure Chrome options. Running with a visible browser is best for debugging.
    # Once it works, you can add `options.add_argument('--headless')` to hide the window.
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless') 

    # Automatically downloads and sets up the correct driver for your version of Chrome
    print("🚀 Launching browser...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # 1. Navigate to the page. The server will see we aren't logged in and redirect us.
        driver.get(LOGIN_ENTRY_URL)
        
        # 2. Wait for the login page to load by waiting for the username field to appear.
        # This is more reliable than a fixed `time.sleep()`.
        print("⏳ Waiting for the login page to load...")
        wait = WebDriverWait(driver, 20) # Wait for a maximum of 20 seconds
        user_field = wait.until(EC.visibility_of_element_located((By.ID, "userNameInput")))

        # 3. Enter credentials and click the sign-in button.
        print("🔑 Entering credentials...")
        user_field.send_keys(username)
        driver.find_element(By.ID, "passwordInput").send_keys(password)
        driver.find_element(By.ID, "submitButton").click()
        
        # 4. After login, wait for the *next* page (the course search page) to load.
        # We'll know it's loaded when we can see the "Subject" search box.
        print("⏳ Waiting for course search page after login...")
        wait.until(EC.visibility_of_element_located((By.ID, "registerLink")))
        print("✅ Successfully logged in!")

        # 5. The page is now fully loaded. Extract the uniqueSessionId from the page's source code.
        # print("🔍 Extracting uniqueSessionId from the page...")
        # page_source = driver.page_source
        # match = re.search(r'"uniqueSessionId"\s*:\s*"(\w+)"', page_source)
        
        # if not match:
        #     print("❌ ERROR: Logged in, but could not find the uniqueSessionId on the page.")
        #     return None, None

        # session_id = match.group(1)
        # print(f"   => Found ID: {session_id}")

        # 6. Extract the login cookies from the browser session.
        print("🍪 Extracting session cookies...")
        selenium_cookies = driver.get_cookies()

        session_id = None
        
        return session_id, selenium_cookies

    except Exception as e:
        print(f"❌ An error occurred during the Selenium login process: {e}")
        return None, None
    finally:
        # 7. IMPORTANT: Always close the browser window.
        print("🚪 Closing browser.")
        driver.quit()


def fetch_course_data(cookies, session_id):
    """
    PHASE 2: THE SPEEDY MESSENGER
    Uses the session data from Selenium to make a fast API call with `requests`.
    """
    print("\n--- Phase 2: Fetching API Data with Authenticated Session ---")
    
    # Create a `requests` session object, which will act like a browser that is already logged in.
    session = requests.Session()
    
    # 1. Transfer the cookies from Selenium to our `requests` session.
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    
    # 2. Set up the parameters for our API request.
    api_params = {
        "txt_subject": TARGET_SUBJECT,
        "txt_courseNumber": TARGET_COURSE_NUMBER,
        "txt_term": TARGET_TERM,
        "uniqueSessionId": session_id,
        "pageOffset": "0",
        "pageMaxSize": "50",
        "sortColumn": "subjectDescription",
        "sortDirection": "asc"
    }

    # The Referer header is often required as a security measure.
    headers = {
        'Referer': f'https://banner9-registration.kfupm.edu.sa/StudentRegistrationSsb/ssb/classRegistration/classRegistration?term={TARGET_TERM}'
    }

    # 3. Make the final API call.
    print(f"🚀 Making API request for {TARGET_SUBJECT} {TARGET_COURSE_NUMBER}...")
    response = session.get(API_URL, params=api_params, headers=headers)
    
    if response.status_code == 200:
        print("✅ API request successful!")
        return response.json()
    else:
        print(f"❌ API request failed with status code: {response.status_code}")
        print(response.text)
        return None


# --- This is the main part of the script that runs everything ---
if __name__ == "__main__":
    # For better security, it's best to use environment variables.
    # But for now, we will ask the user to input their credentials.
    kfupm_user = os.getenv("KFUPM_USERNAME") or input("Enter your KFUPM username (e.g., s202012340): ")
    kfupm_pass = os.getenv("KFUPM_PASSWORD") or getpass("Enter your KFUPM password: ")

    # --- Execute Phase 1 ---
    unique_id, auth_cookies = get_authenticated_session_info(kfupm_user, kfupm_pass)

    # --- Execute Phase 2 (only if Phase 1 was successful) ---
    if auth_cookies:
        course_data = fetch_course_data(auth_cookies, 202273620)
        if course_data:
            print("\n" + "="*30)
            print("      COURSE DATA RECEIVED")
            print("="*30)
            # Pretty-print the JSON response
            print(json.dumps(course_data, indent=2))
            print(f"\nTotal sections found: {course_data.get('totalCount', 0)}")