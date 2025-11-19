from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import uuid
import datetime
import os
import hashlib
import sys
from typing import Dict, List, Optional

# Add parent directory to path to import db_manager
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from db_manager import DatabaseManager
    USE_DATABASE = True
except ImportError:
    USE_DATABASE = False
    print("Warning: Database module not available, using fallback storage")

app = Flask(__name__, static_folder='../static', static_url_path='/static')
CORS(app)

ADMIN_CREDENTIALS = {
    "admin": hashlib.sha256("admin123".encode()).hexdigest(),
    "manager": hashlib.sha256("manager123".encode()).hexdigest()
}

# Initialize database connection if available
if USE_DATABASE:
    try:
        DatabaseManager.initialize_pool()
    except Exception as e:
        print(f"Database initialization failed: {e}")
        USE_DATABASE = False

# Fallback to in-memory storage if database is not available
_bookings_cache = None
_config_cache = None

class DataManager:
    """Data manager that uses database when available, falls back to in-memory storage"""
    
    @staticmethod
    def load_bookings() -> Dict:
        """Load all bookings - returns dict for backwards compatibility"""
        if USE_DATABASE:
            try:
                bookings_list = DatabaseManager.get_all_bookings()
                # Convert list to dict with ticket_id as key
                return {booking['ticket_id']: {
                    'ticket_id': booking['ticket_id'],
                    'name': booking['name'],
                    'age': booking['age'],
                    'phone': booking['phone'],
                    'email': booking['email'],
                    'departure': booking['departure'],
                    'destination': booking['destination'],
                    'date': booking['date'].isoformat() if hasattr(booking['date'], 'isoformat') else str(booking['date']),
                    'time': booking['time'],
                    'seat': booking['seat'],
                    'fare': float(booking['fare']),
                    'status': booking['status'],
                    'booked_at': booking['booked_at'].isoformat() if hasattr(booking['booked_at'], 'isoformat') else str(booking['booked_at'])
                } for booking in bookings_list}
            except Exception as e:
                print(f"Database error: {e}")
                return DataManager._load_from_memory()
        return DataManager._load_from_memory()
    
    @staticmethod
    def _load_from_memory() -> Dict:
        global _bookings_cache
        if _bookings_cache is None:
            _bookings_cache = {}
        return _bookings_cache
    
    @staticmethod
    def save_bookings(bookings: Dict):
        """Save bookings - maintained for backwards compatibility"""
        global _bookings_cache
        _bookings_cache = bookings
    
    @staticmethod
    def load_config() -> Dict:
        """Load configuration"""
        if USE_DATABASE:
            try:
                # Get routes
                routes_list = DatabaseManager.get_all_routes()
                bus_routes = {route['route_name']: float(route['fare']) for route in routes_list}
                bus_schedules = {route['route_name']: route['schedule'] for route in routes_list}
                
                # Get bus stops
                stops_list = DatabaseManager.get_all_bus_stops()
                bus_stops = {stop['city']: stop['stops'] for stop in stops_list}
                
                # Get system config
                config = DatabaseManager.get_all_config()
                
                return {
                    'bus_routes': bus_routes,
                    'bus_schedules': bus_schedules,
                    'bus_stops': bus_stops,
                    'total_seats': int(config.get('total_seats', 50)),
                    'company_name': config.get('company_name', 'Chikukwa Bus Services'),
                    'contact_phone': config.get('contact_phone', '+263777189947'),
                    'contact_email': config.get('contact_email', 'support@chikukwabus.com')
                }
            except Exception as e:
                print(f"Database error: {e}")
                return DataManager._load_config_from_memory()
        return DataManager._load_config_from_memory()
    
    @staticmethod
    def _load_config_from_memory() -> Dict:
        global _config_cache
        if _config_cache is None:
            _config_cache = DataManager.get_default_config()
        return _config_cache
    
    @staticmethod
    def save_config(config: Dict):
        """Save configuration"""
        global _config_cache
        _config_cache = config
    
    @staticmethod
    def get_default_config() -> Dict:
        return {
            "bus_routes": {
                "Bulawayo to Gweru": 5, "Gweru to Bulawayo": 5,
                "Bulawayo to Kwekwe": 7, "Kwekwe to Bulawayo": 7,
                "Bulawayo to Kadoma": 8, "Kadoma to Bulawayo": 8,
                "Bulawayo to Chegutu": 10, "Chegutu to Bulawayo": 10,
                "Bulawayo to Norton": 13, "Norton to Bulawayo": 13,
                "Bulawayo to Harare": 15, "Harare to Bulawayo": 15,
                "Gweru to Kwekwe": 3, "Kwekwe to Gweru": 3,
                "Gweru to Kadoma": 4, "Kadoma to Gweru": 4,
                "Gweru to Chegutu": 5, "Chegutu to Gweru": 5,
                "Gweru to Norton": 6, "Norton to Gweru": 6,
                "Gweru to Harare": 7, "Harare to Gweru": 7,
                "Kwekwe to Kadoma": 2, "Kadoma to Kwekwe": 2,
                "Kwekwe to Chegutu": 6, "Chegutu to Kwekwe": 6,
                "Kwekwe to Norton": 9, "Norton to Kwekwe": 9,
                "Kwekwe to Harare": 10, "Harare to Kwekwe": 10,
                "Kadoma to Chegutu": 4, "Chegutu to Kadoma": 4,
                "Kadoma to Norton": 5, "Norton to Kadoma": 5,
                "Kadoma to Harare": 6, "Harare to Kadoma": 6,
                "Chegutu to Norton": 1, "Norton to Chegutu": 1,
                "Chegutu to Harare": 3, "Harare to Chegutu": 3,
                "Norton to Harare": 2, "Harare to Norton": 2,
            },
            "bus_schedules": {
                "Bulawayo to Gweru": "08:00 AM", "Gweru to Bulawayo": "02:00 PM",
                "Gweru to Kwekwe": "09:00 AM", "Kwekwe to Gweru": "03:00 PM",
                "Bulawayo to Kwekwe": "09:00 AM", "Kwekwe to Bulawayo": "03:30 PM",
                "Kwekwe to Kadoma": "10:00 AM", "Kadoma to Kwekwe": "04:00 PM",
                "Bulawayo to Kadoma": "10:00 AM", "Kadoma to Bulawayo": "04:30 PM",
                "Kadoma to Chegutu": "10:30 AM", "Chegutu to Kadoma": "04:45 PM",
                "Bulawayo to Chegutu": "11:00 AM", "Chegutu to Bulawayo": "05:00 PM",
                "Bulawayo to Harare": "12:00 PM", "Harare to Bulawayo": "06:00 PM",
                "Gweru to Kadoma": "09:30 AM", "Kadoma to Gweru": "02:30 PM",
                "Gweru to Chegutu": "10:15 AM", "Chegutu to Gweru": "03:15 PM",
                "Gweru to Norton": "11:00 AM", "Norton to Gweru": "04:00 PM",
                "Gweru to Harare": "11:30 AM", "Harare to Gweru": "05:00 PM",
                "Kwekwe to Chegutu": "10:45 AM", "Chegutu to Kwekwe": "04:15 PM",
                "Kwekwe to Norton": "11:30 AM", "Norton to Kwekwe": "05:15 PM",
                "Kwekwe to Harare": "12:15 PM", "Harare to Kwekwe": "06:15 PM",
                "Kadoma to Norton": "11:00 AM", "Norton to Kadoma": "05:00 PM",
                "Kadoma to Harare": "11:30 AM", "Harare to Kadoma": "05:30 PM",
                "Chegutu to Norton": "11:45 AM", "Norton to Chegutu": "05:45 PM",
                "Chegutu to Harare": "12:15 PM", "Harare to Chegutu": "06:15 PM",
                "Norton to Harare": "12:30 PM", "Harare to Norton": "06:30 PM",
            },
            "bus_stops": {
                "Bulawayo": "City Hall, Renkini Bus Terminus, and National Railways of Zimbabwe Station.",
                "Gweru": "Main Street, City Centre, and Railway Station.",
                "Kwekwe": "City Centre, Kwekwe Mall, and Railway Station.",
                "Kadoma": "City Centre, Kadoma Mall, and Railway Station.",
                "Chegutu": "City Centre, Chegutu Mall, and Railway Station.",
                "Norton": "Main Street, Town Centre, and near the Post Office.",
                "Harare": "City Centre, Avondale, and Mbare Musika Bus Terminus."
            },
            "total_seats": 50,
            "company_name": "Chikukwa Bus Services",
            "contact_phone": "+263777189947",
            "contact_email": "support@chikukwabus.com"
        }

