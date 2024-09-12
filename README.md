# Tech58 Project - Django
---
#### Description
Cnm58 project for 'CnM' Website is built in Python (Django)
#### Requirements
* **Python = 3.10.5
* Django = 5.1.1
* django-environ==0.11.2
### Configuration Instructions
* **Step 1:** Clone the Git Repository
  `git clone https://github.com/coderdigi01/HRMS.git`
* **Step 2:** CD into that directory
 `cd tech58`
* **Step 3:** Install Virtual Env (If not already installed)
 **For Ubuntu:** `sudo apt-get install virtualenv`
 **For MacOS:** `brew install virtualenv`
* **Step 4:** Create a Virtual Environment
  `virtualenv -p python3.10 venv`
* **Step 5:** Activate Virtual Environment
 `venv\Scripts\Activate`
* **Step 6:** Install Requirements
 `pip install -r requirements.txt`
* **Step 7:** Create .env file from sample
* **Step 8:** Run Migrations
 `python manage.py migrate`
* **Step 9:** Run Development Server
 `python manage.py runserver`