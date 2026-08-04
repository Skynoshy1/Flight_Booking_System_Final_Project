# Traveloka Flight Booking System - Final Report Outline

This document presents a comprehensive outline for the final report of the project, detailing all system architectures, database integrations, advanced algorithms, and features implemented across the monorepo.

---

## 📖 Proposed Final Report Outline

### 1. Executive Summary
*   **Project Context**: Transition from a legacy news/weather application to a high-fidelity, enterprise-grade flight booking monorepo.
*   **Core Objective**: Designing a scalable, responsive, and real-time flight booking application replicating the Traveloka design system.
*   **Key Engineering Achievements**: Graph-based flight searches, socket-like broadcast concurrency control, automated database cleanup, and interactive 2D seating models.

### 2. Monorepo & System Architecture
*   **Frontend Architecture**: Vue 3 (Composition API), Vite build system, SCSS design tokens (customizing Bootstrap 5), and Axios API client wrapper.
*   **Backend Architecture**: FastAPI (Asynchronous Python), Pydantic validation schemas, SQLAlchemy database models, and dynamic background tasks.
*   **Database Infrastructure**: Supabase (PostgreSQL) hosting relational models with primary/foreign key integrity constraints.
*   **Security & JWT Token Authentication**: 
    *   Supabase auth client integration.
    *   Route-level navigation guards on the frontend.
    *   Token validation middleware protecting backend endpoints.

### 3. Flight Network Graph Building & Search Routing
*   **Graph Network Representation**:
    *   **Nodes**: Airport hubs represented by country/city data (e.g., `SGN`, `HAN`, `DAD`, `CXR`, `BMV`).
    *   **Edges**: Flight segments representing directed edges connecting airports, detailed with cost parameters, arrival/departure schedules, and airline classes.
*   **Dynamic Data Seeding & Cleanup**:
    *   Backend crawling daemon (`crawl_flights.py`) mimicking real flight schedules.
    *   Cron schedule executions generating flexible flights over rolling windows.

### 4. Real-Time Seat Synchronization & Concurrency Control
*   **The Seat Double-Booking Problem**: Handling the race condition where multiple users attempt to select and purchase the exact same seat simultaneously.
*   **Real-time Collaboration Layer**:
    *   Supabase Realtime channels with custom broadcast topics (`flight-room-{flight_id}`).
    *   **Presence Mechanism**: Instantly track users in the room. If a user closes the browser tab or disconnects, their locked seats are automatically cleared.
*   **Concurrency Resolution**:
    *   First-to-click locks the seat locally for other sessions, updating the interactive 2D seating chart UI.
    *   Backend transactions with verification steps to check database records for seat conflicts before finalizing payment.

### 5. Ticket Lifecycle, Expiration & Automatic Archiving
*   **Flight Expiration Cleaning**:
    *   Periodic sweep queries (`clean_old_flights`) targeting unbooked flights scheduled in the past, preventing table bloat.
*   **Real-Time Ticket Validation**:
    *   Checking pending bookings; transitioning expired checkouts to cancellation lists or moving finalized flights to user history once flights depart.

### 6. Interactive User Experience & Business Logic
*   **Interactive 2D Seating Chart**:
    *   Graphical plane grid mapping seat classes (First, Business, Economy) with relative surcharge calculations.
*   **IP-Based Geolocation Detection**:
    *   Determining closest departure hubs dynamically based on mock IP detection.
*   **Loyalty Points & Tier-Based Pricing**:
    *   Applying dynamic discounts (Bronze, Silver, Gold tiers) calculated from profile points in real-time.
*   **Social Interactions**:
    *   Facebook-style comments and user likes linked dynamically to bookings and airlines.
*   **Flight Review & Rating System**:
    *   Post-booking user feedback collection (stars and text comments) synchronized to the reviews database.

### 7. Multi-Currency Exchange Rates System
*   **Third-party Rate Integration**:
    *   Asynchronous calls via `httpx` to sync rates dynamically against external currency providers.
    *   Local caching of rates (USD, VND, EUR, SGD, THB, MYR) to ensure high-performance API response times with graceful fallback conversion logic.

### 8. Enterprise Admin & Analytics Dashboard
*   **Dashboard KPIs**: Tracking overall revenue, flight occupancy, active bookings, and average tickets.
*   **CRUD Data Controls**: Adding, updating, and removing flights.
*   **Hub Analytics**: Density mapping based on geographic flight distributions.

### 9. Verification, Testing & Conclusion
*   **Automated Verification**: Pydantic schema validation, route checking, and API endpoints testing.
*   **Manual Testing Playbook**: Concurrency simulation via multiple active browser tabs.
*   **Conclusion**: Summary of the engineering achievements.
