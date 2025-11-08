# GitHub Profile Comparator

A complete end-to-end web application that allows users to compare two GitHub profiles side-by-side.

## Features

- 🔐 User Authentication (Signup, Login, Logout) with JWT tokens
- 📊 GitHub Profile Comparison
- 🎨 Modern, responsive UI with Tailwind CSS
- 🔒 Protected routes for authenticated users
- 📈 Detailed comparison metrics (repositories, stars, followers, languages, etc.)

## Tech Stack

### Backend
- Python FastAPI
- MongoDB
- JWT Authentication (PyJWT)
- Password Hashing (bcrypt)
- GitHub API Integration

### Frontend
- React 18
- React Router
- Tailwind CSS
- Axios
- Vite

## Prerequisites

- Python 3.8+
- Node.js 16+
- MongoDB (local or MongoDB Atlas)
- npm or yarn

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables (optional):
Create a `.env` file in the backend directory:
```
MONGO_URI=mongodb://localhost:27017/
SECRET_KEY=your-secret-key-change-in-production
```

5. Make sure MongoDB is running on your system.

6. Start the backend server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Usage

1. **Sign Up**: Create a new account by providing a username, email, and password.

2. **Log In**: Sign in with your email and password.

3. **Compare Profiles**: 
   - Enter two GitHub profile URLs in the dashboard
   - Click "Compare Profiles"
   - View the detailed comparison including:
     - Repository counts
     - Total stars
     - Followers
     - Most used languages
     - Top notable projects
     - Bio information

4. **Logout**: Click the logout button to sign out.

## API Endpoints

### Public Endpoints

- `POST /signup` - Create a new user account
- `POST /login` - Authenticate and receive JWT token

### Protected Endpoints

- `POST /compare` - Compare two GitHub profiles (requires JWT token)

## Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API service layer
│   │   ├── App.jsx          # Main app component
│   │   └── main.jsx         # Entry point
│   ├── package.json         # Node dependencies
│   └── vite.config.js       # Vite configuration
└── README.md
```

## Troubleshooting

### MongoDB Connection Issues

If you encounter MongoDB connection errors:

1. **Local MongoDB**: Make sure MongoDB is installed and running:
   - Windows: Check if MongoDB service is running in Services
   - Linux/Mac: Run `sudo systemctl start mongod` or `brew services start mongodb-community`

2. **MongoDB Atlas**: If using MongoDB Atlas (cloud), update the `MONGO_URI` in your `.env` file:
   ```
   MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
   ```

3. **Default Connection**: The app uses `mongodb://localhost:27017/` by default if no `MONGO_URI` is set.

### Backend Issues

- **Port Already in Use**: If port 8000 is already in use, you can change it in `main.py` or use: `uvicorn main:app --port 8001`
- **Import Errors**: Make sure all dependencies are installed: `pip install -r requirements.txt`
- **CORS Errors**: The backend is configured to allow requests from `localhost:3000` and `localhost:5173`. Update CORS settings in `main.py` if using a different port.

### Frontend Issues

- **Port Already in Use**: Vite will automatically try the next available port if 3000 is in use
- **API Connection Errors**: Make sure the backend is running on `http://localhost:8000`
- **Build Errors**: Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`

### GitHub API Issues

- **Rate Limiting**: GitHub API has rate limits. If you exceed them, wait a few minutes before trying again.
- **User Not Found**: Make sure the GitHub usernames are correct and the profiles are public.

## Notes

- The JWT token is stored in localStorage after login
- Protected routes automatically redirect to login if not authenticated
- The application uses GitHub's public API (no authentication required for public profiles)
- Make sure MongoDB is running before starting the backend server
- JWT tokens expire after 24 hours (configurable in `main.py`)

## Quick Start Checklist

- [ ] Install Python 3.8+ and Node.js 16+
- [ ] Install and start MongoDB
- [ ] Install backend dependencies: `cd backend && pip install -r requirements.txt`
- [ ] Install frontend dependencies: `cd frontend && npm install`
- [ ] Start backend: `cd backend && python main.py`
- [ ] Start frontend: `cd frontend && npm run dev`
- [ ] Open browser to `http://localhost:3000`

## License

MIT

