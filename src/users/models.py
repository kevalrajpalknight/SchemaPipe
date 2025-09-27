import enum

from sqlalchemy import UUID, Column, Enum, String
from sqlalchemy.orm import relationship

from src.core.database import Base
from src.core.models import TimeStampMixin, UUIDMixin
from src.core.utils import generate_hash


class UserRole(enum.Enum):
    ADMIN = "admin"
    USER = "user"


class UserStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BANNED = "banned"


class User(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String(length=64), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER)
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE)

    # relationships
    pipelines = relationship(
        "Pipeline",
        back_populates="creator",
        lazy="dynamic",
    )
    subscriptions = relationship(
        "Subscription",
        back_populates="user",
        lazy="dynamic",
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, \
            email={self.email}, \
            full_name={self.full_name}, \
            role={self.role})>\
        "

    def __str__(self) -> str:
        return f"User {self.full_name} ({self.email})"

    @property
    def is_admin(self) -> bool:
        return bool(self.role == UserRole.ADMIN)

    @property
    def is_user(self) -> bool:
        return bool(self.role == UserRole.USER)

    def set_password(self, raw_password: str) -> None:
        self.hashed_password = generate_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return bool(self.hashed_password == generate_hash(raw_password))

    @property
    def is_active(self) -> bool:
        return bool(self.status == UserStatus.ACTIVE)
