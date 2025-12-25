## 🚗 Car Rental Management System (Streamlit + File Handling)

This project is a **Car Rental Management System** developed as a **Data Structures & Algorithms (DSA) semester project**. The application provides a modern **Streamlit-based frontend** while preserving the **core logic of a C++ file-handling system**, using plain text files for data storage instead of databases.

The system supports **Admin and User roles**, allowing admins to manage car inventory and users to rent and return cars. All records are stored and processed using **sequential file handling**, demonstrating fundamental DSA concepts in a real-world application.

---

### ✨ Key Features

#### 🔐 Authentication

* Admin Login & Signup
* User Login & Signup
* Role-based access control

#### 🚘 Car Management (Admin)

* Add and remove cars
* View all cars with status (Available / Rented)
* View available cars
* View waiting queue
* View returned cars

#### 👤 User Operations

* Rent a car
* Return a car
* View current bookings

#### 🎨 User Interface

* Modern, responsive UI built with **Streamlit**
* Custom full-screen background and glassmorphism design
* Clean dashboards for Admin and User panels

---

### 🧠 Technical Highlights

* **No database used** — all data is managed using text files
* Demonstrates **file handling, searching, conditionals, and structured records**
* Backend logic remains equivalent to a traditional **C++ CLI-based system**
* Streamlit is used **only for UI**, not for business logic
* Sample car data is auto-initialized without duplication

---

### 🛠️ Technologies Used

* **Python**
* **Streamlit**
* **Pandas**
* **HTML/CSS (for UI styling)**

---

### 📁 Data Storage (Text Files)

```
admins.txt     → Admin credentials  
users.txt      → User credentials  
cars.txt       → Car records and status  
waiting.txt    → Rental queue  
returned.txt   → Returned car history  
```

---

### 🎓 Academic Purpose

This project was built to demonstrate:

* File handling without databases
* Sequential search techniques
* Role-based system design
* Practical application of DSA concepts
* Conversion of a CLI-based system into a GUI application

---

### ▶️ How to Run

```bash
pip install streamlit pandas
streamlit run app.py
```
