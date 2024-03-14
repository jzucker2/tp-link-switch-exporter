#!/usr/bin/env python3
from app import create_app


if __name__ == "__main__":
    app = create_app()
    host = app.config.get('TP_LINK_SWITCH_EXPORTER_HOST')
    port = app.config.get('TP_LINK_SWITCH_EXPORTER_PORT')
    app.run(host=host, port=port, debug=True)
