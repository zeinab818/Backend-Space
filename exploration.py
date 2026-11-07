from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from datetime import datetime, timezone

from extensions import db
from models import ExplorationHistory

exploration_bp = Blueprint(
    "exploration",
    __name__
)

ALLOWED_TYPES = {
    "planet",
    "moon",
    "mission",
    "discovery",
    "article",
    "apod",
    "nasa_image",
    "astronomy_event",

    "iss",
    "space_station",
    "quran_verse",
    "quran_article",
    "constellation",
    "star",
    "galaxy"
}

def format_datetime(value):
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)

    return value.astimezone(timezone.utc).isoformat()

@exploration_bp.post("/track")
@jwt_required()
def track_exploration():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "message": "Invalid request body"
        }), 400

    content_type = data.get("content_type")
    content_id = data.get("content_id")
    title = data.get("title")
    route = data.get("route")
    image_url = data.get("image_url")
    # Validate content type
    if not isinstance(content_type, str) or content_type not in ALLOWED_TYPES:
        return jsonify({
            "message": "Invalid content type"
        }), 400

    # Validate content ID
    if not isinstance(content_id, (str, int)) or isinstance(content_id, bool):
        return jsonify({
            "message": "Invalid content ID"
        }), 400

    content_id = str(content_id).strip()

    if not content_id or len(content_id) > 100:
        return jsonify({
            "message": "Invalid content ID"
        }), 400

    # Validate title
    if not isinstance(title, str) or not title.strip() or len(title) > 200:
        return jsonify({
            "message": "Invalid title"
        }), 400

    title = title.strip()

    # Validate route
    if (
        not isinstance(route, str)
        or not route.startswith("/")
        or route.startswith("//")
        or len(route) > 500
    ):
        return jsonify({
            "message": "Invalid route"
        }), 400

    # Validate optional image URL
        # Find existing exploration
    history = ExplorationHistory.query.filter_by(
        user_id=current_user.id,
        content_type=content_type,
        content_id=content_id
    ).first()

    if history:
        # Update existing record
        history.title = title
        history.route = route
        history.image_url = image_url
        history.last_viewed_at = datetime.now(timezone.utc)

    else:
        # Create new record
        history = ExplorationHistory(
            user_id=current_user.id,
            content_type=content_type,
            content_id=content_id,
            title=title,
            route=route,
            image_url=image_url,
            last_viewed_at=datetime.now(timezone.utc)
        )

        db.session.add(history)

    db.session.commit()

    return jsonify({
        "message": "Exploration tracked successfully"
    }), 200

    return jsonify({
        "message": "Exploration tracked successfully"
    }), 200

@exploration_bp.get("/recent")
@jwt_required()
def get_recent_exploration():

    history = ExplorationHistory.query.filter_by(
        user_id=current_user.id
    ).order_by(
        ExplorationHistory.last_viewed_at.desc()
    ).limit(5).all()

    return jsonify({
        "recent": [
            {
                "id": item.id,
                "content_type": item.content_type,
                "content_id": item.content_id,
                "title": item.title,
                "image_url": item.image_url,
                "route": item.route,
                "last_viewed_at": format_datetime(item.last_viewed_at)
            }
            for item in history
        ]
    }), 200



@exploration_bp.get("/history")
@jwt_required()
def get_exploration_history():

    history = ExplorationHistory.query.filter_by(
        user_id=current_user.id
    ).order_by(
        ExplorationHistory.last_viewed_at.desc()
    ).all()

    return jsonify({
        "history": [
            {
                "id": item.id,
                "content_type": item.content_type,
                "content_id": item.content_id,
                "title": item.title,
                "image_url": item.image_url,
                "route": item.route,
                "last_viewed_at": format_datetime(item.last_viewed_at)
            }
            for item in history
        ]
    }), 200


@exploration_bp.delete("/history/<int:history_id>")
@jwt_required()
def delete_history_item(history_id):

    item = ExplorationHistory.query.filter_by(
        id=history_id,
        user_id=current_user.id
    ).first()

    if item is None:
        return jsonify({
            "message": "History item not found"
        }), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({
        "message": "History item deleted successfully"
    }), 200
@exploration_bp.delete("/history")
@jwt_required()
def clear_exploration_history():

    ExplorationHistory.query.filter_by(
        user_id=current_user.id
    ).delete()

    db.session.commit()

    return jsonify({
        "message": "Exploration history cleared successfully"
    }), 200