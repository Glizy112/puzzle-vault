# Project: The Puzzle Vault
### *Industrial Training Lab: Web Security & State Management*

Welcome to **The Puzzle Vault**, a custom-built laboratory designed for the seekers. This lab focuses on real-world vulnerabilities in modern web applications such as **JWT (JSON Web Tokens)**, **Cookie Security**, and **API Authorization**.

## Project Structure
This repository is split into two distinct environments to demonstrate the "Break" and "Fix" cycle of security engineering:

* **/vulnerable_version**: The "Broken" application. Contains 4+ critical vulnerabilities including IDOR, JWT algorithm exploits, and insecure state management.
* **/fixed_version**: The "Hardened" application. Demonstrates industry-standard defenses using Flask-Talisman and secure coding practices.
* **database.json**: A shared db containing some info (Flags).
* **postman_collection.json**: A starter suite for API testing and manipulation.

## Lab Objectives (The Hunt for 3 Keys aka CTF - Capture the Flag)
Your mission is to perform a security hunt & audit on the vulnerable version (Port 5000) and capture three distinct flags:

1.  **The Inspector Key:** Found by decoding the hidden JWT payload.
2.  **The Ghost Key:** Found via **Insecure Direct Object Reference (IDOR)** on the API.
3.  **The Master Key:** Found by performing a **JWT "None" Algorithm exploit** and hijacking the Admin session in your browser.

*Bonus Flag: Find the hidden **Reconnaissance Header** to leak the server info.*

## Setup Instructions

### 1. Prerequisites
- Python 3.x
- Postman (Desktop version recommended)
- Burp Suite Community Edition

### 2. Installation
Clone the repository and install the required dependencies:
```bash
git clone [https://github.com/Glizy112/puzzle-vault.git](https://github.com/Glizy112/puzzle-vault.git)
cd puzzle-vault
pip install flask PyJWT flask-talisman
