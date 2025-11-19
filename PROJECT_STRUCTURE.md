# 📁 Project Structure

```
web platform/
│
├── 📂 api/                          # Backend API
│   └── index.py                     # Flask application (13.6 KB)
│                                    # - All API endpoints
│                                    # - Business logic
│                                    # - Data management
│
├── 📂 static/                       # Frontend static files
│   ├── style.css                    # CSS styling (8.5 KB)
│   │                                # - Responsive design
│   │                                # - Modern UI components
│   │                                # - Mobile-friendly
│   │
│   └── app.js                       # JavaScript logic (20.9 KB)
│                                    # - API communication
│                                    # - Form handling
│                                    # - Dynamic UI updates
│
├── 📄 index.html                    # Main HTML page (16.2 KB)
│                                    # - Customer interface
│                                    # - Admin interface
│                                    # - Responsive layout
│
├── 📄 vercel.json                   # Vercel configuration (445 B)
│                                    # - Build settings
│                                    # - Route configuration
│                                    # - Environment variables
│
├── 📄 requirements.txt              # Python dependencies (47 B)
│                                    # - Flask
│                                    # - flask-cors
│                                    # - Werkzeug
│
├── 📄 .gitignore                    # Git ignore rules (311 B)
│                                    # - Python cache
│                                    # - Data files
│                                    # - Environment variables
│
├── 📄 README.md                     # Full documentation (5.5 KB)
│                                    # - Features overview
│                                    # - Setup instructions
│                                    # - API documentation
│
├── 📄 DEPLOY_GUIDE.md              # Deployment guide (5.0 KB)
│                                    # - Step-by-step Vercel deployment
│                                    # - Multiple deployment methods
│                                    # - Troubleshooting tips
│
└── 📄 bus_booking_enhanced.py      # Original Tkinter app (43.5 KB)
                                     # - Legacy desktop version
                                     # - Reference only (not used in web version)
```

## File Details

### Core Application Files

#### `api/index.py` (Backend)
**Purpose**: Flask REST API handling all business logic

**Key Components**:
- `DataManager` class - Handles JSON file storage
- `ADMIN_CREDENTIALS` - Admin authentication
- API Routes:
  - Customer endpoints (booking, viewing, canceling)
  - Admin endpoints (dashboard, management)
  - Configuration endpoints

**Technologies**:
- Flask 3.0.0
- flask-cors 4.0.0
- Python hashlib for password encryption
- JSON for data persistence

---

#### `index.html` (Frontend Structure)
**Purpose**: Single-page application structure

**Sections**:
1. **Header** - Logo and admin status
2. **Navigation** - Customer/Admin tabs
3. **Customer Services**:
   - Book Ticket
   - View Ticket
   - Cancel Ticket
   - Check Routes & Fares
   - View Schedule
   - Bus Stops
4. **Admin Panel**:
   - Login page
   - Dashboard with statistics
   - Booking management
   - Route management
   - Report generation
5. **Footer** - Company information
6. **Modal** - For confirmations and receipts

---

#### `static/style.css` (Styling)
**Purpose**: Modern, responsive design

**Features**:
- CSS Variables for theming
- Flexbox and Grid layouts
- Mobile-first responsive design
- Card-based UI components
- Smooth transitions and animations
- Print-friendly styles
- Professional color scheme:
  - Primary: #2c3e50 (Dark blue)
  - Accent: #3498db (Sky blue)
  - Success: #28a745 (Green)
  - Danger: #dc3545 (Red)
  - Admin: #9b59b6 (Purple)

**Responsive Breakpoints**:
- Desktop: > 768px
- Mobile: ≤ 768px

---

#### `static/app.js` (Frontend Logic)
**Purpose**: Client-side functionality

**Key Functions**:
- `initializeApp()` - Load configuration
- `handleBooking()` - Process new bookings
- `viewTicket()` - Display ticket details
- `cancelTicket()` - Cancel bookings
- `handleAdminLogin()` - Admin authentication
- `loadAdminStats()` - Dashboard statistics
- `loadAllBookings()` - Admin booking list
- `generateReport()` - Create reports

**API Integration**:
- Fetch API for HTTP requests
- Error handling and user feedback
- Real-time fare calculation
- Form validation

---

### Configuration Files

#### `vercel.json`
**Purpose**: Vercel deployment configuration

**Configuration**:
```json
{
  "version": 2,
  "builds": [
    { "src": "api/index.py", "use": "@vercel/python" },
    { "src": "static/**", "use": "@vercel/static" }
  ],
  "routes": [
    { "src": "/static/(.*)", "dest": "/static/$1" },
    { "src": "/api/(.*)", "dest": "/api/index.py" },
    { "src": "/(.*)", "dest": "/api/index.py" }
  ]
}
```

