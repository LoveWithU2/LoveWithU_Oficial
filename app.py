from app import app

app = Flask(__name__, static_folder='static')

if __name__ == "__main__":
    app.run(debug=True)
