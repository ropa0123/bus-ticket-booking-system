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
└── # 🚌 Chikukwa Bus Booking System

A modern, full-stack web application for bus ticket booking with admin panel and PostgreSQL database integration.

## ✨ Features

### Customer Features
- 🎫 Book bus tickets online
- 🔍 View ticket details
- ❌ Cancel bookings
- 💰 Check routes and fares
- 📅 View bus schedules
- 📍 Find bus stop locations

### Admin Features
- 📊 Dashboard with statistics
- 👥 View all bookings
- 🔧 Manage routes and pricing
- 📈 Generate reports
- 🔐 Secure authentication

### Technical Features
- 🗄️ **PostgreSQL database** for persistent storage
- 🚀 **Vercel-ready** deployment
- 📱 **Responsive design** - works on all devices
- 🔄 **Automatic fallback** to in-memory storage if database unavailable
- 🎨 **Modern UI** with clean interface

## 🏗️ Architecture

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python Flask REST API
- **Database**: PostgreSQL
- **Deployment**: Vercel (Serverless Functions)

## 📁 Project Structure

```
web platform/
├── api/
│   └── index.py              # Flask API with all endpoints
├── static/
│   ├── app.js                # Frontend JavaScript
│   └── style.css             # Styling
├── index.html                # Main HTML page
├── db_manager.py             # Database operations
├── database.sql              # Database schema
├── init_db.py                # Database initialization script
├── requirements.txt          # Python dependencies
├── vercel.json              # Vercel configuration
├── .env.example             # Environment variables template
├── DEPLOYMENT_GUIDE.md      # Complete deployment instructions
└── DATABASE_SETUP.md        # Database setup guide
```

## 🚀 Quick Start

### 1. Set Up Database

Choose one:
- **Vercel Postgres** (recommended for Vercel deployment)
- **Neon.tech** (free PostgreSQL)
- **Supabase** (free with 500MB)

Get your connection string and create `.env` file:

```env
POSTGRES_URL="postgresql://user:pass@host:5432/db?sslmode=require"
```

### 2. Initialize Database

```bash
pip install -r requirements.txt
python init_db.py
```

### 3. Deploy to Vercel

```bash
npm install -g vercel
vercel login
vercel
vercel env add POSTGRES_URL
vercel --prod
```

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

## 💻 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable
export POSTGRES_URL="your_connection_string"

# Run the application
python api/index.py
```

Open http://localhost:5000

## 🔐 Admin Credentials

**Default credentials** (change these in production!):
- Username: `admin` / Password: `admin123`
- Username: `manager` / Password: `manager123`

## 📖 API Endpoints

### Customer Endpoints
- `GET /api/config` - Get system configuration
- `POST /api/bookings` - Create new booking
- `GET /api/bookings/<id>` - Get booking by ID
- `DELETE /api/bookings/<id>` - Cancel booking
- `POST /api/route-info` - Get route information
- `GET /api/schedules` - Get all schedules
- `GET /api/stops/<city>` - Get bus stops for city

### Admin Endpoints
- `POST /api/admin/login` - Admin login
- `GET /api/admin/bookings` - Get all bookings
- `GET /api/admin/stats` - Get statistics
- `GET /api/admin/routes` - Get all routes
- `PUT /api/admin/routes` - Update route fare

## 🗄️ Database Schema

- **bookings** - All ticket bookings
- **routes** - Bus routes with fares and schedules
- **bus_stops** - Bus stop locations by city
- **system_config** - System configuration

## 🛠️ Technologies Used

- **Backend**: Flask, psycopg2
- **Frontend**: Vanilla JavaScript, CSS3
- **Database**: PostgreSQL
- **Deployment**: Vercel
- **Version Control**: Git

## 📚 Documentation

- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Complete deployment instructions
- [DATABASE_SETUP.md](DATABASE_SETUP.md) - Database setup and management
- [.env.example](.env.example) - Environment variable template

## 🐛 Troubleshooting

### Bookings Not Persisting?
1. Check `POSTGRES_URL` is set in Vercel environment variables
2. Run `vercel logs` to check for database errors
3. Verify database connection string format

### Database Connection Failed?
1. Ensure connection string includes `?sslmode=require`
2. Test connection locally with `.env` file
3. Check database is running and accessible

### Deployment Failed?
1. Verify all files are committed
2. Check `requirements.txt` has all dependencies
3. Ensure `vercel.json` is properly configured

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is open source and available for educational purposes.

## 👥 Contact

- Company: Chikukwa Bus Services
- Phone: +263777189947
- Email: support@chikukwabus.com

## 🎉 Acknowledgments

Built with ❤️ for comfortable and safe travel across Zimbabwe.

---

**Ready to deploy?** Follow the [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)!           # Documentation
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
