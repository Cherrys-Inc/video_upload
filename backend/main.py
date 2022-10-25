# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import math
import os
import random
from asyncio import sleep

from flask import Flask, request, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

import boto3

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
db = SQLAlchemy(app)

app.config['S3_BUCKET'] = os.getenv("S3_BUCKET")
app.config['S3_KEY'] = os.getenv("AWS_ACCESS_KEY_ID")
app.config['S3_SECRET'] = os.getenv("AWS_ACCESS_SECRET")
app.config['S3_LOCATION'] = 'http://{}.s3.amazonaws.com/'.format(os.getenv("S3_BUCKET"))


class Videos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200))


def to_json(self):
    return {
        'id': self.id,
        'url': self.url
    }


s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_ACCESS_SECRET")
)


@app.route('/', methods=['POST'])
def fileupload():
    file = request.files["file"]
    filename = file.filename

    print(filename)
    if file:
        file.filename = secure_filename(file.filename)
        output = send_to_s3(file, app.config["S3_BUCKET"])
        videos = Videos()

        videos.url = str(output)
        db.session.add(videos)
        db.session.commit()

        return str(output)

    else:
        response = "File not found"
    return response


@app.route('/', methods=['GET'])
def home():
    data = []
    video_list = Videos.query.all()

    for video in video_list:
        data.append(video.url)

    return jsonify(data)


def send_to_s3(file, bucket_name, acl="public-read"):
    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            "Anisha/" + file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type  # Set appropriate content type as per the file
            }
        )
    except Exception as e:
        print("Something Happened: ", e)
        return e
    return "{}{}".format(app.config["S3_LOCATION"] + "Anisha/", file.filename)


if __name__ == "__main__":
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
