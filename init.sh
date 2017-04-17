sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/default
sudo /etc/init.d/nginx restart

sudo /etc/init.d/mysql start
sudo mysql -uroot -e "CREATE DATABASE stepic_web_project_db;"
sudo mysql -uroot -e "CREATE USER 'django@localhost' IDENTIFIED BY 'password';"
sudo mysql -uroot -e "GRANT ALL ON dj.* TO 'django@localhost';"
sudo mysql -uroot -e "GRANT USAGE ON *.* TO 'django@localhost';"
sudo mysql -uroot -e "FLUSH PRIVILEGES;"

sudo gunicorn -c /home/box/web/etc/gunicorn.conf hello:wsgi_application
sudo gunicorn -c /home/box/web/etc/gunicorn-django.conf ask.wsgi:application