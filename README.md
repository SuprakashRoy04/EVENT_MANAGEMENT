Event Membership Management System

A Flask-based web application for managing event memberships and transactions with role-based authentication and session management.



## Features

## Authentication
- Admin and User login
- Session-based authentication
- Role-based access control

## Admin Capabilities
- Add Membership
- Update Membership (Extend / Cancel)
- View Membership Report
- Add Transactions
- View Transaction Report

## User Capabilities
- View Membership Report
- Add Transactions
- View Transaction Report

## Membership Module
- Auto-generated Membership ID
- Duration options (6 Months / 1 Year / 2 Years)
- Automatic expiry date calculation
- Status tracking (Active / Cancelled)

## Transactions Module
- Add event transactions
- Store membership number reference
- View all transaction records


##  Tech Stack

- **Backend:** Python (Flask)
- **Database:** SQLite
- **Frontend:** HTML + CSS
- **Authentication:** Flask Sessions



##  Project Structure
EVENT_APP/
│
├── app.py
├── database.db
├── templates/
│ ├── login.html
│ ├── dashboard.html
│ ├── add_membership.html
│ ├── update_membership.html
│ ├── report.html
│ ├── transactions.html
  └── transaction_report.html

  




