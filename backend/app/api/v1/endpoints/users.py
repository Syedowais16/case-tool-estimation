"""User management API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.user_models import User, Role
from app.schemas.user_schemas import UserCreate, UserResponse, UserUpdate, UserWithRole, RoleCreate, RoleResponse
from app.core.security.security import get_password_hash, get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if email already exists
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new user
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        hashed_password=get_password_hash(user_data.password),
        role_id=user_data.role_id,
        phone=user_data.phone,
        organization=user_data.organization,
        department=user_data.department
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


# Role management endpoints

@router.post("/roles", response_model=RoleResponse)
async def create_role(role_data: RoleCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """Create new role"""
    if db.query(Role).filter(Role.name == role_data.name).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role already exists"
        )
    
    new_role = Role(**role_data.dict())
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    
    return new_role


@router.get("/roles/{role_id}", response_model=RoleResponse)
async def get_role(role_id: int, db: Session = Depends(get_db)):
    """Get role by ID"""
    role = db.query(Role).filter(Role.id == role_id).first()
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    
    return role


@router.get("/roles")
async def list_roles(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """List all roles"""
    total = db.query(Role).count()
    roles = db.query(Role).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": roles
    }


@router.get("/{user_id}", response_model=UserWithRole)
async def get_user(user_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """Get user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update user information"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Only allow users to update their own data or admins
    if int(current_user["user_id"]) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update other users"
        )
    
    update_data = user_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    return user


@router.get("")
async def list_users(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List all users (paginated)"""
    total = db.query(User).count()
    users = db.query(User).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": users
    }
