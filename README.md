# PIX Payment System

A complete PIX payment processing system built with Flask that enables real-time payment creation, QR code generation, and payment confirmation with WebSocket integration for instant status updates.

## 🚀 Features

- **PIX Payment Creation**: Generate PIX payments with automatic expiration
- **QR Code Generation**: Dynamic QR code creation for each payment
- **Real-time Updates**: WebSocket integration for instant payment notifications
- **Payment Confirmation**: Secure payment verification system
- **Web Interface**: Complete HTML templates for payment flow
- **Status Tracking**: Monitor payment status in real-time
- **Database Integration**: SQLAlchemy ORM for data persistence
- **Error Handling**: Comprehensive validation and error responses
- **Static File Serving**: Automatic QR code image serving

## 🛠️ Tech Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLite with SQLAlchemy ORM
- **Real-time**: Flask-SocketIO for WebSocket communication
- **QR Generation**: qrcode library with Pillow for image processing
- **Frontend**: HTML templates with CSS styling
- **Testing**: pytest for automated testing

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Modern web browser with WebSocket support
- Basic understanding of PIX payment system

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd pix-payment-system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database**
   ```bash
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

5. **Create static directories**
   ```bash
   mkdir -p static/img
   mkdir -p static/css
   mkdir -p static/template_img
   ```

## 🚦 Running the Application

1. **Start the server**
   ```bash
   python app.py
   ```

2. **Access the application**
   - API Base URL: `http://127.0.0.1:5000`
   - Payment pages: `http://127.0.0.1:5000/payments/pix/{payment_id}`

## 📚 API Documentation

### Payment Creation

#### POST /payments/pix
Create a new PIX payment with QR code generation.

**Request Body:**
```json
{
  "value": 99.99
}
```

**Response (201 Created):**
```json
{
  "message": "Pagamento PIX criado com sucesso!",
  "payment": {
    "id": 1,
    "value": 99.99,
    "bank_payment_id": "uuid-string",
    "qr_code": "qr_code_payment_uuid",
    "paid": false,
    "expiration_date": "2025-08-23T12:00:00Z"
  }
}
```

**Error Response (400 Bad Request):**
```json
{
  "message": "Dados inválidos"
}
```

### QR Code Access

#### GET /payments/pix/qr_code/{file_name}
Retrieve the QR code image for a specific payment.

**Parameters:**
- `file_name`: QR code filename (without .png extension)

**Response:**
- Returns PNG image with `image/png` mimetype
- Direct image download for display in payment interface

### Payment Confirmation

#### POST /payments/pix/confirmation
Confirm a PIX payment transaction.

**Request Body:**
```json
{
  "bank_payment_id": "uuid-string",
  "value": 99.99
}
```

**Success Response (200 OK):**
```json
{
  "message": "Confirmação do pagamento PIX gerada com sucesso!"
}
```

**Error Responses:**
- **400 Bad Request**: Missing required fields
- **404 Not Found**: Payment not found or already paid
- **400 Bad Request**: Incorrect payment value

### Payment Status Page

#### GET /payments/pix/{payment_id}
Display payment status page with real-time updates.

**Parameters:**
- `payment_id`: Payment ID (integer)

**Responses:**
- **200 OK**: Returns payment.html (pending) or confirmed_payment.html (paid)
- **404 Not Found**: Returns 404.html template

## 🎯 Payment Flow

### 1. Payment Creation
```python
# Client creates payment
POST /payments/pix
{
  "value": 150.00
}

# System generates:
# - Unique bank_payment_id
# - QR code image
# - Database record
# - Expiration date (+24h)
```

### 2. Payment Display
```python
# User accesses payment page
GET /payments/pix/1

# Page loads with:
# - QR code image
# - Payment value
# - WebSocket connection
# - Real-time status monitoring
```

### 3. Payment Confirmation
```python
# Bank/system confirms payment
POST /payments/pix/confirmation
{
  "bank_payment_id": "uuid",
  "value": 150.00
}

# System:
# - Validates payment
# - Updates database
# - Emits WebSocket event
# - User page refreshes automatically
```

## 🏗️ Project Structure

