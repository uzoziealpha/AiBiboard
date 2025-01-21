# backend/app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm  # Add this import
from sqlalchemy.orm import Session
from typing import Dict
import logging
from ..models.database import get_db
from ..models.user import User
from ..schemas.user import UserCreate, UserResponse
from ..services.auth import create_access_token, get_password_hash, verify_password

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        logger.debug(f"Attempting to create user with email: {user_data.email}")

        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            logger.warning(f"User already exists: {user_data.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create new user
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        logger.info(f"User created successfully: {user_data.email}")

        # Create access token
        access_token = create_access_token(data={"sub": db_user.email})

        return {
            "id": db_user.id,
            "email": db_user.email,
            "full_name": db_user.full_name,
            "access_token": access_token,
            "token_type": "bearer"
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Dict:
    try:
        logger.debug(f"Attempting login for user: {form_data.username}")

        user = db.query(User).filter(User.email == form_data.username).first()
        if not user:
            logger.warning(f"User not found: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        if not verify_password(form_data.password, user.hashed_password):
            logger.warning(f"Invalid password for user: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        access_token = create_access_token(data={"sub": user.email})

        logger.info(f"Login successful for user: {form_data.username}")
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name
            }
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

# Add a JSON-based login endpoint
@router.post("/login/json")
async def login_json(
    email: str,
    password: str,
    db: Session = Depends(get_db)
) -> Dict:
    try:
        logger.debug(f"Attempting JSON login for user: {email}")

        user = db.query(User).filter(User.email == email).first()
        if not user:
            logger.warning(f"User not found: {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        if not verify_password(password, user.hashed_password):
            logger.warning(f"Invalid password for user: {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        access_token = create_access_token(data={"sub": user.email})

        logger.info(f"JSON login successful for user: {email}")
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name
            }
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"JSON login error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )