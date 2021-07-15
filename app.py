from flask import Flask, request, send_file, jsonify, abort
import boto3
from s3 import create_presigned_url, list_files, get_random_image

app = Flask(__name__)
BUCKET = "pieski"

@app.route('/')
def entry_point():
    return 'ok'

@app.route("/files")
def files():
    if request.method == 'GET':
        contents = list_files(BUCKET)
        return jsonify(files = contents)

@app.route("/image/random", methods=['GET'])
def random_image():
    if request.method == 'GET':
        image = get_random_image(BUCKET)

        if image:
          url = create_presigned_url(BUCKET, image['Key'])
          return jsonify(url = url)

        return abort('404', 'No images available')

if __name__ == '__main__':
    # app.debug = True
    app.run()
