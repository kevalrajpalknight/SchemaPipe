import enum

from sqlalchemy import JSON, UUID, Column, Enum, ForeignKey, String
from sqlalchemy.orm import relationship

from src.core.database import Base
from src.core.models import TimeStampMixin, UUIDMixin
from src.core.utils import generate_hash


class PipelineStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"


class Accessibility(enum.Enum):
    PUBLIC = "public"
    PROTECTED = "protected"


class Pipeline(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = "pipelines"

    id = Column(UUID, primary_key=True, index=True)
    schema = Column(JSON, nullable=False)
    status = Column(
        Enum(PipelineStatus),
        default=PipelineStatus.INACTIVE,
    )
    accessibility = Column(
        Enum(Accessibility),
        default=Accessibility.PROTECTED,
    )
    secret_key = Column(String(length=100))
    short_code = Column(String(length=10), unique=True, index=True)
    created_by = Column(UUID, ForeignKey("users.id"), nullable=False, index=True)

    # relationships
    creator = relationship(
        "User",
        back_populates="pipelines",
        lazy="joined",
    )

    def check_access(self, key: str) -> bool:
        """Check if the provided key grants access to the pipeline."""
        if bool(self.accessibility == Accessibility.PUBLIC):
            return True
        hashed_key = generate_hash(key)
        return bool(hashed_key == self.secret_key)

    def set_secret_key(self, raw_key: str) -> None:
        """Generate hashed key and save to secret key."""
        self.secret_key = generate_hash(raw_key)

    @property
    def get_secret_key(self) -> str:
        """Get a masked version of the secret key."""
        return str(self.secret_key[:3] + "***" + self.secret_key[-3:])

    @property
    def show_secret_key(self) -> str:
        """Show the full secret key."""
        return str(self.secret_key)

    def __repr__(self) -> str:
        return f"<Pipeline(\
            id={self.id}, \
            status={self.status}, \
            accessibility={self.accessibility}, \
            created_by={self.created_by}) \
        >"

    def __str__(self):
        return f"Pipeline {self.id} created by User {self.created_by} \
        with Status {self.status} and Accessibility {self.accessibility}"
