official-citrizen-website
=========================

Неофициален сайт на България, защото официалния не го бива, проект от https://docs.google.com/spreadsheet/ccc?key=0AoQEIaPHnvx6dHVWTDJIUDBrN0FEOURzMUZaRnFTTXc


## Технически детайли


### Преди да започнем

Трябва да има инсталирано на сървъра:

    - nginx server
    - uwsgi server
    - uwsgi python plugin
    - pip (python package manager)
    - virtualenvwrapper
	
### Инсталация

Клонирате си това repo.

След това изпълнявате в терминал:

```
mkvirtualenv citizenqa --no-site-packages
workon citizenqa
pip install django==1.3 south MarkDown html5lib ElementTree ipython python-openid mysql-python
```

Ако смятате да ползвате сървъра за база данни и няма mysql инсталиран:

```
sudo apt-get install mysql-server mysql-client
```

### Базата данни
```
mysql -u root 
```

или ако имате парола за `root` потребителя:

```
mysql -u root -p
```

В самия `mysql` терминал съдавате база данни с:

```
CREATE DATABASE osqa DEFAULT CHARACTER SET UTF8 COLLATE utf8_general_ci ;
```
и излизате от него:

```
exit
```

След това  изпълнявате:

```
python manage.py syncdb --all
python manage.py migrate forum --fake
```

И активирате сървърите:

```
sudo ln -s /home/ubuntu/web/citizenqa/citizenqa.dev.nginx /etc/nginx/sites-enabled
sudo ln -s /home/ubuntu/web/citizenqa/citizenqa.uwsgi /etc/uwsgi/apps-enabled/citizenqa.ini
sudo service uwsgi restart
sudo service nginx restart
```

### FTP достъп

На разработчиците в Obshtestvo.bg беше пратен до мейл ключ за достъп до сървъра.

Прилагам и снимки на това как се настройва FileZilla:

![Към настройките](http://i41.tinypic.com/v62gi8.jpg)

![Добавяне на ключа в настройките](http://i42.tinypic.com/1d6xi.png)

![Създаване на ftp връзка](http://i43.tinypic.com/359ixht.png)
