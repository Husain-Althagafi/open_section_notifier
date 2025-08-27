# KFUPM Course Availability Notifier


A multi-user Telegram bot (for now) and automated scraper that notifies students at King Fahd University of Petroleum and Minerals (KFUPM) when a spot opens up in a full course section.

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🌟 Features

- **Notifications via Telegram:** The scraper runs every 10 or so minutes using Github Actions, sending out notifications for tracked sections if they have available seating. If you want you can easily host it somewhere else where you can have it running much more frequently.
- **Multi-User Support:** Anyone can interact with the bot just search the bot name qvcCourseTrackerBot on telegram and you can start a chat and start using it so long as the telebot script is being run somewhere.
- **Multi-Course Tracking:** Can track multiple course sections simultaneously.

## 🤖 How It Works

If you want to use the bot you are gonna have to run some things locally since I won't keep the bot script running myself. But it is really easy to set up I'll have instructions here.

1. **telebot.py** This is the script for hosting the bot and its commands, you will need this running either on a server or locally. You only need this running when making the tracking request, the tracking itself and the notifications dont need this script.
2. **course_offering.py


## 🚀 Getting Started

You can interact with the live bot on Telegram here: [Your Bot's Telegram Link](https://t.me/qvcCourseTrackerBot)

### Telegram Bot Commands

Once you've started a chat with the bot, you can use the following commands:

-   `/start` - Display the welcome message.
-   `/track <DEPT> <CRN>` - Start tracking a specific course section.
    -   *Example:* `/track ICS 202`
 
TODO
-   `/untrack <DEPT> <CRN>` - Stop tracking a course section.
    -   *Example:* `/untrack ICS 202`
-   `/mycourses` - List all the courses you are currently tracking.

---

## 🛠️ Setting Up for Development (For Contributors)

Interested in contributing or running your own instance? Follow these steps.

### Prerequisites

-   Python 3.11+
-   A Telegram account
-   A Supabase account
-   A GitHub account

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
