import requests
import json
import time
import re








SEARCH_URL = "https://banner9-registration.kfupm.edu.sa/StudentRegistrationSsb/ssb/classRegistration/classRegistration"

API_URL = "https://banner9-registration.kfupm.edu.sa/StudentRegistrationSsb/ssb/searchResults/searchResults"

search_params = {
    'TARGET_CRN' : "21588",
    'TARGET_TERM' : "202510",
    'TARGET_SUBJECT' : "ICS",
    'TARGET_COURSE_NUMBER' : "433"
}

# will return a json object like this:

# loop over the res.data.data for each course found, check if course.courseReferenceNumber matches the CRN you want
# then check course.status.sectionOpen to see if the course is open or not

# {
#   "success": true,
#   "totalCount": 14,
#   "data": 
#   [
#     {
#       "id": 762052,
#       "term": "202510",
#       "termDesc": "First Semester 2025-26",
#       "courseReferenceNumber": "13230",
#       "partOfTerm": "1",
#       "courseNumber": "433",
#       ......
#      }
#   ]


if __name__ == "__main__":
    print("Starting course availability checker...")

