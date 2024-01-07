from app.repositories.user_repository import UserRepository
from app.models.user import User, BaseModel
from app.database import MongoDB
from jose import jwt, JWTError
import uuid
from fastapi import HTTPException, status, Depends
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer
from app.models.authentication import authentication_response
from passlib.context import CryptContext
from typing import Annotated
from datetime import datetime, timedelta

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    access_token: str
    token_type: str

def verify_password(plain_password, hashed_password):
    """
    Verify if a received password matches the stored hash.

    Args:
        plain_password (str): The plain password to be verified.
        hashed_password (str): The hashed password stored.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Hash a password.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)

class UserService:
    def __init__(self, mongo_db: MongoDB):
        """
        Initialize the UserService.

        Args:
            mongo_db (MongoDB): The MongoDB instance.
        """
        self.user_repository = UserRepository(mongo_db)
        self.secret_key = os.getenv("SECRET_KEY")
        self.algorithm = os.getenv("ALGORITHM")

    def create_user(self, user_data: User):
        """
        Create a user instance and return the user's ID.

        Args:
            user_data (User): The user data.

        Raises:
            HTTPException: If the user already exists.

        Returns:
            str: The ID of the created user.
        """
        user = self.user_repository.get_user_by_email(user_data.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User Already Exist")
        user_data.password = get_password_hash(user_data.password)
        user_uuid = str(uuid.uuid4())
        user_data.uuid = user_uuid
        return self.user_repository.create_user(user_data)

    def get_user(self, email):
        """
        Get a user instance by email.

        Args:
            email (str): The email of the user.

        Raises:
            HTTPException: If the user is not found.

        Returns:
            User: The user instance.
        """
        user = self.user_repository.get_user_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
        return user

    def authenticate_user(self, email: str, password: str):
        """
        Authenticate a user based on email and password.

        Args:
            email (str): The email of the user.
            password (str): The user's password.

        Returns:
            Union[User, bool]: The user instance if authentication succeeds, False otherwise.
        """
        user = self.get_user(email)
        if not user:
            return False
        if not verify_password(password, user['password']):
            return False
        return user

    def get_users(self):
        """
        Get a list of all users.

        Returns:
            List[User]: The list of all users.
        """
        return self.user_repository.get_users()

    def create_access_token(self, data: dict, expires_delta: timedelta):
        """
        Create a new access token.

        Args:
            data (dict): The data to be encoded in the token.
            expires_delta (timedelta): The expiration time for the token.

        Returns:
            str: The encoded JWT token.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def get_user_by_uuid(self, uuid: str) -> User:
        """
        Get a user by UUID.

        Args:
            uuid (str): The UUID of the user.

        Raises:
            HTTPException: If the user is not found.

        Returns:
            User: The user instance.
        """
        user_data = self.user_repository.get_user_by_uuid(uuid)
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return User(**user_data)

    async def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]):
        """
        Get the current user based on the provided JWT token.

        Args:
            token (str): The JWT token.

        Raises:
            HTTPException: If the credentials are invalid.

        Returns:
            User: The current user.
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = self.get_user(email=username)
        if user is None:
            raise credentials_exception
        return user

    async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)]):
        """
        Get the current active user.

        Args:
            current_user (User): The current user instance.

        Raises:
            HTTPException: If the user is inactive.

        Returns:
            User: The current active user.
        """
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
