from flask import Flask, render_template, request


app = Flask(__name__)



@app.route("/", methods=["GET", "POST"])  # Handles both GET and POST
def index():
    if request.method == "POST":
        first_name = request.form.get("first_name")  # Use .get() to avoid KeyError
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        date = request.form.get("date")
        occupation = request.form.get("occupation")

        print(first_name, last_name, email, date, occupation)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Host updated for local network access