---

#### `requirements.txt`
**Purpose**: Python dependencies for deployment

**Dependencies**:
- Flask==3.0.0 - Web framework
- flask-cors==4.0.0 - Cross-Origin Resource Sharing
- Werkzeug==3.0.1 - WSGI utility library

---

#### `.gitignore`
**Purpose**: Files to exclude from version control

**Excludes**:
- Python cache files (`__pycache__/`, `*.pyc`)
- Virtual environments (`venv/`, `env/`)
- Data files (`*.json` except `vercel.json`)
- IDE files (`.vscode/`, `.idea/`)
- Environment variables (`.env`)
- System files (`.DS_Store`, `Thumbs.db`)

---

### Documentation Files

#### `README.md`
Complete project documentation including:
- Feature overview
- Tech stack
- Local development setup
- Deployment instructions
- API documentation
- Configuration guide
- Security notes

#### `DEPLOY_GUIDE.md`
Step-by-step deployment guide with:
- Three deployment methods
- Troubleshooting section
- Post-deployment checklist
- Database upgrade path

#### `PROJECT_STRUCTURE.md` (This File)
Detailed breakdown of project structure and files

---

## Data Flow

### Customer Booking Flow
```
1. User fills booking form (index.html)
   ↓
2. JavaScript validates input (app.js)
   ↓
3. POST request to /api/bookings (app.js)
   ↓
4. Flask processes request (api/index.py)
   ↓
5. Data saved to JSON (api/index.py)
   ↓
6. Response sent back
   ↓
7. Receipt displayed (app.js)
```

### Admin Dashboard Flow
```
1. Admin logs in (index.html)
   ↓
2. POST to /api/admin/login (app.js)
   ↓
3. Credentials verified (api/index.py)
   ↓
4. Dashboard loads
   ↓
5. GET /api/admin/stats (app.js)
   ↓
6. Statistics calculated (api/index.py)
   ↓
7. Dashboard populated (app.js)
```

---

## Technologies Summary

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling (Flexbox, Grid, Variables)
- **JavaScript (ES6+)** - Logic (Fetch API, Async/Await)

### Backend
- **Python 3.9+** - Programming language
- **Flask** - Web framework
- **JSON** - Data storage

### Deployment
- **Vercel** - Serverless hosting
- **Git/GitHub** - Version control
- **Vercel CLI** - Deployment tool

---

## Routes (Zimbabwe Cities)

The system handles bus routes between:
1. **Bulawayo** - City Hall, Renkini Bus Terminus, NRZ Station
2. **Gweru** - Main Street, City Centre, Railway Station
3. **Kwekwe** - City Centre, Kwekwe Mall, Railway Station
4. **Kadoma** - City Centre, Kadoma Mall, Railway Station
5. **Chegutu** - City Centre, Chegutu Mall, Railway Station
6. **Norton** - Main Street, Town Centre, Post Office area
7. **Harare** - City Centre, Avondale, Mbare Musika

**Total Routes**: 42 (bidirectional)
**Seats per Bus**: 50

---

## Security Features

1. **Admin Authentication** - Password hashing (SHA-256)
2. **Input Validation** - Frontend and backend
3. **CORS Protection** - flask-cors configuration
4. **HTTPS** - Automatic with Vercel
5. **Data Sanitization** - SQL injection prevention (JSON storage)

---

## Future Enhancements

### Phase 1 - Database Integration
- [ ] PostgreSQL/MongoDB integration
- [ ] User authentication system
- [ ] Booking history

### Phase 2 - Payment Integration
- [ ] Payment gateway (Stripe/PayPal)
- [ ] Mobile money integration
- [ ] Receipt generation (PDF)

### Phase 3 - Advanced Features
- [ ] Email/SMS notifications
- [ ] Real-time seat availability
- [ ] Multi-language support
- [ ] Mobile app

---

## Development Timeline

**Original Version**: Desktop app with Tkinter (43.5 KB)
**Web Version**: Modern web application (Total: ~100 KB)

**Conversion Time**: ~2 hours
**Files Created**: 10
**Lines of Code**: ~1,500

---

## Maintenance

### Regular Tasks
1. Monitor Vercel logs for errors
2. Check booking data regularly
3. Update admin passwords periodically
4. Review and update routes/fares
5. Backup data files (if using JSON)

### Monitoring
- **Vercel Dashboard**: Traffic, errors, performance
- **Browser Console**: Frontend errors
- **API Logs**: Backend issues

---

**Last Updated**: November 18, 2025
**Version**: 1.0.0
**Status**: ✅ Ready for Deployment
