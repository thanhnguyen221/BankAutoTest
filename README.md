# 🏦 BankAutoTest - Automated Banking System Testing

![Selenium](https://img.shields.io/badge/-Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![Python](https://img.shields.io/badge/-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/-Django-092E20?style=for-the-badge&logo=django&logoColor=white)

An advanced, hybrid automated testing framework designed for a Map-based Banking Management System. This project seamlessly integrates deep Backend API validation with highly observable Frontend UI automation, featuring a custom JavaScript injection engine (the "Flying Head") for real-time test monitoring and execution.

## 📺 Video Demo
Watch the "Flying Head" automation logic in action:


https://github.com/user-attachments/assets/77fb6d29-ecea-4ab2-877f-823e9383c90a



> [!TIP]
> The video above demonstrates the full automated flow from login to marker validation.

---

## ✨ Key Features

* **Hybrid Test Execution:** Combines Django's native `TestCase` for backend logic with Selenium WebDriver for frontend UI interactions within a single, unified controller.
* **Visual Tracking Engine:** An advanced JavaScript injector that calculates precise element coordinates, animates a tracker to the target, applies focus effects, and simulates actual DOM mouse events.
* **Dynamic Data Entry:** Features a realistic asynchronous "typewriter" effect with element highlighting for inputting data into forms, making execution highly observable.
* **Smart Tab & Map Handling:** Logic-aware navigation that prevents misclicks between UI tabs and strictly verifies Leaflet map markers post-CRUD operations.
* **Comprehensive Test Coverage:** Executes exactly 40 standardized test cases covering Unit, Integration, System, and Acceptance levels.
* **Resource Management Utility:** A built-in OS-level command trigger to safely terminate all orphaned Chrome processes and prevent memory leaks.

---

## ⚙️ Architecture & How It Works


**1. Data & State Initialization**
The `init_data` controller acts as a seed mechanism, wiping old logs and injecting the 40 predefined test case definitions into the database. A `SHARED_TEST_STATE` dictionary is utilized to dynamically pass contextual data between chained test steps (e.g., passing a dynamically generated username from a Registration case directly to a Login case).

**2. Hybrid Test Controller (`run_tests`)**
This central dispatcher dynamically routes test execution based on the selected mode. The **Backend Layer** instantiates Django `TestCase` classes directly to rapidly execute security and logic tests without browser overhead. The **Frontend Layer** triggers Selenium WebDriver to run the highly visual System and Acceptance cases.

**3. Advanced UI Automation & Injection**
Instead of native, invisible Selenium clicks, the framework utilizes an injected DOM element. It calculates exact layout bounds via `getBoundingClientRect()`, animates to the location, and uses `dispatchEvent` for absolute click accuracy on dynamic maps and complex layered UI elements.

**4. Security & Authentication Scenarios**
The unit testing suite actively attempts to inject malicious scripts (XSS) and SQL payloads to verify Django's ORM protection and auto-escaping mechanisms. It also validates boundary constraints (e.g., max lengths), Unicode support, and whitespace trimming logic.

**5. The "Panic Button"**
A robust `close_browsers` utility function uses raw OS-level commands (`pkill` on MacOS/Linux or `taskkill` on Windows) to forcefully terminate all hidden ChromeDriver processes during mass testing runs.

---

## 🛠 Tech Stack

* **Core Language:** Python
* **Automation:** Selenium WebDriver, webdriver-manager
* **Web Framework:** Django
* **Mapping:** Leaflet.js
* **Frontend Injectors:** Vanilla JavaScript, DOM Manipulation

---

## 🚀 Getting Started

Follow these steps to deploy and run the testing platform locally:

**1. Clone the repository:**
```bash
git clone [https://github.com/thanhnguyen221/BankAutoTest.git](https://github.com/thanhnguyen221/BankAutoTest.git)
   cd bank_project
python manage.py runserver or python3 manage.py runserver
http://127.0.0.1:8000/test-dashboard/init/
http://127.0.0.1:8000/


