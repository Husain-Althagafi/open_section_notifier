import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def send_request():

    """
    Send a GET request to the course-offering.com API to retrieve course data.

    Returns the JSON response containing course information for the specified department and CRN.

    """

    # Configuration for the request
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'origin': 'https://course-offering.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://course-offering.com/',
        'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    }

    # dept_code = input("Enter department code (e.g., ICS): ")

    params = {
        'term_code': '202510',
        'department_code': 'ICS',
        'bcs': 'HH99-UTRR-9K9K-RRRR-FE69',
    }

    response = requests.get('https://us-east1-course-offering-us-east1.cloudfunctions.net/courses', params=params, headers=headers)

    # CRN = input("Enter CRN (e.g., 13912): ")

    # for course in response.json()['data']:
    #     if course['crn'] == CRN:
    #         print('COURSE FOUND BY CRN:', CRN)
    #         print(json.dumps(course, indent=4))
    i = 0
    for course in response.json()['data']:
        if i < 5:
            is_open(course)
            i+=1

        if course['name'] == 'ICS433' and course['sections'][0]['schedule']['time']['start'] == '1000':
            print('COURSE FOUND')
            print(json.dumps(course, indent=4))
            is_open(course)



def send_telegram_message(message_text):

    """
    Send a message via Telegram bot. Uses github secrets for bot token and chat ID.
    
    """

    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("Error with telegram bot")
        return
    
    api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    escaped_text = message_text.replace("-", "\\-").replace(".", "\\.").replace("!", "\\!")

    payload = {
        'chat_id': chat_id,
        'text': escaped_text,
        'parse_mode': 'MarkdownV2'
    }

    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()     
        print("Telegram notification sent successfully")
    except requests.exceptions.RequestException as e:
            print(f"Error sending Telegram message: {e}")


def is_open(course):

    """
    Check if a course section is open based on its if there are available seats.

    """

    max_seats = course['capacity']['seats']['maximum']
    taken_seats = course['capacity']['seats']['taken']
    available_seats = max_seats - taken_seats
    
    if available_seats > 0:
        print("SECTION HAS OPEN SEATS")
        message = f"Section {course['crn']} of course: {course['name']} is open with {available_seats} available seats!"
        send_telegram_message(message)
    else:
        print("SECTION IS FULL")
    
      

if __name__ == "__main__":
    print("Retreiving course data from course-offering.com")
    send_request()