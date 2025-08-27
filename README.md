# KFUPM Course Availability Notifier


A multi-user Telegram bot (for now, but i dont like telegram so might make some other version) and automated scraper that notifies students at King Fahd University of Petroleum and Minerals (KFUPM) when a spot opens up in a full course section.

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🌟 Features

- **Notifications via Telegram:** The scraper runs every 10 or so minutes using Github Actions, sending out notifications for tracked sections if they have available seating. If you want you can easily host it somewhere else where you can have it running much more frequently.
- **Multi-User Support:** Anyone can interact with the bot just search the bot name qvcCourseTrackerBot on telegram and you can start a chat and start using it so long as the telebot script is being run somewhere.
- **Multi-Course Tracking:** Can track multiple course sections simultaneously.

## 🤖 How It Works

If you want to use the bot you are gonna have to run some things locally since I won't keep the bot script running myself. But it is really easy to set up I'll have instructions here.

- **telebot.py** This is the script for hosting the bot and its commands, you will need this running either on a server or locally. You only need this running when making the tracking request, the tracking itself and the notifications dont need this script.
- **course_offering.py** This is the automation script. I'll probably keep this running with actions but if I dont sorry. This is whats needed for the tracking and the notifying of available sections.
- If you want to run everything yourself then you will need to set up your own supabase database. ezez



## 🚀 Getting Started

You can interact with the live bot on Telegram here: (https://t.me/qvcCourseTrackerBot)

### Telegram Bot Commands

Once you've started a chat with the bot, you can use the following commands:

-   `/start` - Display the welcome message.
-   `/track <DEPT> <CRN>` - Start tracking a specific course section.
    -   *Example:* `/track ICS 202`
 
These aren't done yet TODO
-   `/untrack <DEPT> <CRN>` - Stop tracking a course section.
    -   *Example:* `/untrack ICS 202`
-   `/mycourses` - List all the courses you are currently tracking.

---


Speedrun tutorial (should write a better one later):

gonna assume u dont need tutorial for the supabase stuff
1. fork the repo
2. clone it locally
3. cd into repo
4. make a venv and install the requirements
5. set up a .env with the required information
6. have a 2nd terminal where u run the telebot.py script (now the telegram bot and the storing of track requests in the database should work
7. check that the github actions is working and it should run the course_offering.py script around every ten minutes

i think thats it, very simple and not polished but ill fix those in time if i feel like it

thanks for looking at my work <3



