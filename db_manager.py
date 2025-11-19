import os
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool
from typing import Dict, List, Optional
from contextlib import contextmanager

class DatabaseManager:
    """Database manager with connection pooling for PostgreSQL"""
    
    _pool = None
    
    @classmethod
    def initialize_pool(cls):
        """Initialize database connection pool"""
        if cls._pool is None:
            database_url = os.environ.get('POSTGRES_URL') or os.environ.get('DATABASE_URL')
            if not database_url:
                raise ValueError("Database URL not found in environment variables")
            
            # Parse connection string and add sslmode if needed
            if 'sslmode' not in database_url:
                database_url += '?sslmode=require'
            
            cls._pool = SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                dsn=database_url
            )
    
    @classmethod
    @contextmanager
    def get_connection(cls):
        """Get a database connection from the pool"""
        if cls._pool is None:
            cls.initialize_pool()
        
        conn = cls._pool.getconn()
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cls._pool.putconn(conn)
    
    @classmethod
    def execute_query(cls, query: str, params: tuple = None, fetch: bool = True):
        """Execute a query and return results"""
        with cls.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                if fetch:
                    return cursor.fetchall()
                return cursor.rowcount
    
    @classmethod
    def execute_one(cls, query: str, params: tuple = None):
        """Execute a query and return a single result"""
        with cls.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()
    
    # Booking operations
    @classmethod
    def create_booking(cls, booking_data: Dict) -> Dict:
        """Create a new booking"""
        query = """
            INSERT INTO bookings 
            (ticket_id, name, age, phone, email, departure, destination, date, time, seat, fare, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """
        params = (
            booking_data['ticket_id'],
            booking_data['name'],
            booking_data['age'],
            booking_data['phone'],
            booking_data.get('email', ''),
            booking_data['departure'],
            booking_data['destination'],
            booking_data['date'],
            booking_data['time'],
            booking_data['seat'],
            booking_data['fare'],
            booking_data.get('status', 'confirmed')
        )
        return dict(cls.execute_one(query, params))
    
    @classmethod
    def get_booking(cls, ticket_id: str) -> Optional[Dict]:
        """Get a booking by ticket ID"""
        query = "SELECT * FROM bookings WHERE ticket_id = %s"
        result = cls.execute_one(query, (ticket_id,))
        return dict(result) if result else None
    
    @classmethod
    def get_all_bookings(cls) -> List[Dict]:
        """Get all bookings"""
        query = "SELECT * FROM bookings ORDER BY booked_at DESC"
        return [dict(row) for row in cls.execute_query(query)]
    
    @classmethod
    def cancel_booking(cls, ticket_id: str) -> bool:
        """Cancel a booking"""
        query = "UPDATE bookings SET status = 'cancelled', updated_at = CURRENT_TIMESTAMP WHERE ticket_id = %s"
        return cls.execute_query(query, (ticket_id,), fetch=False) > 0
    
    @classmethod
    def check_seat_availability(cls, departure: str, destination: str, date: str, time: str, seat: int) -> bool:
        """Check if a seat is available for a specific journey"""
        query = """
            SELECT COUNT(*) as count FROM bookings 
            WHERE departure = %s AND destination = %s AND date = %s AND time = %s 
            AND seat = %s AND status = 'confirmed'
        """
        result = cls.execute_one(query, (departure, destination, date, time, seat))
        return result['count'] == 0
    
    # Route operations
    @classmethod
    def get_all_routes(cls) -> List[Dict]:
        """Get all routes"""
        query = "SELECT * FROM routes ORDER BY route_name"
        return [dict(row) for row in cls.execute_query(query)]
    
    @classmethod
    def get_route(cls, route_name: str) -> Optional[Dict]:
        """Get a route by name"""
        query = "SELECT * FROM routes WHERE route_name = %s"
        result = cls.execute_one(query, (route_name,))
        return dict(result) if result else None
    
    @classmethod
    def update_route_fare(cls, route_name: str, fare: float) -> bool:
        """Update route fare"""
        query = "UPDATE routes SET fare = %s, updated_at = CURRENT_TIMESTAMP WHERE route_name = %s"
        return cls.execute_query(query, (fare, route_name), fetch=False) > 0
    
    @classmethod
    def get_all_cities(cls) -> List[str]:
        """Get all unique cities from routes"""
        query = """
            SELECT DISTINCT city FROM (
                SELECT SPLIT_PART(route_name, ' to ', 1) as city FROM routes
                UNION
                SELECT SPLIT_PART(route_name, ' to ', 2) as city FROM routes
            ) cities
            ORDER BY city
        """
        return [row['city'] for row in cls.execute_query(query)]
    
    # Bus stops operations
    @classmethod
    def get_bus_stops(cls, city: str) -> Optional[Dict]:
        """Get bus stops for a city"""
        query = "SELECT * FROM bus_stops WHERE city = %s"
        result = cls.execute_one(query, (city,))
        return dict(result) if result else None
    
    @classmethod
    def get_all_bus_stops(cls) -> List[Dict]:
        """Get all bus stops"""
        query = "SELECT * FROM bus_stops ORDER BY city"
        return [dict(row) for row in cls.execute_query(query)]
    
    # Config operations
    @classmethod
    def get_config(cls, key: str) -> Optional[str]:
        """Get a configuration value"""
        query = "SELECT config_value FROM system_config WHERE config_key = %s"
        result = cls.execute_one(query, (key,))
        return result['config_value'] if result else None
    
    @classmethod
    def get_all_config(cls) -> Dict:
        """Get all configuration"""
        query = "SELECT config_key, config_value FROM system_config"
        results = cls.execute_query(query)
        return {row['config_key']: row['config_value'] for row in results}
    
    @classmethod
    def set_config(cls, key: str, value: str) -> bool:
        """Set a configuration value"""
        query = """
            INSERT INTO system_config (config_key, config_value)
            VALUES (%s, %s)
            ON CONFLICT (config_key) 
            DO UPDATE SET config_value = EXCLUDED.config_value, updated_at = CURRENT_TIMESTAMP
        """
        return cls.execute_query(query, (key, value), fetch=False) >= 0
    
    # Statistics
    @classmethod
    def get_booking_stats(cls) -> Dict:
        """Get booking statistics"""
        query = """
            SELECT 
                COUNT(*) as total_bookings,
                COUNT(*) FILTER (WHERE status = 'confirmed') as confirmed,
                COUNT(*) FILTER (WHERE status = 'cancelled') as cancelled,
                COALESCE(SUM(fare) FILTER (WHERE status = 'confirmed'), 0) as total_revenue
            FROM bookings
        """
        return dict(cls.execute_one(query))
    
    @classmethod
    def get_top_routes(cls, limit: int = 5) -> List[Dict]:
        """Get top routes by booking count"""
        query = """
            SELECT 
                departure || ' to ' || destination as route,
                COUNT(*) as count
            FROM bookings
            WHERE status = 'confirmed'
            GROUP BY departure, destination
            ORDER BY count DESC
            LIMIT %s
        """
        return [dict(row) for row in cls.execute_query(query, (limit,))]
