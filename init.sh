apt-get update
apt-get install mysql-server > /dev/null
apt-get update
pip install selenium 
apt install chromium-chromedriver
cp /usr/lib/chromium-browser/chromedriver /usr/bin > /dev/null
service mysql start
pip -q install PyMySQL flask_sqlalchemy flask_mysqldb flask_wtf pyngrok
ngrok authtoken 1hZjWPDFqc7JZWwwqNBqoYP4dXm_4P5nDk1bJjcAta6iCDczG
mysql -u root --password=root -e "CREATE DATABASE litwallet; USE litwallet; CREATE TABLE users(id int PRIMARY KEY AUTO_INCREMENT, name varchar(255), password varchar(255), email_address varchar(255 ) DEFAULT NULL); INSERT INTO users(name, password) VALUES('Francis', 'Tucket');"
ngrok http 5000