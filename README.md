# 🚌 Chikukwa Bus Booking System

A modern, web-based bus booking system for managing bus reservations across Zimbabwe. Built with Flask backend and vanilla JavaScript frontend, optimized for Vercel deployment.

## Features

### Customer Features
- 🎫 **Book Tickets** - Easy online ticket booking with seat selection
- 🔍 **View Tickets** - Check booking details using Ticket ID
- ❌ **Cancel Tickets** - Cancel bookings when needed
- 💰 **Check Routes & Fares** - View available routes and pricing
- ⏰ **View Schedules** - Check bus departure times
- 📍 **Bus Stops** - Find pickup and drop-off locations

### Admin Features
- 🔐 **Secure Login** - Admin authentication system
- 📊 **Dashboard** - View booking statistics and revenue
- 📋 **Manage Bookings** - View, search, and cancel bookings
- 🛣️ **Manage Routes** - Update routes and pricing
- 📈 **Generate Reports** - Create booking statistics reports

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Deployment**: Vercel Serverless Functions
- **Storage**: JSON file storage (serverless-compatible)

## Project Structure

```
web platform/
├── api/
│   └── index.py          # Flask API backend
├── static/
│   ├── style.css         # Styling
│   └── app.js           # Frontend logic
├── index.html           # Main HTML page
├── vercel.json          # Vercel configuration
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # Documentation
```

## Local Development

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Setup

1. **Navigate to project directory**
   ```bash
   cd "D:\My Programs\Bus booking system\web platform"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the development server**
   ```bash
   python api/index.py
   ```

4. **Open in browser**
   ```
   http://localhost:5000
   ```

## Deployment to Vercel

### Option 1: Using Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   vercel
   ```

4. **Deploy to production**
   ```bash
   vercel --prod
   ```

### Option 2: Using Vercel Dashboard

1. **Push code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Bus booking system"
   git branch -M main
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Import to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Vercel will auto-detect the configuration from `vercel.json`
   - Click "Deploy"

3. **Your app will be live!**
   - Access at: `https://your-project-name.vercel.app`

## Configuration

### Admin Credentials
Default admin accounts (change in `api/index.py`):
- **Username**: admin | **Password**: admin123
- **Username**: manager | **Password**: manager123

### Routes and Pricing
Routes and schedules are defined in `api/index.py` in the `get_default_config()` function. Modify there to:
- Add new routes
- Update fares
- Change schedules
- Modify bus stops

### Company Information
Update company details in the config:
- Company name
- Contact phone
- Contact email
- Total seats per bus

## API Endpoints

### Public Endpoints
- `GET /api/config` - Get system configuration
- `POST /api/route-info` - Get route information
- `POST /api/bookings` - Create a booking
- `GET /api/bookings/:id` - Get booking details
- `DELETE /api/bookings/:id` - Cancel a booking
- `GET /api/schedules` - Get all schedules
- `GET /api/stops/:city` - Get bus stops for a city

### Admin Endpoints
- `POST /api/admin/login` - Admin login
- `GET /api/admin/bookings` - Get all bookings
- `GET /api/admin/stats` - Get statistics
- `GET /api/admin/routes` - Get all routes
- `PUT /api/admin/routes` - Update route fare

## Environment Variables

For production deployment, you can set:
- `FLASK_ENV=production` (already in vercel.json)

## Data Persistence

The application uses JSON files stored in `/tmp` directory on Vercel (serverless environment). 

**Note**: Data in `/tmp` is ephemeral and may be cleared. For production use, consider upgrading to:
- PostgreSQL (via Vercel Postgres)
- MongoDB Atlas
- Supabase
- Any other cloud database

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers

## Responsive Design

The application is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones

## Security Notes

1. **Change default admin passwords** before production deployment
2. **Use HTTPS** (Vercel provides this automatically)
3. **Consider adding rate limiting** for API endpoints
4. **Implement proper session management** for admin authentication
5. **Add input validation** on both frontend and backend

## Future Enhancements

- [ ] Payment gateway integration
- [ ] Email notifications
- [ ] SMS confirmations
- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] User accounts and history
- [ ] Real-time seat availability
- [ ] PDF ticket generation
- [ ] Multi-language support
- [ ] Mobile app (React Native/Flutter)

## Support

For issues or questions:
- **Email**: support@chikukwabus.com
- **Phone**: +263777189947

## License

© 2025 Chikukwa Bus Services. All rights reserved.

---

**Made with ❤️ for Zimbabwe 🇿🇼**
