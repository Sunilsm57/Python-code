# Railway PostgreSQL Setup Guide

## Issue: `postgres.railway.internal` Connection Error

This error occurs when the Python service cannot connect to the PostgreSQL service because:
1. The `DATABASE_URL` environment variable is not properly configured
2. The hostname is incorrect or not accessible

## Step-by-Step Fix:

### 1. Get Correct Database URL from Railway

**Go to Railway Dashboard:**
- Open [railway.app](https://railway.app)
- Open your project
- Click on your **PostgreSQL** service
- Go to "Data" tab
- Copy the **DATABASE_PUBLIC_URL** or the connection string

It should look like:
```
postgresql://postgres:PASSWORD@autorack.proxy.rlwy.net:PORT/railway
```

### 2. Set DATABASE_URL in Python Service

**In your Python service:**
1. Click **Variables** tab
2. Find or create `DATABASE_URL` variable
3. Paste the full PostgreSQL connection string
4. Click **Save**

### 3. Verify Other Environment Variables

Make sure these are also set:
```
DATABASE_URL=postgresql://username:password@host:port/database
DEBUG=False
SECRET_KEY=your-random-secret-key
ALLOWED_ORIGINS=https://your-frontend-domain.com
```

### 4. Deploy

Click **Redeploy** or push new code to trigger deployment.

## Expected DATABASE_URL Format

```
postgresql://postgres:{PASSWORD}@{HOST}:{PORT}/{DATABASE}
```

**Railway Example:**
```
postgresql://postgres:zzIQdiQoTkiRQPKYmwAGBaoXWqNuJjHq@autorack.proxy.rlwy.net:19017/railway
```

## Connection Pool Settings

The updated `connection.py` now includes:
- `pool_pre_ping=True` - Verifies connection is alive before using
- `pool_recycle=3600` - Recycles connections every hour (prevents stale connections)
- `expire_on_commit=False` - Better session management

## Troubleshooting

### Still getting connection errors?

1. **Check if PostgreSQL service is running:**
   - Go to PostgreSQL service in Railway
   - Verify status is "Running"

2. **Verify DATABASE_URL format:**
   - Ensure no typos in credentials
   - Verify PORT is correct (usually 5432 for public, custom for Railway proxy)
   - Confirm database name exists

3. **Check logs:**
   - In your Python service, check the deployment logs
   - Look for the exact connection error

4. **Test connection locally:**
   ```bash
   psql "your-database-url"
   ```

### If using Internal Network:

If Railway services are in the same project and you need to use internal hostname:
```
postgresql://postgres:password@postgres.railway.internal:5432/railway
```
(Only works for internal Railway networking)

---

For more help, see [Railway PostgreSQL Documentation](https://docs.railway.app/databases/postgresql)
