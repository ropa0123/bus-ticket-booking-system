const API_BASE = '/api';
let currentConfig = null;
let isAdminLoggedIn = false;
let currentAdminUsername = null;

document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupEventListeners();
});

function initializeApp() {
    loadConfig();
    setMinDate();
}

function setupEventListeners() {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', (e) => switchTab(e.target.closest('.tab-btn').dataset.tab));
    });

    document.getElementById('bookingForm').addEventListener('submit', handleBooking);
    document.getElementById('adminLoginForm').addEventListener('submit', handleAdminLogin);
}

function switchTab(tabName) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    document.getElementById(`${tabName}Tab`).classList.add('active');
    
    if (tabName === 'admin' && !isAdminLoggedIn) {
        document.getElementById('adminLogin').style.display = 'block';
        document.getElementById('adminDashboard').style.display = 'none';
    } else if (tabName === 'admin' && isAdminLoggedIn) {
        document.getElementById('adminLogin').style.display = 'none';
        document.getElementById('adminDashboard').style.display = 'block';
        loadAdminStats();
        loadAllBookings();
    }
}

function showSection(sectionName) {
    document.querySelectorAll('.section').forEach(section => section.classList.remove('active'));
    document.getElementById(`${sectionName}Section`).classList.add('active');
    
    if (sectionName === 'schedule') {
        loadSchedules();
    }
}

async function loadConfig() {
    try {
        const response = await fetch(`${API_BASE}/config`);
        currentConfig = await response.json();
        
        populateCitySelects();
        populateSeatSelect();
        updateCompanyInfo();
    } catch (error) {
        showError('Failed to load configuration');
    }
}

function populateCitySelects() {
    const selects = ['departure', 'destination', 'routeDeparture', 'routeDestination', 'citySelect'];
    selects.forEach(id => {
        const select = document.getElementById(id);
        select.innerHTML = '<option value="">Select City</option>';
        currentConfig.cities.forEach(city => {
            select.innerHTML += `<option value="${city}">${city}</option>`;
        });
    });
}

function populateSeatSelect() {
    const select = document.getElementById('seat');
    select.innerHTML = '<option value="">Select Seat</option>';
    for (let i = 1; i <= currentConfig.total_seats; i++) {
        select.innerHTML += `<option value="${i}">${i}</option>`;
    }
}

function updateCompanyInfo() {
    document.getElementById('companyName').textContent = currentConfig.company_name;
    document.getElementById('contactPhone').textContent = currentConfig.contact_phone;
    document.getElementById('contactEmail').textContent = currentConfig.contact_email;
}

function setMinDate() {
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('date').min = today;
}

async function calculateFare() {
    const departure = document.getElementById('departure').value;
    const destination = document.getElementById('destination').value;
    
    if (!departure || !destination) {
        document.getElementById('fareDisplay').textContent = 'Fare: $0';
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/route-info`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ departure, destination })
        });
        
        if (response.ok) {
            const data = await response.json();
            document.getElementById('fareDisplay').textContent = `Fare: $${data.fare}`;
        } else {
            document.getElementById('fareDisplay').textContent = 'No route available';
        }
    } catch (error) {
        showError('Failed to calculate fare');
    }
}

async function handleBooking(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = {
        name: formData.get('name'),
        age: formData.get('age'),
        phone: formData.get('phone'),
        email: formData.get('email') || '',
        departure: formData.get('departure'),
        destination: formData.get('destination'),
        date: formData.get('date'),
        time: formData.get('time'),
        seat: formData.get('seat')
    };
    
    try {
        const response = await fetch(`${API_BASE}/bookings`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            const booking = await response.json();
            showBookingReceipt(booking);
            e.target.reset();
            document.getElementById('fareDisplay').textContent = 'Fare: $0';
        } else {
            const error = await response.json();
            showError(error.error || 'Booking failed');
        }
    } catch (error) {
        showError('Failed to process booking');
    }
}

function showBookingReceipt(booking) {
    const receipt = `
        <div class="receipt">
            <h2>✅ Booking Confirmed!</h2>
            <div class="receipt-details">
                <p><strong>Ticket ID:</strong> ${booking.ticket_id}</p>
                <p><strong>Name:</strong> ${booking.name}</p>
                <p><strong>Phone:</strong> ${booking.phone}</p>
                <hr>
                <p><strong>From:</strong> ${booking.departure}</p>
                <p><strong>To:</strong> ${booking.destination}</p>
                <p><strong>Date:</strong> ${booking.date}</p>
                <p><strong>Time:</strong> ${booking.time}</p>
                <p><strong>Seat:</strong> ${booking.seat}</p>
                <hr>
                <p><strong>Fare:</strong> $${booking.fare}</p>
                <p><strong>Status:</strong> <span class="status-confirmed">CONFIRMED</span></p>
            </div>
            <p class="receipt-note">Please save your Ticket ID: <strong>${booking.ticket_id}</strong></p>
            <p>Arrive 15 minutes before departure time.</p>
        </div>
    `;
    showModal(receipt);
}

async function viewTicket() {
    const ticketId = document.getElementById('viewTicketId').value.trim().toUpperCase();
    
    if (!ticketId) {
        showError('Please enter a ticket ID');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/bookings/${ticketId}`);
        
        if (response.ok) {
            const booking = await response.json();
            displayTicketDetails(booking);
        } else {
            showError('Ticket not found');
        }
    } catch (error) {
        showError('Failed to fetch ticket');
    }
}

