import json

import predict

from flask import Flask, render_template, request

# Flask app setup
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        json_content = json.loads(request.form.get("opportunityObject"))
        predicted_dict, x = predict.predict(predict.model, json_content, predict.out_data, predict.entite)
        return render_template("result.html", result=predicted_dict)

    elif request.method == "GET":

        return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
