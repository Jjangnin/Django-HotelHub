System Architecture and Data Model
Overview

The application is a client-side Next.js app that runs entirely in the browser.
User session state, user profiles, rooms, and bookings are all persisted in localStorage without a backend server.

UI components interact with a lightweight data access layer in:

lib/hotel-data.ts

components/auth-provider.tsx

These modules read/write browser storage and expose hooks for pages under app/.

Architecture Diagram
flowchart LR
    subgraph Browser
        UI[Next.js pages & UI components]
        Auth[AuthProvider & hooks]
        Data[Hotel data helpers]
    end

    User((End User)) --> UI
    UI --> Auth
    UI --> Data
    Auth <--> LS1[(localStorage:<br/>hotel_auth, hotel_users)]
    Data <--> LS2[(localStorage:<br/>hotel_rooms, hotel_bookings)]

    NoteAuth[Manages login state<br/>and user list]
    NoteData[Initializes rooms,<br/>handles booking CRUD,<br/>updates room status]

    Auth --- NoteAuth
    Data --- NoteData

Flow Highlights

Authentication
AuthProvider hooks read/write hotel_auth and hotel_users, enabling login/signup/logout without a server.

Rooms & Bookings
Helpers in hotel-data.ts initialize rooms, filter rooms, create bookings, and update booking status, all persisted in localStorage.

Navigation
Protected pages use AuthContext for guarding access; unauthenticated users are redirected to /login.

Data Model Diagram
erDiagram
    User {
        string id
        string name
        string email
        string role
        string phone
        string createdAt
    }

    Room {
        string id
        string number
        string type
        string status
        int price
        int capacity
        string amenities
        int floor
    }

    Booking {
        string id
        string userId
        string roomId
        string roomNumber
        string checkIn
        string checkOut
        int guests
        int totalPrice
        string status
        string createdAt
        string specialRequests
    }

    User ||--o{ Booking : has_bookings
    Room ||--o{ Booking : is_reserved_in

Data Storage Keys
Key	Description
hotel_auth	Currently authenticated user
hotel_users	Array of registered users
hotel_rooms	Array of room records (initialized on first load)
hotel_bookings	Array of bookings; booking creation updates the related room status
