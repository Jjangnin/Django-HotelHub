# System Architecture and Data Model

## Overview
The application is a client-side Next.js app that runs entirely in the browser. User session state, user profiles, rooms, and bookings are all persisted in `localStorage` without a backend server. UI components interact with a lightweight data access layer in `lib/hotel-data.ts` and `components/auth-provider.tsx` to read/write browser storage and expose hooks for pages under `app/`.

## Architecture Diagram
```mermaid
flowchart LR
    subgraph Browser
        UI[Next.js pages & UI components]
        Auth[AuthProvider & hooks]
        Data[Hotel data helpers]
    end

    User((End User)) --> UI
    UI --> Auth
    UI --> Data
    Auth <--> LocalStorage[(localStorage: hotel_auth, hotel_users)]
    Data <--> LocalStorage2[(localStorage: hotel_rooms, hotel_bookings)]

    note over Auth,LocalStorage: Manages login state and user list
    note over Data,LocalStorage2: Initializes rooms, handles booking CRUD, updates room status
```

### Flow Highlights
- **Authentication**: UI calls `AuthProvider` hooks to read/write `hotel_auth` and `hotel_users` in `localStorage`, enabling login/signup and logout flows without server calls.
- **Rooms & Bookings**: UI components invoke hotel data helpers to initialize rooms, list/filter rooms, create bookings, and update booking status, all persisted in `localStorage` keys.
- **Navigation**: Protected pages guard access using authentication state from context; unauthenticated users are redirected to `/login`.

## Data Model Diagram
```mermaid
ergDiagram
    User {
        string id
        string name
        string email
        string role
        string? phone
        string createdAt
    }
    Room {
        string id
        string number
        string type
        string status
        number price
        number capacity
        string[] amenities
        number floor
    }
    Booking {
        string id
        string userId
        string roomId
        string roomNumber
        string checkIn
        string checkOut
        number guests
        number totalPrice
        string status
        string createdAt
        string? specialRequests
    }

    User ||--o{ Booking : "has bookings"
    Room ||--o{ Booking : "is reserved in"
```

### Data Storage Keys
- `hotel_auth`: currently authenticated user object.
- `hotel_users`: array of registered users.
- `hotel_rooms`: array of room records (initialized with defaults on first load).
- `hotel_bookings`: array of bookings; booking creation also updates the related room status.
```