@app.route('/')
def index():
    return send_from_directory('../', 'index.html')

@app.route('/api/config', methods=['GET'])
def get_config():
    config = DataManager.load_config()
    cities = sorted(set([r.split(' to ')[0] for r in config['bus_routes'].keys()] +
                       [r.split(' to ')[1] for r in config['bus_routes'].keys()]))
    return jsonify({
        'cities': cities,
        'routes': config['bus_routes'],
        'schedules': config['bus_schedules'],
        'stops': config['bus_stops'],
        'total_seats': config['total_seats'],
        'company_name': config['company_name'],
        'contact_phone': config['contact_phone'],
        'contact_email': config['contact_email']
    })

@app.route('/api/route-info', methods=['POST'])
def get_route_info():
    data = request.json
    departure = data.get('departure')
    destination = data.get('destination')
    
    if not departure or not destination:
        return jsonify({'error': 'Missing departure or destination'}), 400
    
    config = DataManager.load_config()
    route = f"{departure} to {destination}"
    
    if route not in config['bus_routes']:
        return jsonify({'error': 'No direct route available'}), 404
    
    return jsonify({
        'fare': config['bus_routes'][route],
        'schedule': config['bus_schedules'].get(route, 'N/A')
    })

@app.route('/api/bookings', methods=['POST'])
def create_booking():
    data = request.json
    
    required_fields = ['name', 'age', 'phone', 'departure', 'destination', 'date', 'time', 'seat']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        age = int(data['age'])
        if age < 1 or age > 120:
            return jsonify({'error': 'Invalid age'}), 400
    except:
        return jsonify({'error': 'Invalid age format'}), 400
    
    try:
        travel_date = datetime.datetime.strptime(data['date'], "%Y-%m-%d").date()
        if travel_date < datetime.date.today():
            return jsonify({'error': 'Date must be in the future'}), 400
    except:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    try:
        seat = int(data['seat'])
        config = DataManager.load_config()
        if seat < 1 or seat > config['total_seats']:
            return jsonify({'error': f'Seat must be between 1 and {config["total_seats"]}'}), 400
    except:
        return jsonify({'error': 'Invalid seat number'}), 400
    
    route = f"{data['departure']} to {data['destination']}"
    if route not in config['bus_routes']:
        return jsonify({'error': 'No direct route available'}), 404
    
    fare = config['bus_routes'][route]
    ticket_id = str(uuid.uuid4())[:8].upper()
    
    if USE_DATABASE:
        try:
            # Check seat availability
            if not DatabaseManager.check_seat_availability(
                data['departure'], data['destination'], data['date'], data['time'], seat
            ):
                return jsonify({'error': 'This seat is already booked for this journey'}), 409
            
            # Create booking
            booking_data = {
                'ticket_id': ticket_id,
                'name': data['name'],
                'age': age,
                'phone': data['phone'],
                'email': data.get('email', ''),
                'departure': data['departure'],
                'destination': data['destination'],
                'date': data['date'],
                'time': data['time'],
                'seat': seat,
                'fare': fare,
                'status': 'confirmed'
            }
            
            result = DatabaseManager.create_booking(booking_data)
            
            # Convert datetime objects to strings for JSON response
            return jsonify({
                'ticket_id': result['ticket_id'],
                'name': result['name'],
                'age': result['age'],
                'phone': result['phone'],
                'email': result.get('email', ''),
                'departure': result['departure'],
                'destination': result['destination'],
                'date': result['date'].isoformat() if hasattr(result['date'], 'isoformat') else str(result['date']),
                'time': result['time'],
                'seat': result['seat'],
                'fare': float(result['fare']),
                'status': result['status'],
                'booked_at': result['booked_at'].isoformat() if hasattr(result['booked_at'], 'isoformat') else str(result['booked_at'])
            }), 201
        except Exception as e:
            print(f"Database error: {e}")
            return jsonify({'error': 'Failed to create booking'}), 500
    else:
        # Fallback to in-memory storage
        bookings = DataManager.load_bookings()
        
        # Check seat availability
        for booking in bookings.values():
            if (booking['departure'] == data['departure'] and 
                booking['destination'] == data['destination'] and
                booking['date'] == data['date'] and
                booking['time'] == data['time'] and
                booking['seat'] == seat and
                booking.get('status') != 'cancelled'):
                return jsonify({'error': 'This seat is already booked for this journey'}), 409
        
        booking_data = {
            'ticket_id': ticket_id,
            'name': data['name'],
            'age': age,
            'phone': data['phone'],
            'email': data.get('email', ''),
            'departure': data['departure'],
            'destination': data['destination'],
            'date': data['date'],
            'time': data['time'],
            'seat': seat,
            'fare': fare,
            'status': 'confirmed',
            'booked_at': datetime.datetime.now().isoformat(),
        }
        
        bookings[ticket_id] = booking_data
        DataManager.save_bookings(bookings)
        
        return jsonify(booking_data), 201

