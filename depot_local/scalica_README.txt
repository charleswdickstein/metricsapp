First installation:

Install required packages.
$ sudo apt-get update; sudo apt-get install mysql-server libmysqlclient-dev python-dev python-virtualenv build-essential autoconf libtool pkg-config python-opengl python-imaging python-pyrex python-pyside.qtopengl idle-python2.7 qt4-dev-tools qt4-designer libqtgui4 libqtcore4 libqt4-xml libqt4-test libqt4-script libqt4-network libqt4-dbus python-qt4 python-qt4-gl libgle3 python-dev libssl-dev
(Set a mysql root password)

Force virtual environment to use python 2 by doing virtualenv -p python2 env
$ vim first_install.sh 
	> Change venv line to --> virtualenv -p python2 env
$ ./first_install.sh

Install the proper databases
$ cd db
$ sudo service mysql start
$ ./install_db.sh
(Will ask for the mysql root password configured above).
$ cd ..

Sync the database
$ source ./env/bin/activate
$ cd web/scalica
$ python manage.py makemigrations micro
$ python manage.py migrate


# After the first installation, from the project's directory
Run the server:
$ source ./env/bin/activate
$ cd web/scalica
$ python manage.py runserver 0:8000 

# To run the server forever using screen package:
$ source ./env/bin/activate
$ sudo apt-get install screen
$ screen
$ python manage.py runserver 0:8000
# now exit from the screen
PRESS ctrl+a d
# We can return to the screen by:
$ screen -r

Access the site at http://localhost:8000/micro

