sudo service nginx start
gunicorn -w3 -b0.0.0.0:5000 monitor:app
