import enum

from sqlalchemy import UUID, Column, Enum, Integer
from sqlalchemy.orm import relationship

from src.core.database import Base
from src.core.models import TimeStampMixin, UUIDMixin


class SubscriptionStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    CANCELED = "canceled"


class Subscription(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = "subscriptions"

    id = Column(UUID, primary_key=True, index=True)
    user_id = Column(UUID, nullable=False, index=True)
    credits = Column(Integer, default=0)
    credits_used = Column(Integer, default=0)
    status = Column(
        Enum(SubscriptionStatus),
        default=SubscriptionStatus.INACTIVE,
    )

    # relationships
    user = relationship(
        "User",
        back_populates="subscriptions",
        lazy="joined",
    )

    def __repr__(self):
        return f"<Subscription(\
            id={self.id}, \
            user_id={self.user_id}, \
            credits={self.credits}, \
            status={self.status}) \
        >"

    def __str__(self):
        return f"Subscription {self.id} for User {self.user_id} \
        with {self.credits} credits and Status {self.status}"
