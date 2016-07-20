sudo service nginx start
gunicorn -w3 -b127.0.0.1:5000 monitor:app