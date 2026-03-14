# Python FastAPI Application with PostgreSQL

A FastAPI application with user management, email services, and PostgreSQL database integration.

## Project Structure

```
.
├── auth/                 # Authentication module
├── database/             # Database connection
├── models/               # SQLAlchemy models
├── routers/              # API route handlers
├── schemas/              # Pydantic schemas
├── services/             # Business logic services
├── utils/                # Utility functions
├── main.py              # FastAPI application entry point
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker container configuration
├── Procfile             # Procfile for Railway
├── railway.json         # Railway configuration
├── .env.example         # Example environment variables
└── .env                 # Local environment variables (not committed)
```

## Prerequisites

- Python 3.11+
- PostgreSQL 12+
- Docker (optional)
- Railway account

## Local Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd Python-code
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your local configuration

5. **Run the application:**
   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at: `http://localhost:8000`
   API documentation: `http://localhost:8000/docs`

## Environment Variables

See `.env.example` for all available configuration options:

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `DEBUG` | Debug mode | `False` |
| `ALLOWED_ORIGINS` | CORS allowed origins (comma-separated) | `http://localhost:4200,https://yourdomain.com` |
| `SECRET_KEY` | Secret key for JWT tokens | Your secret key |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `30` |
| `EMAIL_HOST` | SMTP host | `smtp.gmail.com` |
| `EMAIL_PORT` | SMTP port | `587` |
| `EMAIL_USER` | Email address for sending | `your_email@gmail.com` |
| `EMAIL_PASSWORD` | Email password/app password | Your password |

## Railway Deployment

### Step 1: Push Code to Git

```bash
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

### Step 2: Create Railway Project

1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub"
4. Connect your GitHub account and select your repository

### Step 3: Add PostgreSQL Service

1. In your Railway project dashboard, click "Add Service"
2. Select "PostgreSQL"
3. Railway will automatically create a PostgreSQL instance

### Step 4: Configure Python Service

1. Railway will auto-detect the Python application
2. Go to the Python service settings
3. Set the **Start Command** to:
   ```
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

4. Under **Variables**, add the following environment variables:
   - `DATABASE_URL`: Railway will auto-populate from PostgreSQL service, or manually set it
   - `DEBUG`: `False`
   - `SECRET_KEY`: Generate a strong secret key
   - `ALLOWED_ORIGINS`: Your frontend URLs (comma-separated)
   - `EMAIL_USER`: Your email address
   - `EMAIL_PASSWORD`: Your email password
   - Any other variables from `.env.example`

### Step 5: Link PostgreSQL to Python Service

1. In your Python service, go to Variables
2. Click "Add Variable"
3. Set `DATABASE_URL` to the PostgreSQL connection string provided by Railway
4. Or link services directly through Railway's UI

### Step 6: Deploy

1. Click "Deploy" or wait for auto-deployment on push
2. Check the logs to ensure the application starts successfully
3. Visit the generated Railway domain to test

## Database Connection String Format

```
postgresql://username:password@host:port/database_name
```

**Railway Example (Auto-generated):**
```
postgresql://postgres:password@postgres.railway.internal:5432/railway
```

## API Usage

### Example: Create User

```bash
curl -X POST "http://localhost:8000/api/users" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "full_name": "John Doe"
  }'
```

## Docker Build & Run (Local Testing)

```bash
# Build image
docker build -t python-api:latest .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:pass@host:5432/db" \
  python-api:latest
```

## Troubleshooting

### PostgreSQL Connection Issues
- Verify `DATABASE_URL` is correct
- Ensure PostgreSQL is running (local) or accessible (Railway)
- Check firewall/network rules

### Port Already in Use
- Change `PORT` in `.env` to an available port
- Or kill the process using port 8000

### Import Errors
- Ensure all dependencies are in `requirements.txt`
- Reinstall: `pip install -r requirements.txt --force-reinstall`

### Railway Deployment Fails
- Check build logs in Railway dashboard
- Ensure `Procfile` and `Dockerfile` are correct
- Verify all environment variables are set

## Support

For more information:
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Railway Documentation](https://docs.railway.app)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**Last Updated:** March 2026
