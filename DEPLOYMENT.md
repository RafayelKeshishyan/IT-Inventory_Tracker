# Deployment Guide - IT Inventory Tracker on Vercel

This guide will help you deploy your full-stack IT Inventory Tracker to Vercel with PostgreSQL.

## Prerequisites

- [Vercel Account](https://vercel.com/signup) (free)
- [GitHub Account](https://github.com) (to connect your repo)
- Git installed locally

## Step 1: Push to GitHub

1. **Initialize git (if not already done):**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - ready for Vercel deployment"
   ```

2. **Create a new repository on GitHub:**
   - Go to https://github.com/new
   - Name it: `inventory-tracker`
   - Don't initialize with README (you already have one)
   - Click "Create repository"

3. **Push your code:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/inventory-tracker.git
   git branch -M main
   git push -u origin main
   ```

## Step 2: Set Up Vercel Postgres

1. **Go to Vercel Dashboard:**
   - Visit https://vercel.com/dashboard
   - Click on "Storage" tab
   - Click "Create Database"

2. **Create PostgreSQL Database:**
   - Select "Postgres"
   - Choose a name: `inventory-tracker-db`
   - Select region closest to you
   - Click "Create"

3. **Note your connection string:**
   - After creation, click on your database
   - Go to ".env.local" tab
   - You'll see `POSTGRES_URL` - this will be automatically added to your project

## Step 3: Deploy to Vercel

1. **Import Project:**
   - Go to https://vercel.com/new
   - Click "Import Git Repository"
   - Select your `inventory-tracker` repository
   - Click "Import"

2. **Configure Project:**
   - **Framework Preset:** Vite
   - **Root Directory:** `./` (leave as default)
   - **Build Command:** `cd frontend && npm run build`
   - **Output Directory:** `frontend/dist`
   - **Install Command:** `npm install` (in root)

3. **Environment Variables:**
   Click "Environment Variables" and add:
   
   **For Production:**
   - Key: `VITE_API_URL`
   - Value: `/api`
   - Environment: Production

4. **Connect Database:**
   - In the same deployment screen, scroll down to "Storage"
   - Click "Connect Store"
   - Select your `inventory-tracker-db` PostgreSQL database
   - Click "Connect"
   - This automatically adds `POSTGRES_URL` environment variable

5. **Deploy:**
   - Click "Deploy"
   - Wait 2-3 minutes for deployment to complete

## Step 4: Initialize Database

After first deployment, you need to create the database tables:

1. **Go to your Vercel project dashboard**
2. **Click on "Storage" tab**
3. **Click on your database**
4. **Click "Query" tab**
5. **Run this SQL to create tables:**

```sql
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL CHECK (type IN ('device', 'part')),
    location VARCHAR(255),
    status VARCHAR(50) NOT NULL CHECK (status IN ('available', 'in_use', 'broken', 'checked_out')),
    quantity INTEGER DEFAULT 1,
    low_stock_threshold INTEGER DEFAULT 5,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_items_type ON items(type);
CREATE INDEX idx_items_status ON items(status);
CREATE INDEX idx_items_location ON items(location);
```

6. **Optional: Add sample data**

You can run the seed data by creating a one-time script, or manually add items through your UI after deployment.

## Step 5: Test Your Deployment

1. **Visit your deployed URL** (e.g., `https://inventory-tracker.vercel.app`)
2. **Test the dashboard** - should load with 0 items
3. **Add a test item** - click "Add Item" button
4. **Verify CRUD operations:**
   - Create an item ✓
   - Edit the item ✓
   - Delete the item ✓
   - Search/filter ✓

## Local Development Setup

To continue developing locally:

1. **Install dependencies:**
   ```bash
   # Backend
   cd backend
   pip install -r requirements.txt
   
   # Frontend
   cd ../frontend
   npm install
   ```

2. **Create `.env` file in frontend folder:**
   ```bash
   cd frontend
   echo "VITE_API_URL=http://localhost:8000/api" > .env
   ```

3. **Run locally (2 terminals):**
   
   **Terminal 1 - Backend:**
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```
   
   **Terminal 2 - Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

4. **Visit:** http://localhost:5173

## Troubleshooting

### Issue: API calls failing with CORS errors
**Solution:** Check that `VITE_API_URL` is set correctly:
- Local: `http://localhost:8000/api`
- Production: `/api`

### Issue: Database connection errors
**Solution:** 
- Verify `POSTGRES_URL` is set in Vercel environment variables
- Check database is in the same region as your deployment
- Verify tables are created (Step 4)

### Issue: Build failing
**Solution:**
- Check build logs in Vercel dashboard
- Make sure all dependencies are in `package.json` and `requirements.txt`
- Verify Python version is compatible (Vercel uses Python 3.9+)

### Issue: 404 errors on API routes
**Solution:**
- Verify `vercel.json` routes are correct
- Check `api/index.py` exists
- Redeploy project

## Continuous Deployment

Once set up, Vercel automatically:
- ✅ Deploys on every push to `main` branch
- ✅ Creates preview deployments for pull requests
- ✅ Provides automatic HTTPS
- ✅ Global CDN for fast loading

## Updating Your Deployment

To push updates:

```bash
git add .
git commit -m "Your update message"
git push
```

Vercel will automatically rebuild and deploy!

## Environment Variables Reference

| Variable | Local Value | Production Value | Purpose |
|----------|-------------|------------------|---------|
| `VITE_API_URL` | `http://localhost:8000/api` | `/api` | Frontend API endpoint |
| `POSTGRES_URL` | (SQLite) | Auto-set by Vercel | Database connection |

## Cost

✅ **Everything is FREE on Vercel:**
- Unlimited deployments
- Vercel Postgres free tier: 256MB storage, 60 compute hours/month
- Perfect for portfolio projects and demos

## Next Steps

1. ✅ Add custom domain (optional): Project Settings → Domains
2. ✅ Monitor usage: Dashboard → Analytics
3. ✅ Set up staging environment: Create a `develop` branch
4. ✅ Add environment protection: Project Settings → Environment Variables

---

## Questions or Issues?

- Vercel Docs: https://vercel.com/docs
- Vercel Postgres: https://vercel.com/docs/storage/vercel-postgres
- FastAPI on Vercel: https://vercel.com/docs/functions/runtimes/python

Your app is now live! 🚀
