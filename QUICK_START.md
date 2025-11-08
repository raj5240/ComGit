# Quick Start Guide - GitHub Profile Comparator

## Prerequisites Checklist

Before starting, ensure you have:
- ✅ Python 3.8 or higher installed
- ✅ Node.js 16 or higher installed
- ✅ MongoDB installed and running (local) OR MongoDB Atlas account (cloud)
- ✅ npm or yarn package manager

## Step-by-Step Setup

### Step 1: Set Up MongoDB

**Option A: Local MongoDB**
- Install MongoDB from [mongodb.com](https://www.mongodb.com/try/download/community)
- Start MongoDB service:
  - **Windows**: MongoDB should start automatically as a service, or run `net start MongoDB`
  - **Linux**: `sudo systemctl start mongod`
  - **Mac**: `brew services start mongodb-community`

**Option B: MongoDB Atlas (Cloud)**
- Create a free account at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
- Create a cluster and get your connection string
- Note the connection string for Step 3

### Step 2: Set Up Backend

1. **Open a terminal/command prompt** and navigate to the backend directory:
   ```bash
   cd backend
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables** (optional):
   - Create a `.env` file in the `backend` directory
   - Add the following (modify if using MongoDB Atlas):
     ```
     MONGO_URI=mongodb://localhost:27017/
     SECRET_KEY=your-secret-key-change-in-production
     ```
   - **If using MongoDB Atlas**, replace `MONGO_URI` with your Atlas connection string

5. **Start the backend server**:
   ```bash
   python main.py
   ```
   
   You should see:
   ```
   INFO:     Started server process
   INFO:     Uvicorn running on http://0.0.0.0:8000
   ```

   **Keep this terminal open!** The backend must be running.

### Step 3: Set Up Frontend

1. **Open a NEW terminal/command prompt** (keep backend running)

2. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

3. **Install Node.js dependencies**:
   ```bash
   npm install
   ```
   
   This may take a few minutes on first run.

4. **Start the frontend development server**:
   ```bash
   npm run dev
   ```
   
   You should see:
   ```
   VITE v5.x.x  ready in xxx ms
   ➜  Local:   http://localhost:3000/
   ```

### Step 4: Access the Application

1. **Open your web browser** and navigate to:
   ```
   http://localhost:3000
   ```

2. **Sign up** for a new account:
   - Enter a username, email, and password
   - Click "Sign Up"
   - You'll be redirected to the login page

3. **Log in** with your credentials:
   - Enter your email and password
   - Click "Log In"
   - You'll be redirected to the dashboard

4. **Compare GitHub profiles**:
   - Enter two GitHub profile URLs (e.g., `https://github.com/octocat` and `https://github.com/torvalds`)
   - Click "Compare Profiles"
   - View the detailed comparison results!

## Running the Project (After Initial Setup)

Once everything is set up, you only need to:

1. **Start MongoDB** (if using local MongoDB)

2. **Start Backend** (in one terminal):
   ```bash
   cd backend
   # Activate virtual environment if not already active
   # Windows: venv\Scripts\activate
   # Linux/Mac: source venv/bin/activate
   python main.py
   ```

3. **Start Frontend** (in another terminal):
   ```bash
   cd frontend
   npm run dev
   ```

4. **Open browser** to `http://localhost:3000`

## Troubleshooting

### Backend won't start
- **MongoDB not running**: Make sure MongoDB is running on your system
- **Port 8000 in use**: Change the port in `main.py` or stop the process using port 8000
- **Import errors**: Make sure you activated the virtual environment and installed dependencies

### Frontend won't start
- **Port 3000 in use**: Vite will automatically use the next available port
- **npm install fails**: Try deleting `node_modules` and `package-lock.json`, then run `npm install` again
- **API connection errors**: Make sure the backend is running on `http://localhost:8000`

### Can't connect to MongoDB
- **Local MongoDB**: Check if the service is running: `mongosh` or `mongo` should connect
- **MongoDB Atlas**: Verify your connection string in the `.env` file
- **Firewall issues**: Make sure port 27017 is open (for local MongoDB)

### GitHub API errors
- **Rate limiting**: GitHub has rate limits. Wait a few minutes and try again
- **User not found**: Verify the GitHub usernames are correct and profiles are public

## Quick Commands Reference

```bash
# Backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python main.py

# Frontend
cd frontend
npm install
npm run dev
```

## Need Help?

- Check the main [README.md](README.md) for detailed documentation
- Verify all prerequisites are installed
- Check that MongoDB is running
- Ensure both backend and frontend servers are running simultaneously