@app.route('/api/bookings/<ticket_id>', methods=['GET'])
def get_booking(ticket_id):
    ticket_id = ticket_id.upper()
    
    if USE_DATABASE:
        try:
            booking = DatabaseManager.get_booking(ticket_id)
            if not booking:
                return jsonify({'error': 'Ticket not found'}), 404
            
            return jsonify({
                'ticket_id': booking['ticket_id'],
                'name': booking['name'],
                'age': booking['age'],
                'phone': booking['phone'],
                'email': booking.get('email', ''),
                'departure': booking['departure'],
                'destination': booking['destination'],
                'date': booking['date'].isoformat() if hasattr(booking['date'], 'isoformat') else str(booking['date']),
                'time': booking['time'],
                'seat': booking['seat'],
                'fare': float(booking['fare']),
                'status': booking['status'],
                'booked_at': booking['booked_at'].isoformat() if hasattr(booking['booked_at'], 'isoformat') else str(booking['booked_at'])
            })
        except Exception as e:
            print(f"Database error: {e}")
            return jsonify({'error': 'Failed to fetch booking'}), 500
    else:
        bookings = DataManager.load_bookings()
        if ticket_id not in bookings:
            return jsonify({'error': 'Ticket not found'}), 404
        return jsonify(bookings[ticket_id])