function displayTicketDetails(booking) {
    const statusClass = booking.status === 'confirmed' ? 'status-confirmed' : 'status-cancelled';
    const html = `
        <h3>Ticket Details</h3>
        <div class="ticket-info">
            <p><strong>Ticket ID:</strong> ${booking.ticket_id}</p>
            <p><strong>Name:</strong> ${booking.name}</p>
            <p><strong>Phone:</strong> ${booking.phone}</p>
            ${booking.email ? `<p><strong>Email:</strong> ${booking.email}</p>` : ''}
            <p><strong>Route:</strong> ${booking.departure} → ${booking.destination}</p>
            <p><strong>Date:</strong> ${booking.date}</p>
            <p><strong>Time:</strong> ${booking.time}</p>
            <p><strong>Seat:</strong> ${booking.seat}</p>
            <p><strong>Fare:</strong> $${booking.fare}</p>
            <p><strong>Status:</strong> <span class="${statusClass}">${booking.status.toUpperCase()}</span></p>
        </div>
    `;
    document.getElementById('ticketDetails').innerHTML = html;
}

async function cancelTicket() {
    const ticketId = document.getElementById('cancelTicketId').value.trim().toUpperCase();
    
    if (!ticketId) {
        showError('Please enter a ticket ID');
        return;
    }
    
    if (!confirm(`Are you sure you want to cancel ticket ${ticketId}?`)) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/bookings/${ticketId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showSuccess('Ticket cancelled successfully');
            document.getElementById('cancelTicketId').value = '';
        } else {
            const error = await response.json();
            showError(error.error || 'Cancellation failed');
        }
    } catch (error) {
        showError('Failed to cancel ticket');
    }
}

async function checkRouteFare() {
    const departure = document.getElementById('routeDeparture').value;
    const destination = document.getElementById('routeDestination').value;
    
    if (!departure || !destination) {
        showError('Please select both departure and destination');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/route-info`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ departure, destination })
        });
        
        if (response.ok) {
            const data = await response.json();
            const html = `
                <h3>Route Information</h3>
                <p><strong>Route:</strong> ${departure} → ${destination}</p>
                <p><strong>Fare:</strong> $${data.fare}</p>
                <p><strong>Departure Time:</strong> ${data.schedule}</p>
            `;
            document.getElementById('routeInfo').innerHTML = html;
        } else {
            showError('No direct route available');
        }
    } catch (error) {
        showError('Failed to fetch route information');
    }
}

async function loadSchedules() {
    try {
        const response = await fetch(`${API_BASE}/schedules`);
        const schedules = await response.json();
        
        let html = `
            <table>
                <thead>
                    <tr>
                        <th>Route</th>
                        <th>Departure Time</th>
                        <th>Fare</th>
                    </tr>
                </thead>
                <tbody>
        `;
        
        schedules.forEach(schedule => {
            html += `
                <tr>
                    <td>${schedule.route}</td>
                    <td>${schedule.schedule}</td>
                    <td>$${schedule.fare}</td>
                </tr>
            `;
        });
        
        html += `</tbody></table>`;
        document.getElementById('scheduleTable').innerHTML = html;
    } catch (error) {
        showError('Failed to load schedules');
    }
}

async function showBusStops() {
    const city = document.getElementById('citySelect').value;
    
    if (!city) {
        showError('Please select a city');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/stops/${city}`);
        
        if (response.ok) {
            const data = await response.json();
            const html = `
                <h3>Bus Stops in ${data.city}</h3>
                <p>${data.stops}</p>
            `;
            document.getElementById('stopsInfo').innerHTML = html;
        } else {
            showError('City not found');
        }
    } catch (error) {
        showError('Failed to fetch bus stops');
    }
}

