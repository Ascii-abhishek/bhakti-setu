# Bhakti Setu# 🎈 Blank app template



A modern web application for storing and accessing mythological stories, mantras, and aartis in Hindi and English.A simple Streamlit app template for you to modify!



## Features[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)



- 🎨 **Beautiful UI**: Bootstrap-based responsive design with light/dark theme support### How to run it on your own machine

- 🔍 **Smart Search**: Natural language search for stories, mantras, and aartis

- 🎵 **Audio Support**: Listen to mantras and aartis with built-in media player1. Install the requirements

- 🌐 **Bilingual Content**: Support for Hindi and English languages

- 🔐 **Admin Panel**: Secure admin interface for content management   ```

- 📱 **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices   $ pip install -r requirements.txt

   ```

## Tech Stack

2. Run the app

- **Backend**: FastAPI (Python)

- **Database**: PostgreSQL with SQLAlchemy ORM   ```

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla), Bootstrap 5   $ streamlit run streamlit_app.py

- **Authentication**: JWT tokens with passlib for password hashing   ```

- **Configuration**: Pydantic Settings for environment variables

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- PostgreSQL database (Neon, AWS RDS, or local)
- pip package manager

### Installation

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables** in `.env`:
   ```env
   DB_NAME=your_database_name
   DB_USER=your_database_user
   DB_PASSWORD=your_database_password
   DB_HOST=your_database_host
   DB_PORT=5432
   
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=your_secure_password
   
   SECRET_KEY=your_secret_key_here
   ```

3. **Initialize the database**
   ```bash
   python3 init_db.py
   ```

4. **Run the application**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the application**
   - Home Page: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin
   - API Docs: http://localhost:8000/docs

## License

MIT License
