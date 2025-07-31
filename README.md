# Store - Modern E-commerce Platform

A full-stack e-commerce application built with FastAPI, Vue 3, and modern development practices.

## Project Structure

This is a monorepo containing both backend and frontend applications:

```
store/
├── store-backend/          # FastAPI backend application
│   ├── app/               # Main application code
│   │   ├── api/          # API routes and endpoints
│   │   ├── core/         # Core configurations
│   │   ├── db/           # Database connections
│   │   ├── models/       # SQLModel table models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── services/     # Business logic layer
│   ├── tests/            # Test files
│   └── requirements.txt  # Python dependencies
├── store-frontend/         # Vue 3 frontend application
│   ├── src/              # Source code
│   │   ├── components/   # Reusable Vue components
│   │   ├── views/        # Page views
│   │   ├── stores/       # Pinia state management
│   │   └── services/     # API client services
│   └── package.json      # Node.js dependencies
└── docker-compose.yml     # Container orchestration
```

## Features

### Backend (FastAPI)
- **Modern Python API** with FastAPI and async/await
- **SQLModel Integration** for type-safe database operations
- **Stripe Payment Processing** for secure transactions
- **Email Notifications** via Gmail API
- **AI Integration** with Google Gemini API
- **Comprehensive Testing** with pytest
- **API Documentation** with OpenAPI/Swagger

### Frontend (Vue 3)
- **Modern Vue 3** with Composition API
- **State Management** with Pinia
- **AI Assistant** component for customer support
- **Responsive Design** with mobile-first approach
- **Real-time Updates** and notifications
- **Stripe Checkout** integration
- **TypeScript Support** for type safety

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Environment Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd store
   ```

2. **Set up environment variables:**
   ```bash
   # Copy example environment files
   cp .env.example .env
   cp store-backend/.env.example store-backend/.env
   cp store-frontend/.env.example store-frontend/.env
   ```

3. **Configure your environment variables:**
   
   Edit the `.env` files with your actual values. See the Environment Variables section below for details.

### Running with Docker

**Start the entire application stack:**
```bash
docker-compose up --build
```

This will start:
- **Database**: PostgreSQL on port 5432
- **Backend**: FastAPI on port 8000
- **Frontend**: Vue 3 app on port 5173

### Access the Applications

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Environment Variables

### Required Environment Variables

| Variable | Scope | Description |
|----------|-------|-------------|
| `DATABASE_URL` | Backend | PostgreSQL connection string |
| `STRIPE_API_KEY` | Backend | Stripe secret key |
| `STRIPE_WEBHOOK_SECRET` | Backend | Stripe webhook endpoint secret |
| `STRIPE_PRICE_ID` | Backend | Stripe product price ID |
| `FRONTEND_URL` | Backend | Frontend URL for CORS and redirects |
| `GMAIL_CREDENTIALS_JSON` | Backend | Google OAuth2 credentials |
| `EMAIL_SENDER` | Backend | Email address for notifications |
| `GEMINI_API_KEY` | Backend | Google Gemini API key |
| `VITE_API_BASE_URL` | Frontend | Backend API base URL |
| `VITE_FIREBASE_*` | Frontend | Firebase configuration |

### Getting API Keys

1. **Stripe**: Get your API keys from [Stripe Dashboard](https://dashboard.stripe.com/apikeys)
2. **Google Gemini**: Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
3. **Gmail API**: Set up OAuth2 credentials in [Google Cloud Console](https://console.cloud.google.com/)
4. **Firebase**: Get configuration from [Firebase Console](https://console.firebase.google.com/)

## Development

### Backend Development
```bash
cd store-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Development
```bash
cd store-frontend
npm install
npm run dev
```

### Running Tests
```bash
# Backend tests
cd store-backend
pytest

# Frontend tests (when added)
cd store-frontend
npm run test
```

## Architecture

This project follows modern software architecture principles:

- **Domain-Driven Design**: Clear separation of business logic
- **Clean Architecture**: Dependency inversion and separation of concerns
- **Microservices Ready**: Modular design for easy scaling
- **CI/CD Friendly**: Docker containers and automated testing
- **Security First**: Environment-based configuration and secure defaults

## Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLModel** - Type-safe database operations
- **PostgreSQL** - Reliable database
- **Stripe** - Payment processing
- **Google Gemini** - AI integration
- **Gmail API** - Email notifications

### Frontend
- **Vue 3** - Progressive JavaScript framework
- **Pinia** - State management
- **Vite** - Fast build tool
- **TypeScript** - Type safety

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Local development orchestration
- **PostgreSQL** - Database

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.