```
pix-payment-system/
├── app.py                     # Main Flask application
├── requirements.txt           # Python dependencies
├── repository/
│   └── database.py           # Database configuration
├── db_models/
│   └── payments.py           # Payment model
├── payments/
│   └── pix.py               # PIX payment logic
├── templates/
│   ├── payment.html         # Pending payment page
│   ├── confirmed_payment.html # Confirmed payment page
│   └── 404.html             # Not found page
├── static/
│   ├── css/                 # Stylesheets
│   ├── img/                 # Generated QR codes
│   └── template_img/        # Static images
└── payments.db              # SQLite database
```

## 🔄 WebSocket Integration

### Real-time Payment Updates

The system uses Flask-SocketIO for real-time communication:

```javascript
// Client-side connection
var socket = io.connect('http://127.0.0.1:5000');

// Listen for payment confirmation
socket.on('payment-confirmed-{payment_id}', function() {
    location.reload(); // Refresh to show confirmed status
});
```

### Server-side Events

```python
# Payment confirmation triggers WebSocket event
@app.route('/payments/pix/confirmation', methods=['POST'])
def get_pix_confirmation():
    # ... validation logic ...
    
    payment.paid = True
    db.session.commit()
    
    # Emit real-time notification
    socketio.emit(f'payment-confirmed-{payment.id}')
    
    return jsonify({"message": "Confirmação gerada com sucesso!"})
```

## 🔒 Security Features

- **Payment Validation**: Multiple validation layers for payment data
- **Unique Identifiers**: UUID-based payment IDs for security
- **Expiration Control**: 24-hour automatic payment expiration
- **Value Verification**: Exact amount matching for confirmation
- **Status Protection**: Prevents double payment processing

## 🧪 Testing

### Manual Testing with curl

```bash
# Create payment
curl -X POST http://127.0.0.1:5000/payments/pix \
  -H "Content-Type: application/json" \
  -d '{"value": 99.99}'

# Get QR code
curl http://127.0.0.1:5000/payments/pix/qr_code/qr_code_payment_uuid \
  --output qrcode.png

# Confirm payment
curl -X POST http://127.0.0.1:5000/payments/pix/confirmation \
  -H "Content-Type: application/json" \
  -d '{"bank_payment_id": "uuid-string", "value": 99.99}'
```

### Automated Testing

```bash
# Run pytest suite
pytest

# Run with coverage
pytest --cov=app
```

## 🎨 UI/UX Features

### Payment Interface
- **Clean Design**: Modern, responsive payment interface
- **Real-time Updates**: Instant status changes without refresh
- **QR Code Display**: Large, scannable QR codes
- **Progress Indicators**: Clear payment status visualization
- **Error Handling**: User-friendly error messages

### Template System
- **payment.html**: Pending payment display with WebSocket integration
- **confirmed_payment.html**: Success page with confirmation details
- **404.html**: Custom error page for invalid payment IDs

## ⚙️ Configuration

### Environment Variables
```bash
export FLASK_ENV=development
export DATABASE_URL=sqlite:///payments.db
export SECRET_KEY=your-secret-key
```

### Database Configuration
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payments.db'
app.config['SECRET_KEY'] = 'SECRET_KEY'
```

## 🔮 Future Enhancements

- [ ] **Authentication System**: User accounts and payment history
- [ ] **Webhook Integration**: Real bank API integration
- [ ] **Payment Analytics**: Transaction reports and statistics
- [ ] **Mobile App**: React Native companion app
- [ ] **Multi-currency**: Support for different currencies
- [ ] **Recurring Payments**: Subscription payment support
- [ ] **Admin Dashboard**: Payment management interface
- [ ] **API Rate Limiting**: Request throttling and security
- [ ] **Email Notifications**: Payment confirmation emails
- [ ] **Advanced Security**: JWT tokens and OAuth integration

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

1. Check existing GitHub issues
2. Create new issue with detailed information
3. Provide payment logs and error messages
4. Include browser console output for WebSocket issues

## 🏆 Acknowledgments

- Flask community for excellent documentation
- PIX payment system specification
- QR code libraries and standards
- WebSocket real-time communication protocols
