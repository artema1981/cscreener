#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from density.binance_ws import all_futures_binance, start_api_ws
import redis
from density.chart_of_dencitys import create_instans_chartofdencitys
import threading


redis_client = redis.Redis(host='localhost', port=6379, db=0)

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CScreener.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # clean redis_db
    redis_client.flushall()

    # create list all futures
    all_futures_binance()

    # connect to api and websockets
    start_api_ws()
    threading.Thread(target=create_instans_chartofdencitys).start()

    main()
