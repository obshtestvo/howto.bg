#!/usr/bin/env bash

VAGRANT_DIR=/vagrant
PROJECT_NAME=howtobg
DB_NAME=$PROJECT_NAME

sudo apt-get update -y

# usability (can be omitted)
sudo apt-get update -y
touch $HOME/.hushlogin
sudo apt-get install expect curl zsh fortune cowsay htop git build-essential -y
wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh
sudo mkdir -p $HOME/.oh-my-zsh/custom/plugins
git clone git://github.com/zsh-users/zsh-syntax-highlighting.git  $HOME/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting
sudo chsh -s `which zsh` vagrant
sed -i.bak 's/^plugins=(.*/plugins=(git django python pip virtualenvwrapper zsh-syntax-highlighting)/' $HOME/.zshrc
echo "export LC_ALL=en_US.UTF-8" >> $HOME/.zshrc
echo "export LANG=en_US.UTF-8" >> $HOME/.zshrc


# settings
if [ ! -f "$VAGRANT_DIR/server/settings_app.py" ]; then
    cp $VAGRANT_DIR/server/settings_app.py.vagrant-sample $VAGRANT_DIR/server/settings_app.py
fi

# database
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password password'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password password'
sudo apt-get install mysql-server -y
mysql -uroot -ppassword -e "SET PASSWORD = PASSWORD('');"
mysql -uroot -e "CREATE DATABASE \`$DB_NAME\` CHARACTER SET utf8 COLLATE utf8_general_ci;"
sudo apt-get install python-dev libmysqlclient-dev -y

# django project specific
sudo apt-get install python-pip -y
sudo pip install virtualenvwrapper
source virtualenvwrapper.sh
mkvirtualenv $PROJECT_NAME --no-site-packages
workon $PROJECT_NAME
pip install -r $VAGRANT_DIR/requirements.dev.txt

# project sturcture & permissions
mkdir -p $VAGRANT_DIR/log
mkdir -p $VAGRANT_DIR/cache
touch $VAGRANT_DIR/log/django.osqa.log
chmod 777 -R $VAGRANT_DIR/log
chmod 777 -R $VAGRANT_DIR/cache
chmod 777 -R $VAGRANT_DIR/forum/upfiles

# django database init
python $VAGRANT_DIR/manage.py syncdb --all --noinput
#python $VAGRANT_DIR/manage.py migrate
python $VAGRANT_DIR/manage.py migrate forum --fake
mysql $PROJECT_NAME -u root < $VAGRANT_DIR/forum_modules/mysqlfulltext/fts_install.sql

# servers
sudo apt-get install nginx-full uwsgi uwsgi-plugin-python -y
sudo usermod -a -G vagrant www-data
sudo ln -s $VAGRANT_DIR/server/settings_nginx.vagrant.conf /etc/nginx/sites-enabled/vagrant.conf
sudo ln -s $VAGRANT_DIR/server/settings_uwsgi.vagrant.ini /etc/uwsgi/apps-enabled/vagrant.ini
ln -s $HOME/.virtualenvs/$PROJECT_NAME/lib/python2.7/site-packages/django/contrib/admin/static/admin/ $VAGRANT_DIR/admin_media
sudo rm /etc/nginx/sites-available/default
sudo service nginx restart
sudo service uwsgi restart
echo "start on vagrant-mounted

script
  service nginx restart
  service uwsgi restart
  (cd $VAGRANT_DIR &&   )
end script" | sudo tee /etc/init/vagrant-fix.conf