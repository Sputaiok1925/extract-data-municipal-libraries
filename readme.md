# Municipal Libraries Data Fetcher

This Python script fetches data about municipal libraries from the [Golemio API](https://api.golemio.cz/docs/openapi/#/%F0%9F%8F%A2%EF%B8%8F%20Municipal%20Libraries%20(v2)), saves it into a CSV file, and automatically updates it every day at 7:00 AM (Prague time).

---

## Code Description

The script is structured into three main parts:

1. **Fetching data from API**
   - Uses the `requests` library to call the Golemio API.
   - API authentication is done by passing an API key in the request headers (loaded from a `.env` file).

2. **Extracting and saving data**
   - Extracts relevant fields like library name, address, coordinates, and opening hours.
   - Saves everything into a CSV file called `municipal_libraries.csv` using `pandas`.

3. **Scheduler for automatic updates**
   - Uses the `APScheduler` library to schedule automatic daily updates at 7:00 AM (Europe/Prague timezone).
   - On the first run, it checks if the output file exists — if not, it downloads the data right away.

---

## How to run this code on your PC

### 1. Clone the repository or сopy the code to your IDE

### 2. Install the necessary libraries
`requests`<br>
 Used for sending HTTP requests to the API and retrieving data.<br>
`pandas`<br>
 Allows creating a table (DataFrame) and saving the retrieved data into a CSV file.<br>
`json`<br>
 Helps with decoding API responses in JSON format and processing data.<br>
`os`<br>
 Used for interacting with system variables, such as retrieving the API key and checking file existence.<br>
`BlockingScheduler` (from `apscheduler.schedulers.blocking`)<br>
 Enables scheduling automatic execution of the function for data updates.<br>
`pytz`<br>
 Used to set the correct time zone for the scheduler (`Europe/Prague`).<br>
`dotenv`<br>
 Allows loading environment variables (e.g., API key) from a `.env` file.<br>
`datetime`<br>
 Used for working with date and time, such as logging the current timestamp during data updates.<br>
### 3. Golemio token
Get your API KEY on [generate your token ](https://api.golemio.cz/api-keys), and assign it to the API_KEY variable 
### 4. Run the code
At the first start the file with data municipal_libraries.csv is automatically created, then this file is automatically updated at 7.00 Prague time.

---

## Why I chose this implementation approach

I designed this solution with simplicity, reliability, and automation in mind.

- **Simplicity & Readability**
I used standard and widely-known Python libraries like `requests` and `pandas` so that anyone with basic Python knowledge can read and modify the code.

- **Secure API Key Management**
Instead of hardcoding API keys, I use a `.env` file and `python-dotenv`. This prevents accidental leaks and is a best practice in real-world projects.

- **Automatic Daily Updates**
By using `APScheduler`, the script handles its own scheduling without needing `cron` jobs or `Docker`. It’s lightweight and works on any platform.

- **Portable CSV Output**
The data is saved in UTF-8 encoded CSV format (`municipal_libraries.csv`), making it easy to open in Excel, Python, or any other data tool.

- **Error Handling**
The script includes error handling for API failures and JSON decoding problems, so it won't crash during daily runs.

### Why This Approach Works Well
- **Easy to run** on a personal computer
- **Ready for future improvements** (like adding more fields)
- **Reliable for daily use** without manual effort
