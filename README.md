# 🚑 AI-Driven Emergency Ambulance Routing System

<p align="center">
  <b>An AI-Assisted Smart Ambulance Management and Route Recommendation Platform</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Project-MCA%20Final%20Year-blue?style=for-the-badge" alt="MCA Project" />
  <img src="https://img.shields.io/badge/Status-Under%20Development-orange?style=for-the-badge" alt="Under Development" />
  <img src="https://img.shields.io/badge/Version-0.1-green?style=for-the-badge" alt="Version 0.1" />
</p>

---

## 📌 About the Project

**AI-Driven Emergency Ambulance Routing System** is a web-based academic project designed to assist emergency-response operators in managing ambulance requests and making informed decisions.

The proposed system aims to bring emergency information, ambulance availability, route recommendations, estimated arrival time (ETA), and hospital suitability into one centralized platform.

It is designed to use Artificial Intelligence, Machine Learning, routing algorithms, and geographical data to support faster and more organized emergency-response decisions.

### 🎯 Project Objectives

- Manage and monitor emergency requests through a centralized platform.
- Assess emergency severity using Machine Learning.
- Identify suitable available ambulances.
- Recommend efficient routes using map and routing data.
- Estimate ambulance arrival time (ETA).
- Recommend hospitals based on distance and required facilities.
- Support emergency status monitoring and route updates.
- Provide dashboards for emergency-response management.

> **Project Scope:** This is an academic decision-support prototype. It is not a replacement for professional medical judgment or an independently operating emergency service.

---

## 🛠️ Technology Stack

| Project Layer | Technologies |
|---|---|
| Frontend | React.js, React Router, CSS |
| Backend | Python, FastAPI |
| Database | MySQL 8.0 |
| ORM | SQLAlchemy 2 |
| Database Migrations | Alembic |
| API Testing | Postman, FastAPI Swagger UI |
| Machine Learning | Python, Scikit-learn |
| Data Processing | Pandas, NumPy |
| Maps | OpenStreetMap |
| Routing Engine | OSRM |
| Version Control | Git, GitHub |
| Development Tool | Visual Studio Code |

---

## 👥 Our Team

This project is developed collaboratively by a team of four MCA students.

| Member | Name | Registration Number | Assigned Role |
|---|---|---|---|
| Member 1 | Akancha Rani | 12500523 | Backend & Database |
| Member 2 | Prabhjot Kaur | 12503717 | AI & Machine Learning |
| Member 3 | Dilip Kumar (Sonu) | 12520416 | Frontend Development |
| Member 4 | Aryan Guleria | 12522004 | Maps & Algorithms |

### 👩‍💻 Individual Responsibilities

#### Member 1 – Backend and Database
**Technologies:** Python, FastAPI, MySQL, SQLAlchemy, Alembic

- Develop and maintain the FastAPI backend.
- Design and manage the MySQL database.
- Implement database connectivity and relationships.
- Develop emergency management APIs.
- Develop ambulance and hospital APIs.
- Implement authentication and authorization.
- Manage backend business logic and database operations.

#### Member 2 – AI and Machine Learning
**Technologies:** Python, Scikit-learn, Pandas, NumPy

- Prepare and preprocess datasets.
- Develop emergency severity classification.
- Develop ETA prediction models.
- Train and evaluate Machine Learning models.
- Analyse emergency and travel-related data.
- Integrate trained ML models with the backend.

#### Member 3 – Frontend Development
**Technologies:** React.js, React Router, CSS, JavaScript

- Develop the React-based web application.
- Design login and registration interfaces.
- Develop administrative and operator dashboards.
- Develop ambulance-related dashboard interfaces.
- Create forms, tables, charts, and reusable components.
- Integrate frontend pages with backend APIs.
- Maintain responsive and user-friendly interfaces.

#### Member 4 – Maps and Algorithms
**Technologies:** Python, OpenStreetMap, OSRM, Routing Algorithms

- Integrate OpenStreetMap for geographical visualization.
- Implement OSRM-based route calculation.
- Develop ambulance selection algorithms.
- Develop hospital recommendation algorithms.
- Analyse and optimize route recommendations.
- Implement dynamic rerouting logic.

**Team Collaboration:** All members participate in integration, testing, documentation, and final project demonstration.

---

## ⚙️ Current Development Status

### Version 0.1 – Implemented Features

| Feature | Current Status |
|---|---|
| Emergency request registration | ✅ Implemented |
| Save emergency requests in MySQL | ✅ Implemented |
| Emergency request listing | ✅ Implemented |
| Status and severity filters | ✅ Implemented |
| Emergency details page | ✅ Implemented |
| Backend status update API | ✅ Implemented |
| Emergency status history | ✅ Implemented |
| Dashboard statistics from database | ✅ Implemented |
| Ambulance listing | ✅ Implemented |
| Hospital listing | ✅ Implemented |
| API and database health check | ✅ Implemented |

### 🚧 Upcoming Modules

The following modules are planned for future development and integration:

- AI-based emergency severity classification.
- Machine Learning-based ETA prediction.
- Smart ambulance selection.
- Hospital recommendation engine.
- OpenStreetMap and OSRM integration.
- Route optimization.
- Live ambulance GPS tracking.
- Live traffic integration.
- Dynamic rerouting.
- Authentication and role-based access.
- Notifications and reports.

