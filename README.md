
ALL YOU NEED:

https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-14-04
did everything except ran gunicorn --workers=3 --bind ... icarus_server:app

also use pip3 to install everything

postgres remote access:

http://www.cyberciti.biz/tips/postgres-allow-remote-access-tcp-connection.html


# Grab psycopg2 and pip
apt-get install python3-pip python3-psycopg2

# Remove the Python 2.7 version of gunicorn, so we can...
pip uninstall gunicorn

# Install the Python 3 version of gunicorn, and a couple of dependencies.
pip3 install gunicorn tornado django
# Sadly, at time of writing, gevent isn't Python 3 compatible... But tornado is!
# So, switch them out with a little sed magic
sed 's/worker_class = '\''gevent'\''/worker_class='\''tornado'\''/' /etc/gunicorn.d/gunicorn.py -i.orig

# Restart gunicorn to make the changes take effect...
service gunicorn restart


###############################################
# To start SERVERS:
sudo start icarus
sudo start icarus_tcp //listens on localhost 8888

solartruckingisbadass

logs: sudo /var/log/upstart/icarus.log only right after server has been restarted

HAD TO RUN THIS: sudo chown -R username:group directory
