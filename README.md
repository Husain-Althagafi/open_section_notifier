# KFUPM Course Availability Notifier

![Project Banner](https://your-image-host.com/banner.png)  <!-- Optional: Create a cool banner image -->

A multi-user Telegram bot and automated scraper that notifies students at King Fahd University of Petroleum and Minerals (KFUPM) when a spot opens up in a full course section.

[![GitHub Actions CI](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/scheduler.yml/badge.svg)](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/scheduler.yml)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🌟 Features

- **Real-Time Notifications:** Get instant alerts on Telegram the moment a seat becomes available.
- **Multi-User Support:** Any user can interact with the bot to track courses.
- **Multi-Course Tracking:** Track multiple course sections simultaneously.
- **Resilient & Automated:** A GitHub Actions-powered scraper runs every few minutes, ensuring reliable and continuous monitoring.
- **Easy to Use:** Simple, command-based interaction directly within Telegram.

## 🤖 How It Works

This project is built on a decoupled, serverless architecture, ensuring scalability and reliability.

1.  **The Telegram Bot (The Frontend):** A Python script (`bot.py`) runs 24/7 on a cloud host (e.g., Render). It listens for user commands like `/track` and `/untrack`.
2.  **The Database (The Brain):** When a user requests to track a course, the bot saves this request (user's chat ID, department, and CRN) to a central **Supabase** (PostgreSQL) database.
3.  **The Scraper (The Worker):** A GitHub Actions workflow (`scheduler.yml`) triggers the main scraping script (`course_offering.py`) on a regular schedule (e.g., every 5 minutes).
4.  **The Logic:** The scraper connects to the Supabase database to get the full list of all courses being tracked. It then makes an efficient, single API call per department to KFUPM's course offering API to check for seat availability.
5.  **The Notification:** If an open spot is found, the scraper queries the database to find all users tracking that specific course and sends a personalized notification to each one via the Telegram Bot API. The tracking request is then removed to prevent spam.

![Architecture Diagram](https://your-image-host.com/architecture.png) <!-- Optional: A diagram is great for complex projects -->

## 🚀 Getting Started

You can interact with the live bot on Telegram here: [Your Bot's Telegram Link](https://t.me/YourBotUsername)

### Telegram Bot Commands

Once you've started a chat with the bot, you can use the following commands:

-   `/start` - Display the welcome message.
-   `/track <DEPT> <CRN>` - Start tracking a specific course section.
    -   *Example:* `/track ICS 202`
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
