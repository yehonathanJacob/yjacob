import os
from flask import Flask, render_template

app = Flask(__name__)


color = os.environ.get('APP_COLOR','blue')

@app.route("/")
def main():
	print(color)
	return f"color={color}"

if __name__ == "__main__":
	app.run(host="0.0.0.0", port="8080")
