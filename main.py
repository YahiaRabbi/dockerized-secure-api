from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
import jwt
from jwt.exceptions import InvalidTokenError
import json
import logging

from auth import verify_password, get_password_hash, create_access_token, SECRET_KEY, ALGORITHM
from database import get_db, User, Product, redis_client



# --- Configure Enterprise Logging (The CCTV Camera) ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Noorzaah Secure API Engine")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")



# --- Pydantic Models ---
class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class ProductCreate(BaseModel):
    name: str
    price_bdt: int




# --- Security Dependency ---
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user




# --- API Endpoints ---

@app.post("/api/v1/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pwd = get_password_hash(user.password)
    new_user = User(full_name=user.full_name, email=user.email, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    logger.info(f"New user registered: {user.email}")
    return {"message": "Account created successfully in PostgreSQL"}



@app.post("/api/v1/login", response_model=Token)
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        logger.warning(f"Failed login attempt for email: {user.email}")
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": user.email})
    logger.info(f"User logged in successfully: {user.email}")
    return {"access_token": access_token, "token_type": "bearer"}



@app.get("/api/v1/profile")
async def get_profile(current_user: User = Depends(get_current_user)):
    return {"message": f"Welcome back, {current_user.full_name}!", "email": current_user.email}



@app.post("/api/v1/products", status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Enterprise Trick: Adding a new product invalidates the old cache!"""
    new_product = Product(name=product.name, price_bdt=product.price_bdt)
    db.add(new_product)
    db.commit()
    
    # Cache Invalidation: Delete the old list from Redis so users see the new product
    redis_client.delete("noorzaah_products")
    logger.info(f"New product added: {product.name}. Cache Invalidated.")
    
    return {"message": f"Product '{product.name}' added successfully"}



@app.get("/api/v1/products")
async def get_products(db: Session = Depends(get_db)):
    """Fetches real products from DB and Caches them."""
    cached_products = redis_client.get("noorzaah_products")
    
    if cached_products:
        logger.info("⚡ Cache Hit: Served products from Redis RAM.")
        return {"source": "Redis Cache ⚡", "data": json.loads(cached_products)}
    
    logger.info("🗄️ Cache Miss: Querying PostgreSQL for products.")
    

    # Fetch from real Database instead of dummy dictionary
    products = db.query(Product).all()
    products_data = [{"id": p.id, "name": p.name, "price_bdt": p.price_bdt} for p in products]
    
    
    # Save to Redis for 60 seconds
    redis_client.setex("noorzaah_products", 60, json.dumps(products_data))
    return {"source": "PostgreSQL Database 🗄️", "data": products_data}