@app.route('/api/bookings/<ticket_id>', methods=['DELETE'])
def cancel_booking(ticket_id):
    ticket_id = ticket_id.upper()
    
    if USE_DATABASE:
        try:
            booking = DatabaseManager.get_booking(ticket_id)
            if not booking:
                return jsonify({'error': 'Ticket not found'}), 404
            
            if booking['status'] == 'cancelled':
                return jsonify({'error': 'Ticket already cancelled'}), 400
            
            DatabaseManager.cancel_booking(ticket_id)
            return jsonify({'message': 'Ticket cancelled successfully'})
        except Exception as e:
            print(f"Database error: {e}")
            return jsonify({'error': 'Failed to cancel booking'}), 500
    else:
        bookings = DataManager.load_bookings()
        if ticket_id not in bookings:
            return jsonify({'error': 'Ticket not found'}), 404
        
        if bookings[ticket_id].get('status') == 'cancelled':
            return jsonify({'error': 'Ticket already cancelled'}), 400
        
        bookings[ticket_id]['status'] = 'cancelled'
        DataManager.save_bookings(bookings)
        return jsonify({'message': 'Ticket cancelled successfully'})

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    if username in ADMIN_CREDENTIALS:
        if ADMIN_CREDENTIALS[username] == hashlib.sha256(password.encode()).hexdigest():
            return jsonify({'success': True, 'username': username})
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/admin/bookings', methods=['GET'])
def admin_get_all_bookings():
    if USE_DATABASE:
        try:
            bookings_list = DatabaseManager.get_all_bookings()
            # Convert datetime objects for JSON
            result = []
            for booking in bookings_list:
                result.append({
                    'ticket_id': booking['ticket_id'],
                    'name': booking['name'],
                    'age': booking['age'],
                    'phone': booking['phone'],
                    'email': booking.get('email', ''),
                    'departure': booking['departure'],
                    'destination': booking['destination'],
                    'date': booking['date'].isoformat() if hasattr(booking['date'], 'isoformat') else str(booking['date']),
                    'time': booking['time'],
                    'seat': booking['seat'],
                    'fare': float(booking['fare']),
                    'status': booking['status'],
                    'booked_at': booking['booked_at'].isoformat() if hasattr(booking['booked_at'], 'isoformat') else str(booking['booked_at'])
                })
            return jsonify(result)
        except Exception as e:
            print(f"Database error: {e}")
            return jsonify([])
    else:
        bookings = DataManager.load_bookings()
        return jsonify(list(bookings.values()))

