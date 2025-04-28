# Rewardify Backend

A **FastAPI**-based backend powering **Rewardify**, an AI-assisted habit and challenge tracker.


**Frontend Repository:** https://github.com/dvolynov/Rewardify-App  
**Backend Repository:** https://github.com/dvolynov/Rewardify


[🚀TEST THE APP](https://rewardify-hack-9862f082da4d.herokuapp.com/)   
[📚GO TO API](https://rewardify-api-f36c675ae5dc.herokuapp.com/docs)


## 🚀 Features

- JWT **authentication** (login, register)
- **User management** (update profile, delete account)
- **Challenge system**:
  - AI-powered challenge generation (via OpenAI)
  - Track daily progress
  - Plan milestones
- **PostgreSQL** database (via SQLAlchemy ORM)
- Fully **async** and **CORS**-enabled
- Structured error handling and API validation
- Auto-generated interactive docs (`/docs`)


## 📂 Project Structure

```
.
├── ai/               # AI logic for challenges and rewards (uses OpenAI)
├── core/             # Core utilities (authentication, exception handling)
├── database/         # Database setup, models, and CRUD operations
├── endpoints/        # FastAPI route definitions (auth, challenges, user, etc.)
├── schemas/          # Pydantic models for request and response validation
├── tools/            # Helper tools and configuration files
├── .env              # Environment variables
├── .gitignore        # Git ignored files list
├── config.ini        # General app and AI configuration
├── deps.py           # Dependency injections for FastAPI
├── main.py           # FastAPI application entry point
├── Procfile          # Process file for deployment (Heroku, etc.)
├── README.md         # Project documentation
├── requirements.txt  # Python package dependencies
├── settings.py       # App settings and configuration management
```

## 🛠 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/rewardify-backend.git
cd rewardify-backend
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

Create a `.env` file at the project root:

```dotenv
# .env
ENV=development
DEBUG=true

DB_HOST=localhost
DB_PORT=5432
DB_USERNAME=your_db_user
DB_PASSWORD=your_db_password
DB_DATABASE=your_db_name
DB_SSLMODE=prefer

JWT_SECRET_KEY=your_jwt_secret_key
JWT_ALGORITHM=HS256
EXPIRES_DAYS=7

OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4
```

Also ensure your `config.ini` exists:

```ini
# config.ini
[GENERAL]
APP_NAME = Rewardify
SAVE_DIRECTORY = __cache__/users

[AI]
MODEL_PROVIDER = openai
DEFAULT_MODEL = gpt-4
TEMPERATURE = 0.7
MAX_TOKENS = 512
```

### 4. Start the server

```bash
uvicorn main:app --reload
```

The server will run at [http://127.0.0.1:8000](http://127.0.0.1:8000).


## 🧠 API Overview

Interactive documentation available:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)


## 📊 Tech Stack

- **Python 3.11+**
- **FastAPI**
- **SQLAlchemy**
- **PostgreSQL**
- **OpenAI API**
- **Pydantic**
- **JWT Authentication**


## ✨ Future Improvements

- Email verification and password reset
- Role-based authorization (admin, user)
- Challenge templates and reward system
- WebSocket real-time updates
- Docker support for production deployment


## 📄 License

This project is licensed under the MIT License.