async function handleAdminLogin(e) {
    e.preventDefault();
    
    const username = document.getElementById('adminUsername').value;
    const password = document.getElementById('adminPassword').value;
    
    try {
        const response = await fetch(`${API_BASE}/admin/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            isAdminLoggedIn = true;
            currentAdminUsername = data.username;
            updateAdminStatus();
            document.getElementById('adminLogin').style.display = 'none';
            document.getElementById('adminDashboard').style.display = 'block';
            loadAdminStats();
            loadAllBookings();
            e.target.reset();
        } else {
            showError('Invalid credentials');
        }
    } catch (error) {
        showError('Login failed');
    }
}

function adminLogout() {
    if (confirm('Are you sure you want to logout?')) {
        isAdminLoggedIn = false;
        currentAdminUsername = null;
        updateAdminStatus();
        document.getElementById('adminLogin').style.display = 'block';
        document.getElementById('adminDashboard').style.display = 'none';
    }
}

function updateAdminStatus() {
    const statusEl = document.getElementById('adminStatus');
    if (isAdminLoggedIn) {
        statusEl.textContent = `👤 Admin: ${currentAdminUsername}`;
    } else {
        statusEl.textContent = '';
    }
}

async function loadAdminStats() {
    try {
        const response = await fetch(`${API_BASE}/admin/stats`);
        const stats = await response.json();
        
        document.getElementById('statTotal').textContent = stats.total_bookings;
        document.getElementById('statConfirmed').textContent = stats.confirmed;
        document.getElementById('statCancelled').textContent = stats.cancelled;
        document.getElementById('statRevenue').textContent = `$${stats.total_revenue}`;
    } catch (error) {
        showError('Failed to load statistics');
    }
}

async function loadAllBookings() {
    try {
        const response = await fetch(`${API_BASE}/admin/bookings`);
        const bookings = await response.json();
        
        let html = `
            <table>
                <thead>
                    <tr>
                        <th>Ticket ID</th>
                        <th>Name</th>
                        <th>Phone</th>
                        <th>Route</th>
                        <th>Date</th>
                        <th>Seat</th>
                        <th>Fare</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
        `;
        
        if (bookings.length === 0) {
            html += '<tr><td colspan="9" style="text-align:center">No bookings found</td></tr>';
        } else {
            bookings.forEach(booking => {
                const statusClass = booking.status === 'confirmed' ? 'status-confirmed' : 'status-cancelled';
                html += `
                    <tr>
                        <td>${booking.ticket_id}</td>
                        <td>${booking.name}</td>
                        <td>${booking.phone}</td>
                        <td>${booking.departure} → ${booking.destination}</td>
                        <td>${booking.date}</td>
                        <td>${booking.seat}</td>
                        <td>$${booking.fare}</td>
                        <td><span class="${statusClass}">${booking.status}</span></td>
                        <td>
                            <button class="action-btn action-btn-primary" onclick='viewBookingDetails(${JSON.stringify(booking)})'>View</button>
                            ${booking.status === 'confirmed' ? 
                                `<button class="action-btn action-btn-danger" onclick="adminCancelBooking('${booking.ticket_id}')">Cancel</button>` : 
                                ''}
                        </td>
                    </tr>
                `;
            });
        }
        
        html += `</tbody></table>`;
        document.getElementById('bookingsTable').innerHTML = html;
    } catch (error) {
        showError('Failed to load bookings');
    }
}

function viewBookingDetails(booking) {
    const statusClass = booking.status === 'confirmed' ? 'status-confirmed' : 'status-cancelled';
    const html = `
        <h2>Booking Details</h2>
        <div class="ticket-info">
            <p><strong>Ticket ID:</strong> ${booking.ticket_id}</p>
            <p><strong>Name:</strong> ${booking.name}</p>
            <p><strong>Age:</strong> ${booking.age}</p>
            <p><strong>Phone:</strong> ${booking.phone}</p>
            ${booking.email ? `<p><strong>Email:</strong> ${booking.email}</p>` : ''}
            <p><strong>Route:</strong> ${booking.departure} → ${booking.destination}</p>
            <p><strong>Date:</strong> ${booking.date}</p>
            <p><strong>Time:</strong> ${booking.time}</p>
            <p><strong>Seat:</strong> ${booking.seat}</p>
            <p><strong>Fare:</strong> $${booking.fare}</p>
            <p><strong>Status:</strong> <span class="${statusClass}">${booking.status.toUpperCase()}</span></p>
            <p><strong>Booked At:</strong> ${new Date(booking.booked_at).toLocaleString()}</p>
        </div>
    `;
    showModal(html);
}

async function adminCancelBooking(ticketId) {
    if (!confirm(`Are you sure you want to cancel ticket ${ticketId}?`)) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/bookings/${ticketId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showSuccess('Booking cancelled successfully');
            loadAllBookings();
            loadAdminStats();
        } else {
            showError('Failed to cancel booking');
        }
    } catch (error) {
        showError('Failed to cancel booking');
    }
}

function showAdminSection(section) {
    document.querySelectorAll('.admin-section-content').forEach(el => el.classList.remove('active'));
    document.getElementById(`admin${section.charAt(0).toUpperCase() + section.slice(1)}Section`).classList.add('active');
    
    if (section === 'routes') {
        loadAdminRoutes();
    } else if (section === 'report') {
        generateReport();
    }
}

async function loadAdminRoutes() {
    try {
        const response = await fetch(`${API_BASE}/admin/routes`);
        const routes = await response.json();
        
        let html = `
            <table>
                <thead>
                    <tr>
                        <th>Route</th>
                        <th>Fare ($)</th>
                        <th>Departure Time</th>
                    </tr>
                </thead>
                <tbody>
        `;
        
        routes.forEach(route => {
            html += `
                <tr>
                    <td>${route.route}</td>
                    <td>$${route.fare}</td>
                    <td>${route.schedule}</td>
                </tr>
            `;
        });
        
        html += `</tbody></table>`;
        document.getElementById('routesTable').innerHTML = html;
    } catch (error) {
        showError('Failed to load routes');
    }
}

async function generateReport() {
    try {
        const response = await fetch(`${API_BASE}/admin/stats`);
        const stats = await response.json();
        
        let report = `
╔══════════════════════════════════════╗
║       BOOKING STATISTICS REPORT       ║
╚══════════════════════════════════════╝

Total Bookings: ${stats.total_bookings}
├─ Confirmed: ${stats.confirmed}
├─ Cancelled: ${stats.cancelled}
└─ Pending: ${stats.total_bookings - stats.confirmed - stats.cancelled}

Financial Summary:
├─ Total Revenue: $${stats.total_revenue.toFixed(2)}
└─ Average per Booking: $${stats.confirmed > 0 ? (stats.total_revenue / stats.confirmed).toFixed(2) : '0.00'}

Top Routes:
`;
        
        stats.top_routes.forEach((route, i) => {
            report += `  ${i + 1}. ${route.route}: ${route.count} bookings\n`;
        });
        
        report += `\nReport Generated: ${new Date().toLocaleString()}`;
        
        document.getElementById('reportContent').textContent = report;
    } catch (error) {
        showError('Failed to generate report');
    }
}

function showModal(content) {
    document.getElementById('modalBody').innerHTML = content;
    document.getElementById('modal').classList.add('show');
}

function closeModal() {
    document.getElementById('modal').classList.remove('show');
}

function showError(message) {
    alert('❌ ' + message);
}

function showSuccess(message) {
    alert('✅ ' + message);
}

window.onclick = function(event) {
    const modal = document.getElementById('modal');
    if (event.target === modal) {
        closeModal();
    }
}
