from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
    app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50MB