from app import create_app

if __name__ == "__main__":
    app = create_app(config_filename="../config.py")
    app.run(debug=True, host="0.0.0.0", port=8083)
