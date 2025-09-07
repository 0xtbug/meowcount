import os
from src.app import app

def is_dev_mode() -> bool:
    mode = (
        os.environ.get("APP_MODE")
        or os.environ.get("FLASK_ENV")
        or os.environ.get("ENV")
        or ""
    ).lower()
    return mode in {"dev", "development", "debug"}

if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 3000))

    if is_dev_mode():
        app.run(host=host, port=port, debug=True, use_reloader=True)
    else:
        try:
            from waitress import serve

            serve(app, host=host, port=port)
        except ImportError:
            import warnings

            warnings.warn(
                "Waitress is not installed. Falling back to Flask dev server. "
                "Install 'waitress' and set APP_MODE=prod for production."
            )
            app.run(host=host, port=port, debug=False)
