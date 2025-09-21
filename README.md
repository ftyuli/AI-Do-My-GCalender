# Ai-Do-My-GCalender
Have you hating doing your GCalendar and Tasks from a schedule or syliabus?
Well you come to the right place.

Get AI To do it for you!

With an AI prompt that accompanies this Python script, you can convert your schedules and syliabuses into actionable events and tasks in your GCalender/GTasks.

---

## Features
* Use The provided AI Prompt to generate a CSV file from your schedule or syliabus attached
* Read CSV files from an `imports/` folder
* Creates Google Calendar events for items marked as `"event"`.
* Creates Google Tasks for items marked as `"task"`.
* Handles local timezones automatically and converts task due dates to UTC.
* Moves processed CSV files to an `exhausted/` folder to avoid duplicates.
* Works with multiple CSV files at once.

---

## Setup 

This script needs python (presumable the latest version) and acess to google API for GTasks and GCalender.

### 1. Download Code or Clone the repository

Download the code as ZIP and unzip it in your desired directory or just clone it to there if you know how to do that.

### 2. Install dependencies

Required python dependancies include:

* `google-api-python-client`
* `google-auth-httplib2`
* `google-auth-oauthlib`
* `tzlocal`

You can run the following pip command to install them:

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib tzlocal
```

### 3. Setting up Google APIs

To allow the script to create events and tasks in your GTasks and GCalender, it will need both credentials for **Google Calendar API** and **Google Tasks API**.


1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Navigate to **APIs & Services → Library**:
   * Enable **Google Calendar API**
   * Enable **Google Tasks API**
4. Go to **APIs & Services → Credentials → Create Credentials → OAuth client ID**:
   * Application type: **Desktop App** 
   * Download the JSON file and save it as `credentials.json` in the `credentials/` folder.
5. The first time you run the script, it will open a browser to authorize your account and store the token in `token/token.json`.

---

## Usage

1. Place your CSV files in the `imports/` folder.
2. Run the script:

```bash
python3 main.py
```

3. The script will:

   * Read each CSV row
   * Create events or tasks based on the `action` column
   * Move processed CSVs to `exhausted/`

---

## CSV Format

The CSV must have the following **case-sensitive headers**:

```
title,location,description,start,end,action
```

* `title` – descriptive title (mandatory)
* `location` – location of event (optional)
* `description` – extra details (optional)
* `start` – start datetime for events (`YYYY-MM-DD HH:MM`), leave empty for tasks
* `end` – end datetime for events or due date for tasks (`YYYY-MM-DD HH:MM`)
* `action` – `"event"` or `"task"`

### CSV Example:

```
title,location,description,start,end,action
landery meeting,home,meeting with the gang bout doing laundery,2025-10-10 14:00,2025-10-10 16:00,event
doing da laundry,,do yo laundery,,2025-10-12 14:00,task
```

---

## AI Prompt to Generate CSV Files

You can generate structured CSV files from images or PDFs using the following prompt:

```
You convert schedules from images or PDFs into structured CSV files.

Instructions:
1. Extract all schedule information from the attached file.
2. Use the following case-sensitive CSV columns exactly: 
   title, location, description, start, end, action
3. Every item MUST have a title. If the original schedule does not provide one, generate a descriptive shorthand title that includes:
   - Class or course name if applicable
   - A short description of the task or event  
   Examples: "STAT 151 Class, read mod 1-2" or "ENGL 102 Class, read Romeo and Juliet"
4. Wrap any text that contains commas in double quotes so the CSV layout remains valid.
5. Events (such as classes or exams) MUST have both 'start' and 'end' times, including **hours and minutes** in the format HH:MM (24-hour clock). Dates alone are not sufficient.
6. If an item only has a date but is missing a start or end time, **treat it as a task**, using the date as the 'end' column.
7. Tasks (such as assignments or deadlines) use the 'end' column for the due date. 
8. If an item is part of a class, course, or larger context, include that name at the front of the title in the shorthand style.
9. Ensure all dates and times are in the format YYYY-MM-DD HH:MM (24-hour clock).
10. If a field is missing in the original schedule and cannot be inferred, leave it empty.
11. Output ONLY valid CSV code, with no extra explanation or commentary.
12. The first row of the CSV must be the header.

Example Output:

title,location,description,start,end,action
STAT 151 Class, read mod 1-2,Room 204,Read module 1-2,2025-09-22 09:00,2025-09-22 10:00,event
Laundry Task,,Do laundry,,2025-09-23 14:00,task

Attached file:
```

---

## License

???

