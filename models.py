
from datetime import datetime, timezone

from extensions import db
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(
        db.String(50),
        primary_key=True,
        default=lambda: str(uuid4())
    )    
    username = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    @classmethod
    def get_user_by_username(cls,username):
        return cls.query.filter_by(username=username).first()
    def save(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()


class TokenBlocklist(db.Model):
    __tablename__ = 'token_blocklist'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now
    )
    def __repr__(self): 
        return f'<TokenBlocklist {self.jti}>'
    def save(self):
        db.session.add(self)
        db.session.commit()


class ExplorationHistory(db.Model):
    __tablename__ = "exploration_history"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.String(36),
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    content_type = db.Column(
        db.String(30),
        nullable=False
    )

    content_id = db.Column(
        db.String(100),
        nullable=False
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    image_url = db.Column(
        db.Text,
        nullable=True
    )

    route = db.Column(
        db.String(500),
        nullable=False
    )

    last_viewed_at = db.Column(
    db.DateTime,
    default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
    nullable=False
    )

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "content_type",
            "content_id",
            name="unique_user_exploration"
        ),
    )

    def __repr__(self):
        return f"<ExplorationHistory {self.title}>"