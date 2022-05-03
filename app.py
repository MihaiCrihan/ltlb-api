from src.app import app, FlaskConfig


if not FlaskConfig.PRODUCTION:
    if __name__ == '__main__':
        app.run(FlaskConfig.HOST, FlaskConfig.PORT, debug=FlaskConfig.DEBUG)