@app.route('/api/admin/stats', methods=['GET'])
def admin_stats():
    if USE_DATABASE:
        try:
            stats = DatabaseManager.get_booking_stats()
            top_routes = DatabaseManager.get_top_routes(5)
            
            return jsonify({
                'total_bookings': stats['total_bookings'],
                'confirmed': stats['confirmed'],
                'cancelled': stats['cancelled'],
                'total_revenue': float(stats['total_revenue']),
                'top_routes': [{'route': r['route'], 'count': r['count']} for r in top_routes]
            })
        except Exception as e:
            print(f"Database error: {e}")
            return jsonify({
                'total_bookings': 0,
                'confirmed': 0,
                'cancelled': 0,
                'total_revenue': 0,
                'top_routes': []
            })
    else:
        bookings = DataManager.load_bookings()
        
        total_bookings = len(bookings)
        confirmed = sum(1 for b in bookings.values() if b.get('status') == 'confirmed')
        cancelled = sum(1 for b in bookings.values() if b.get('status') == 'cancelled')
        total_revenue = sum(b.get('fare', 0) for b in bookings.values() 
                           if b.get('status') == 'confirmed')
        
        route_stats = {}
        for booking in bookings.values():
            if booking.get('status') == 'confirmed':
                route = f"{booking.get('departure')} to {booking.get('destination')}"
                route_stats[route] = route_stats.get(route, 0) + 1
        
        top_routes = sorted(route_stats.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return jsonify({
            'total_bookings': total_bookings,
            'confirmed': confirmed,
            'cancelled': cancelled,
            'total_revenue': total_revenue,
            'top_routes': [{'route': r, 'count': c} for r, c in top_routes]
        })

@app.route('/api/admin/routes', methods=['GET'])
def admin_get_routes():
    config = DataManager.load_config()
    routes = []
    for route, fare in config['bus_routes'].items():
        schedule = config['bus_schedules'].get(route, 'N/A')
        routes.append({
            'route': route,
            'fare': fare,
            'schedule': schedule
        })
    return jsonify(routes)

@app.route('/api/admin/routes', methods=['PUT'])
def admin_update_route():
    data = request.json
    route = data.get('route')
    new_fare = data.get('fare')
    
    if not route or new_fare is None:
        return jsonify({'error': 'Missing route or fare'}), 400
    
    config = DataManager.load_config()
    if route not in config['bus_routes']:
        return jsonify({'error': 'Route not found'}), 404
    
    config['bus_routes'][route] = float(new_fare)
    DataManager.save_config(config)
    
    return jsonify({'message': 'Route updated successfully'})

@app.route('/api/schedules', methods=['GET'])
def get_schedules():
    config = DataManager.load_config()
    schedules = []
    for route, schedule in sorted(config['bus_schedules'].items()):
        fare = config['bus_routes'].get(route, 0)
        schedules.append({
            'route': route,
            'schedule': schedule,
            'fare': fare
        })
    return jsonify(schedules)

@app.route('/api/stops/<city>', methods=['GET'])
def get_stops(city):
    config = DataManager.load_config()
    stops = config['bus_stops'].get(city)
    
    if not stops:
        return jsonify({'error': 'City not found'}), 404
    
    return jsonify({'city': city, 'stops': stops})

if __name__ == '__main__':
    app.run(debug=True)
