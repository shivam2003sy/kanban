from app import app
from app.models import User , Card ,List
from flask import request, jsonify
import jwt
from app.util import token_required
@app.route("/api/users/create", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or not data["username"] or not data["email"] or not data["password"]:
        return {
            "message": "Please provide username, email and password!",
            "data": None,
            "error": "Bad Request"
        }, 400
    if User().get_by_username(data["username"]):
        return {
            "message": "User already exists!",
            "data": None,
            "error": "Bad Request"
        }, 400
    new_user = User(
        user=data["username"],
        email=data["email"],
        password=data["password"]
    )
    new_user.save()
    return {
        "message": "User created successfully!",
        "data": new_user.to_json(),
        "error": None
    }, 201


@app.route("/api/users/login", methods=["POST"])
def login_api():
    try:
        data = request.json
        if not data:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        user = User().login(
            data["username"],
            data["password"]
        )
        if user:
            try:
                # token should expire after 24 hrs
                user["public_id"] = jwt.encode(
                    {"id": user["id"]},
                    app.config["SECRET_KEY"],
                    algorithm="HS256"
                )
                return {
                    "message": "Successfully fetched auth token",
                    "data": user
                }
            except Exception as e:
                return {
                    "error": "Something went wrong",
                    "message": str(e)
                }, 500
        return {
            "message": "Error fetching auth token!, invalid email or password",
            "data": None,
            "error": "Unauthorized"
        }, 404
    except Exception as e:
        return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": None
        }, 500

@app.route("/api/lists", methods=["GET"])
@token_required
def all_lists(current_user):
    return {"list" :"all list"}