import datetime
from dataclasses import dataclass
from typing import Any

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

from config import SQLALCHEMY_DATABASE_URI

app = Flask(__name__, static_folder="./dist/assets", template_folder="./dist")
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(100), unique=True, nullable=False)
    image_name = db.Column(db.String(100), unique=True, nullable=False)
    upload_time = db.Column(db.DateTime, nullable=False, default=db.func.now())

    def __init__(self, image_url=None, image_name=None) -> None:
        self.image_url = image_url
        self.image_name = image_name

    def save(self):
        db.session.add(self)
        db.session.commit()


@dataclass
class Response:
    code: int
    message: str
    data: Any = None

    def __init__(self, code, message, data=None):
        self.code = code
        self.message = message
        self.data = data


@app.route("/api/image/queryAll", methods=["GET"])
def list_images():
    images = Image().query.all()

    image_list = [
        {
            "id": image.id,
            "imageUrl": image.image_url,
            "imageName": image.image_name,
            "uploadTime": datetime.datetime.strftime(
                image.upload_time, "%Y-%m-%d %H:%M:%S"
            ),
        }
        for image in images
    ]
    return jsonify(Response(200, "success", image_list))


@app.route("/api/image/add", methods=["POST"])
def add():
    problem = request.get_json()
    image = Image(image_url=problem["imageUrl"], image_name=problem["imageName"])
    image.save()
    return jsonify(Response(201, "success", "添加成功"))


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8088)
