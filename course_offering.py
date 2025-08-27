import requests
import json
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# --- Initialize database ---

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)



def get_seats_in_dept(dept, crn_list):

    """
    Checks a section for available seats

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

    # TODO add logic for getting current term_code 

    params = {
        'term_code': '202510',
        'department_code': dept,
        'bcs': 'HH99-UTRR-9K9K-RRRR-FE69',
    }

    try:    
        print(f'Getting seat info for {dept}')


        response = requests.get('https://us-east1-course-offering-us-east1.cloudfunctions.net/courses', params=params, headers=headers)
        response.raise_for_status()

        all_sections_in_dept = response.json().get('data', [])
        tracked_sections = []

        for section in all_sections_in_dept:
            if section.get('crn') in crn_list:
                tracked_sections.append(section)

        sections_with_available_seats = []

        for section in tracked_sections:
            max_seats = section.get('capacity', {}).get('seats', {}).get('maximum', 0)
            taken_seats = section.get('capacity', {}).get('seats', {}).get('taken', 0)
            if max_seats > taken_seats:
                sections_with_available_seats.append((section.get('crn'), max_seats - taken_seats))   #store tuples (crn, available seats)
        
        return sections_with_available_seats

    except requests.exceptions.RequestException as e:
        print(f"Error making request for {dept} {crn_list}: {e}")
        return []
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error parsing response for {dept} {crn_list}: {e}")
        return []
    


def get_sections_to_track():
    """
    Finds all departments and crns that should be tracked from database

    """

    try:
        response = supabase.table('tracking_requests').select('dept_code, crn').execute()

        unique_courses = set()

        for item in response.data:
            unique_courses.add((item['dept_code'], item['crn']))

        return list(unique_courses)
    
    except Exception as e:
        print(f"Error fetching unique courses from database: {e}")
        return []

def get_users_tracking_section(crn):
    """
    Gets all users tracking a specfic section. will use to find all users tracking each section we find that has available seats that was tracked
    """

    try:
        response = supabase.table('tracking_requests').select('user_chat_id').eq('crn', crn).execute()

        return [user['user_chat_id'] for user in response.data]
    
    except Exception as e:
        print(f"Error fetching users for course {crn}: {e}")
        return []
    
    
def remove_tracking_after_found(crn):
    """
    Deletes all tracking requests for all courses that were found and had the information sent out
    """

    try:
        supabase.table('tracking_requests').delete().eq('crn', crn).execute()
        print(f"Successfully removed tracking requests for {crn}.")
    except Exception as e:
        print(f"Error removing tracking requests for {crn}: {e}")


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

    
def main():
    print('--- Starting Scraping Run ---')

    # find all courses to check 

    sections_to_check = get_sections_to_track()

    if not sections_to_check:
        print("No courses are currently being tracked. Exiting.")
        return
    
    print(f'Found {len(sections_to_check)} unqiue sections to track')

    # build a dict that contains each tracked department and the tracked crns within it 
    dept_crn = {}

    for dept, crn in sections_to_check:
        if dept not in dept_crn.keys():
            dept_crn[dept] = []
        dept_crn[dept].append(crn)
    
    print(f'--- Tracked Sections ---')
    
    for dept in dept_crn.keys():
        for crn in dept_crn[dept]:
            print(f'dept: {dept} crn {crn}')

    print(f' --- Getting Seat Data ---')
    # for each dict we will send a request with all the crns under it

    sections_with_available_seats = []

    for dept in dept_crn.keys():
        sections_with_available_seats_for_dept = get_seats_in_dept(dept, dept_crn[dept])
        print(sections_with_available_seats_for_dept)
    
        
        


if __name__ == "__main__":
    main()