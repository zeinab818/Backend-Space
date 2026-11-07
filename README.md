# 🌌 Āfāq – Backend

**Explore the Universe**

The backend API for Āfāq, a space exploration platform designed to help users discover planets, moons, space missions, astronomical discoveries, and more.

Built with Python and Flask, featuring JWT authentication and personalized exploration history.

## ✨ Features

- **User Authentication:** Register and login functionality.
- **JWT Authentication:** Access and refresh tokens.
- **User Management:** Retrieve authenticated user information.
- **Exploration Tracking:** Track viewed astronomical content.
- **Recent Explorations:** Retrieve the five most recently viewed items.
- **Exploration History:** View and manage personal exploration history.
- **Data Isolation:** Users can only access and manage their own exploration records.
- **Database Migrations:** Manage database schema changes with Flask-Migrate.

## 🛠️ Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Flask-Migrate
- Flask-CORS
- SQLite (Development)
- PostgreSQL (Production target)

## 📁 Project Structure

```text
Backend-Space/
│
├── main.py
├── auth.py
├── users.py
├── exploration.py
├── models.py
├── shemas.py
├── extensions.py
│
├── migrations/
│   └── versions/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/zeinab818/Backend-Space.git
cd Backend-Space
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows:**
```bash
venv\Scripts\activate
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

Add the required configuration variables:

```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
SQL
