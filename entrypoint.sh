#!/bin/bash


exec gunicorn web_db.web_app.wsgi:application -b 0.0.0.0:8080 --reload
