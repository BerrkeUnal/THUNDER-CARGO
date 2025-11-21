# ⚡️ Thunder Cargo - Logistics Management System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **A comprehensive logistics platform bridging the gap between customers and service providers through a secure, role-based architecture.**

---

## 📖 Table of Contents
* [About the Project](#-about-the-project)
* [System Architecture & Roles](#-system-architecture--roles)
* [Tech Stack](#-tech-stack)
* [Database Structure](#-database-structure)
* [Getting Started](#-getting-started)
* [Screenshots](#-screenshots)
* [Contact](#-contact)

---

## 🚀 About the Project

**Thunder Cargo** is a Python-based application powered by a robust MySQL database. It is designed to simulate a real-world cargo management environment where different users have distinct interfaces and permission sets.

The system separates the workflow into two main environments: the **Customer Portal** for end-users and the **Management Dashboard** for the authorized company staff.

---

## 🔐 System Architecture & Roles

The application features a strict **Role-Based Access Control (RBAC)** system with three distinct tiers:

### 1. 👤 Guest (Public Access)
* **Landing Page:** General information about Thunder Cargo services.
* **Public Tracking:** Ability to track a shipment status using only the tracking ID (no login required).
* **Authentication:** Access to Login and Registration pages.

### 2. 📦 User / Customer (Client Portal)
Once logged in, customers gain access to a personalized dashboard:
* **Create Order:** A dedicated form to calculate shipping costs and place new cargo requests.
* **Order History:** A list view of all past and active shipments associated with their account.
* **Profile Management:** Ability to update contact information and address details.
* **Status Notifications:** View real-time updates on their specific packages.

### 3. 🛠 Admin / Authorized Company (Management Dashboard)
A secure, high-privilege area for company staff to manage operations:
* **Global Order Management:** View, edit, and delete orders from all users.
* **Status Updates:** Capability to move cargo status from 'Pending' to 'In Transit' or 'Delivered'.
* **User Management:** View registered users and manage account restrictions.
* **Analytics:** (Optional) View basic stats like total revenue or total active shipments.

---

## 🛠 Tech Stack

* **Programming Language:** Python (Core Logic & Interface)
* **Database:** MySQL (Relational Data Management)
* **Database Connector:** `mysql-connector-python`
* **GUI / Interface:** Streamlit - Python Library

---

## 🗄 Database Structure

The project relies on a relational MySQL database. Key tables include:

* `users` (Stores ID, username, password_hash, role)
* `orders` (Stores tracking_id, sender_id, receiver_details, weight, status)
* `shipment_logs` (Timestamps for status changes)

---

## 🏁 Getting Started

Follow these steps to set up the project on your local machine.

### Prerequisites
* Python 3.x installed.
* MySQL Server installed and running.

### Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/yourusername/thunder-cargo.git](https://github.com/yourusername/thunder-cargo.git)
    cd thunder-cargo
    ```

2.  **Install Python Dependencies**
    ```bash
    pip install mysql-connector-python
    # Add other libraries if used, e.g., pip install customtkinter
    ```

3.  **Database Setup**
    * Open your MySQL Workbench or Command Line.
    * Create a new database named `thunder_cargo_db`.
    * Import the provided SQL file:
    ```bash
    mysql -u root -p thunder_cargo_db < database_schema.sql
    ```

4.  **Configure Connection**
    * Open the `db_config.py` (or relevant file) and update your MySQL credentials:
    ```python
    host="localhost",
    user="your_username",
    password="your_password",
    database="thunder_cargo_db"
    ```

5.  **Run the Application**
    ```bash
    python main.py
    ```
---

## 📞 Contact

**Project Link:** [https://github.com/username/thunder-cargo](https://github.com/BerrkeUnal/thunder-cargo)

---
