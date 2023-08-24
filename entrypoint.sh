#!/bin/sh
python manage.py migrate --noinput

# 環境変数のDEBUGの値がTrueの時はrunserverを、Falseの時はgunicornを実行します
if [ $DEBUG = "True" ]
then
    python manage.py runserver 0.0.0.0:8000
else
    python manage.py compilescss
    python manage.py collectstatic --noinput
    # gunicornを起動させる時はプロジェクト名を指定します
    gunicorn hosnakpub.wsgi:application --bind 0.0.0.0:8000
fi
