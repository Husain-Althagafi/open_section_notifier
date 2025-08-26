import requests
import json

def send_request():

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

    dept_code = input("Enter department code (e.g., ICS): ")

    params = {
        'term_code': '202510',
        'department_code': dept_code,
        'bcs': 'HH99-UTRR-9K9K-RRRR-FE69',
    }

    response = requests.get('https://us-east1-course-offering-us-east1.cloudfunctions.net/courses', params=params, headers=headers)

    # CRN = input("Enter CRN (e.g., 13912): ")

    # for course in response.json()['data']:
    #     if course['crn'] == CRN:
    #         print('COURSE FOUND BY CRN:', CRN)
    #         print(json.dumps(course, indent=4))

    for course in response.json()['data']:
        if course['name'] == 'ICS433' and course['sections'][0]['schedule']['time']['start'] == '1000':
            print('COURSE FOUND')
            print(json.dumps(course, indent=4))
            

if __name__ == "__main__":
    print("Retreiving course data from course-offering.com")

    send_request()