# Railway PostgreSQL Setup Guide

## 🔴 CRITICAL: Still Getting `postgres.railway.internal` Error?

This means your Railway Python service is using the **WRONG DATABASE_URL**.

### The Problem:
Railway auto-injects `DATABASE_URL` as an internal hostname (`postgres.railway.internal`) which only works within Railway's internal network. Your Docker container needs the **PUBLIC URL** to connect.

### ✅ IMMEDIATE FIX - 5 Steps:

#### Step 1: Get Your PostgreSQL Credentials
1. Open [railway.app](https://railway.app)
2. Go to your project
3. Click **PostgreSQL** service
4. Click **Data** tab
5. **Copy the entire Database URL** (it should be `postgresql://postgres:...@autorack.proxy.rlwy.net:...`)

#### Step 2: Go to Python Service Settings
1. Click **Python** service (or your API service)
2. Click **Variables** tab

#### Step 3: Set/Update DATABASE_URL
1. Look for `DATABASE_URL` variable
2. **Replace it completely** with the URL from Step 1
3. Click **Save** (not Save & Deploy yet)

#### Step 4: Verify Other Variables
Make sure these are also set correctly:
```
DATABASE_URL=postgresql://postgres:PASSWORD@autorack.proxy.rlwy.net:PORT/railway
DEBUG=False
SECRET_KEY=generate-a-random-string-here
ALLOWED_ORIGINS=https://your-domain.com
```

#### Step 5: Redeploy
1. Click **Redeploy** button
2. Wait for deployment to complete
3. Check logs for success

---

## Expected DATABASE URLs

### ❌ WRONG (Internal - Will NOT work)
```
postgresql://postgres:password@postgres.railway.internal:5432/railway
```

### ✅ CORRECT (Public - Will work)
```
postgresql://postgres:PASSWORD@autorack.proxy.rlwy.net:19017/railway
```

The key differences:
- Host: `autorack.proxy.rlwy.net` (Railway's public proxy)
- Port: Usually 19017 or custom port
- Uses secure external connection

---

## Debug Your Configuration

Run this locally to check your DATABASE_URL:
```bash
python debug_db_config.py
```

Output will tell you if the URL is correct.

---

## Why This Happens

When you create a PostgreSQL service in Railway:
1. Railway generates an **internal URL** for services within the same project
2. Railway also generates a **public URL** for external access
3. By default, Railway sets `DATABASE_URL` to the **internal URL**
4. Your Docker container needs the **public URL**

---

## Connection Pool Improvements

Your code now includes:
```python
pool_pre_ping=True       # Verify connection alive
pool_recycle=3600        # Recycle every hour
pool_size=5              # 5 connections in pool
max_overflow=10          # Up to 10 extra connections
connect_timeout=10       # 10 second timeout
```

---

## Troubleshooting Checklist

- [ ] DATABASE_URL uses `autorack.proxy.rlwy.net`
- [ ] DATABASE_URL does NOT contain `postgres.railway.internal`
- [ ] PASSWORD in URL is correct (from PostgreSQL service)
- [ ] PORT in URL is correct (usually 19017)
- [ ] DATABASE name is correct (usually `railway`)
- [ ] DEBUG is set to `False` (for production)
- [ ] SECRET_KEY is set to a random string
- [ ] Python service has been redeployed after changing variables

---

## Still Not Working?

1. **Check Railway logs:**
   - Python service → Logs tab
   - Look for exact error message

2. **Test locally:**
   ```bash
   psql "your-database-url"
   ```

3. **Verify PostgreSQL is running:**
   - PostgreSQL service → Status should be "Running"

4. **Check if DB exists:**
   - PostgreSQL service → Data tab → Verify database name

---

For more help: [Railway PostgreSQL Docs](https://docs.railway.app/databases/postgresql)
