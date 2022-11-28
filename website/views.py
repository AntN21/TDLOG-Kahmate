from flask import Blueprint, render_template, request
import re
import random
import numpy as np

views = Blueprint("views", __name__)
chips = [["" for x in range(11)] for x in range(8)]


@views.route("/", methods=["GET", "POST"])
def game():
    print(request.form)
    if request.method == "POST":
        position = re.sub(r"[() ]", "", request.form["next"]).split(",")
        chips[int(position[0])][int(position[1])] = random.choice(
            ["c", "o", "f", "s", "t", "x"]
        )
        if random.randint(0, 2) == 1:
            chips[int(position[0])][int(position[1])] += "b"
    return render_template("game.html", chips=chips)