**Important:** Planned modules are not represented as completed features. Sample records and manually entered information are identified as demonstration data.

---

## 🔄 Proposed System Workflow

```text
Emergency Request
        |
        v
Emergency Information & Location
        |
        v
AI-Based Severity Assessment
        |
        v
Identify Available Ambulances
        |
        v
Route Calculation & ETA Prediction
        |
        v
Suitable Ambulance Recommendation
        |
        v
Hospital Recommendation
        |
        v
Emergency Dispatch
        |
        v
Emergency Status Monitoring
        |
        v
Route Update / Dynamic Rerouting
        |
        v
Emergency Completion
```

---

## 📂 Project Structure

```text
AI-Driven-Emergency-Ambulance-Routing/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database/
│   │   │   ├── connection.py
│   │   │   ├── models.py
│   │   │   ├── initialize_db.py
│   │   │   └── seed.py
│   │   ├── schemas/
│   │   ├── routers/
│   │   ├── services/
│   │   └── utils/
│   ├── alembic/
│   ├── tests/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── utils/
│   │   └── styles/
│   └── package.json
│
├── database/
│   ├── database.sql
│   └── schema_snapshot.sql
│
├── ml/
│   └── (Future ML modules)
│
├── docs/
│   └── BACKEND_DATABASE_EXPLAINED.md
│
├── .env.example
├── .gitignore
├── README.md
└── TEAM_SETUP.md
```

---

## 🔌 Backend API Overview

The backend provides REST APIs for communication between the frontend and database.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Check API and database connection |
| POST | `/api/emergencies` | Create an emergency request |
| GET | `/api/emergencies` | Retrieve emergency requests |
| GET | `/api/emergencies/{id}` | Retrieve emergency details |
| PATCH | `/api/emergencies/{id}/status` | Update emergency status |
| GET | `/api/ambulances` | Retrieve ambulance records |
| GET | `/api/hospitals` | Retrieve hospital records |
| GET | `/api/dashboard/summary` | Retrieve dashboard statistics |

### API Documentation

FastAPI provides interactive API documentation through Swagger UI.

After starting the backend, visit:

`http://localhost:8000/docs`

---

## 💻 Installation and Setup

### Prerequisites

Install the following tools before running the project:

- Python 3.11 or later
- Node.js and npm
- MySQL Server 8.0
- Git
- Visual Studio Code

### 1. Clone the Repository

```bash
git clone https://github.com/AkanchaRani/AI-Driven-Emergency-Ambulance-Routing.git
```

```bash
cd AI-Driven-Emergency-Ambulance-Routing
```

### 2. Configure Environment Variables

Create a local `.env` file from the example:

```powershell
Copy-Item .env.example .env
```

Update the database credentials in `.env`:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=ambulance_routing_db

CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

**Security Note:** Never upload your actual `.env` file, database password, or private credentials to GitHub.

### 3. Backend Setup

Open a terminal in the project root:

```powershell
cd backend
```

Create a virtual environment:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Initialize the database:

```powershell
python -m app.database.initialize_db
```

Start the backend:

```powershell
uvicorn app.main:app --reload
```

Backend URL:

`http://127.0.0.1:8000`

### 4. Frontend Setup

Open another terminal:

```powershell
cd frontend
```

Install dependencies:

```powershell
npm install
```

Start the React application:

```powershell
npm run dev
```

Frontend URL:

`http://localhost:5173`

---

## 🧪 Testing and Verification

The project uses the following tools and methods for testing:

- FastAPI Swagger UI for API testing.
- Postman for REST API verification.
- Pytest for automated backend tests.
- SQLite temporary database for isolated automated tests.
- MySQL for application database operations.
- Frontend and backend integration checks.

Testing is performed incrementally as new modules are developed.

---

## 🔐 Data and Security Practices

- Database credentials are stored in environment variables.
- `.env` is excluded through `.gitignore`.
- `.env.example` contains placeholder configuration.
- Database operations are handled through the backend.
- Emergency status changes are recorded in status history.
- Sample data is distinguished from real operational information.

---

## 🚀 Future Scope

The project can be extended with:

1. Advanced Machine Learning models for severity assessment.
2. Improved ETA prediction using traffic and road-related features.
3. Intelligent ambulance assignment.
4. Map-based route optimization.
5. Hospital recommendation based on medical facilities.
6. Live GPS tracking and traffic-aware route updates.
7. Secure role-based access for different users.
8. Notifications and emergency response analytics.
9. Centralized cloud deployment for multi-user access.

---

## 🎓 Academic Information

| Detail | Information |
|---|---|
| Degree | Master of Computer Applications (MCA) |
| Project Title | AI-Driven Emergency Ambulance Routing |
| Institution | Lovely Professional University |
| Location | Phagwara, Punjab |
| Project Type | Academic Web-Based Application |
| Project Domain | Artificial Intelligence / Machine Learning |

---

## 📚 References and Documentation

- [Python Documentation](https://docs.python.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [OpenStreetMap](https://www.openstreetmap.org/)
- [OSRM Documentation](https://project-osrm.org/)
- [GitHub Documentation](https://docs.github.com/)

---

<p align="center">
  <b>🚑 AI-Driven Emergency Ambulance Routing System</b>
  <br/>
  <i>Building smarter decision-support solutions for emergency response.</i>
  <br/><br/>
  Developed with teamwork, learning, and innovation by the MCA project team.
</p>