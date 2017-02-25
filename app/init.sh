sudo service nginx start
gunicorn -t777 -w3 -b0.0.0.0:5000 monitor:app
