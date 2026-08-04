# Flight Booking System (Fullstack Monorepo) ✈️🎫

A modern, feature-rich fullstack Flight Booking System inspired by platforms like Traveloka. This application provides a seamless flight searching, ticket booking, and administrative management experience.

---

## 📁 Project Structure

This monorepo consists of a FastAPI backend and a Vue 3 frontend:

```
flight-booking-system/
├── frontend/             # Vue 3 Frontend
│   ├── src/
│   │   ├── views/        # Page-level views (Home, Flights, Booking, Admin, Profile, etc.)
│   │   ├── components/   # Reusable UI components
│   │   ├── router/       # Routing configuration
│   │   └── App.vue       # Main Application entry point
│   ├── package.json
│   └── vite.config.js
│
├── backend/              # FastAPI Backend
│   ├── app/
│   │   ├── api/v1/       # REST API endpoints (flights, bookings, auth, analytics, etc.)
│   │   ├── core/         # Config, Security, and Database setup
│   │   ├── models/       # SQLAlchemy models
│   │   └── main.py       # Application entry point
│   ├── requirements.txt
│   └── .env              # Backend environment variables
│
└── start.bat             # One-click Windows starter script
```

---

## 🌟 Key Features

### 👤 User Features
* **Interactive Flight Search:** Search for one-way or round-trip flights with custom origins, destinations, and dates.
* **Smart Filtering & Sorting:** Refine flights based on price range, airlines, transit options, and flight duration.
* **Interactive Seat Selection:** View available seats and select your preferred seats dynamically during the booking process.
* **E-Tickets & Booking History:** Retrieve, review, and view details of your booked e-tickets.
* **User Accounts:** Sign in and Register safely to keep track of bookings.

### 👑 Admin Features
* **Flight Management Console:** Add, edit, or remove flights, and update seat allocations or schedules.
* **Analytics Dashboard:** Graphical charts depicting regional bookings, passenger demographics, and booking trends over time.

---

## 🛠️ Technology Stack

* **Frontend:** Vue 3 (Composition API), Bootstrap 5, Vite, Pinia (State Management), Chart.js
* **Backend:** FastAPI (Python 3.10+), SQLAlchemy (ORM), Uvicorn (ASGI server)
* **Database & Auth:** PostgreSQL (hosted via Supabase), Supabase Client Integration

---

## 🚀 How to Run ?

Choose one of the methods below to run the application.

### Method 1: Using the Batch Launcher (Windows - Recommended)
If you are on Windows, you can start both the Frontend and Backend services in parallel with a single double-click:
1. Open the project root directory.
2. Double-click the **`start.bat`** file.
3. This opens two terminal windows running the backend server and frontend development server.

---

### Method 2: Manual Execution

#### 1. Start the Backend
1. Open a new terminal and navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Create and activate a Python virtual environment:
   ```bash
   # Windows
   python -m venv .venv
   .\.venv\Scripts\activate

   # macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   * The API docs will be accessible at: http://127.0.0.1:8000/docs
   * The server runs at: http://127.0.0.1:8000

#### 2. Start the Frontend
1. Open another terminal and navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install the node packages:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
   * Access the website at: http://localhost:5173 (or the URL displayed in the console).
