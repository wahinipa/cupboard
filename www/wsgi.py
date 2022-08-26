# Copyright 2022 Wahinipa LLC
import logging

from www.tracking.commons.builder import create_app

app = create_app()

if __name__ == '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.run()
