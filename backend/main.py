from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pymongo import MongoClient
import bcrypt
import jwt
import httpx
import os
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel, EmailStr, HttpUrl

app = FastAPI(title="GitHub Profile Comparator API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DATABASE_NAME = "github_comparator"
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
users_collection = db["users"]

# JWT configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

security = HTTPBearer()


# Pydantic models
class UserSignup(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class CompareRequest(BaseModel):
    url1: HttpUrl
    url2: HttpUrl


# Helper functions
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    
    user = users_collection.find_one({"email": email})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user


def extract_username_from_url(url: str) -> str:
    """Extract GitHub username from URL."""
    url = url.rstrip("/")
    if "github.com/" in url:
        parts = url.split("github.com/")[-1]
        username = parts.split("/")[0]
        return username
    return url


async def fetch_github_user_data(username: str):
    """Fetch user data from GitHub API."""
    async with httpx.AsyncClient() as client:
        try:
            # Fetch user info
            user_response = await client.get(
                f"https://api.github.com/users/{username}",
                headers={"Accept": "application/vnd.github.v3+json"},
                timeout=10.0
            )
            if user_response.status_code != 200:
                raise HTTPException(
                    status_code=404,
                    detail=f"GitHub user '{username}' not found"
                )
            user_data = user_response.json()
            
            # Fetch repositories
            repos_response = await client.get(
                f"https://api.github.com/users/{username}/repos",
                headers={"Accept": "application/vnd.github.v3+json"},
                params={"per_page": 100, "sort": "updated"},
                timeout=10.0
            )
            repos_data = repos_response.json() if repos_response.status_code == 200 else []
            
            return user_data, repos_data
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="GitHub API timeout")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching GitHub data: {str(e)}")


def analyze_user_data(user_data: dict, repos_data: list) -> dict:
    """Analyze GitHub user data and extract metrics."""
    # Count total repos
    total_repos = len(repos_data)
    
    # Calculate total stars
    total_stars = sum(repo.get("stargazers_count", 0) for repo in repos_data)
    
    # Analyze languages
    language_count = {}
    for repo in repos_data:
        lang = repo.get("language")
        if lang:
            language_count[lang] = language_count.get(lang, 0) + 1
    
    # Sort languages by usage
    most_used_languages = sorted(
        language_count.items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]
    
    # Get top projects by stars
    top_projects = sorted(
        repos_data,
        key=lambda x: x.get("stargazers_count", 0),
        reverse=True
    )[:5]
    
    notable_projects = [
        {
            "name": repo.get("name"),
            "stars": repo.get("stargazers_count", 0),
            "description": repo.get("description") or "No description",
            "url": repo.get("html_url")
        }
        for repo in top_projects
    ]
    
    return {
        "username": user_data.get("login"),
        "name": user_data.get("name") or user_data.get("login"),
        "bio": user_data.get("bio") or "No bio",
        "followers": user_data.get("followers", 0),
        "following": user_data.get("following", 0),
        "total_repos": total_repos,
        "total_stars": total_stars,
        "most_used_languages": most_used_languages,
        "notable_projects": notable_projects,
        "avatar_url": user_data.get("avatar_url"),
        "created_at": user_data.get("created_at"),
    }


def generate_comparison_text(user1_data: dict, user2_data: dict) -> str:
    """Generate human-readable comparison text."""
    comparison = f"""
# GitHub Profile Comparison

## {user1_data['name']} vs {user2_data['name']}

### Profile Overview
- **{user1_data['name']}**: {user1_data['followers']} followers, {user1_data['following']} following, {user1_data['total_repos']} repositories
- **{user2_data['name']}**: {user2_data['followers']} followers, {user2_data['following']} following, {user2_data['total_repos']} repositories

### Repository Count
- **{user1_data['name']}**: {user1_data['total_repos']} repositories
- **{user2_data['name']}**: {user2_data['total_repos']} repositories
- **Winner**: {user1_data['name'] if user1_data['total_repos'] > user2_data['total_repos'] else user2_data['name'] if user2_data['total_repos'] > user1_data['total_repos'] else 'Tie'}

### Total Stars
- **{user1_data['name']}**: {user1_data['total_stars']} stars
- **{user2_data['name']}**: {user2_data['total_stars']} stars
- **Winner**: {user1_data['name'] if user1_data['total_stars'] > user2_data['total_stars'] else user2_data['name'] if user2_data['total_stars'] > user1_data['total_stars'] else 'Tie'}

### Followers
- **{user1_data['name']}**: {user1_data['followers']} followers
- **{user2_data['name']}**: {user2_data['followers']} followers
- **Winner**: {user1_data['name'] if user1_data['followers'] > user2_data['followers'] else user2_data['name'] if user2_data['followers'] > user1_data['followers'] else 'Tie'}

### Most Used Languages

**{user1_data['name']}:**
"""
    
    if user1_data['most_used_languages']:
        for lang, count in user1_data['most_used_languages']:
            comparison += f"- {lang}: {count} repositories\n"
    else:
        comparison += "- No languages detected\n"
    
    comparison += f"\n**{user2_data['name']}:**\n"
    
    if user2_data['most_used_languages']:
        for lang, count in user2_data['most_used_languages']:
            comparison += f"- {lang}: {count} repositories\n"
    else:
        comparison += "- No languages detected\n"
    
    comparison += f"\n### Notable Projects\n\n**{user1_data['name']}'s Top Projects:**\n"
    for project in user1_data['notable_projects']:
        comparison += f"- **{project['name']}** ({project['stars']} stars): {project['description']}\n"
    
    comparison += f"\n**{user2_data['name']}'s Top Projects:**\n"
    for project in user2_data['notable_projects']:
        comparison += f"- **{project['name']}** ({project['stars']} stars): {project['description']}\n"
    
    comparison += f"\n### Bio\n- **{user1_data['name']}**: {user1_data['bio']}\n- **{user2_data['name']}**: {user2_data['bio']}\n"
    
    return comparison.strip()


# Routes
@app.get("/")
def root():
    return {"message": "GitHub Profile Comparator API"}


@app.post("/signup")
async def signup(user_data: UserSignup):
    """Create a new user account."""
    # Check if user already exists
    existing_user = users_collection.find_one({"$or": [{"email": user_data.email}, {"username": user_data.username}]})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists"
        )
    
    # Hash password
    hashed_password = hash_password(user_data.password)
    
    # Create user document
    user_doc = {
        "username": user_data.username,
        "email": user_data.email,
        "password": hashed_password,
        "created_at": datetime.utcnow().isoformat()
    }
    
    try:
        users_collection.insert_one(user_doc)
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )


@app.post("/login")
async def login(credentials: UserLogin):
    """Authenticate user and return JWT token."""
    user = users_collection.find_one({"email": credentials.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not verify_password(credentials.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "username": user["username"],
            "email": user["email"]
        }
    }


@app.post("/compare")
async def compare_profiles(
    compare_request: CompareRequest,
    current_user: dict = Depends(get_current_user)
):
    """Compare two GitHub profiles."""
    # Extract usernames from URLs
    username1 = extract_username_from_url(str(compare_request.url1))
    username2 = extract_username_from_url(str(compare_request.url2))
    
    if username1 == username2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot compare the same user"
        )
    
    # Fetch data for both users
    user1_data, user1_repos = await fetch_github_user_data(username1)
    user2_data, user2_repos = await fetch_github_user_data(username2)
    
    # Analyze data
    analyzed_user1 = analyze_user_data(user1_data, user1_repos)
    analyzed_user2 = analyze_user_data(user2_data, user2_repos)
    
    # Generate comparison text
    comparison_text = generate_comparison_text(analyzed_user1, analyzed_user2)
    
    return {
        "comparison_text": comparison_text,
        "user1": analyzed_user1,
        "user2": analyzed_user2
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

