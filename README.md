# gdax-data

# Trading Starting Dates

* Bitcoin (BTC)
* Bitcoin Cash (BCH): 2017-12-19. See [details](https://status.gdax.com/incidents/51pnkvm843hq).
* Ethereum (ETH)
* Litecoin (LTC): 2016-08-23. See [details](https://blog.gdax.com/gdax-adds-litecoin-trading-9f72d1c75be4)

# Installation

This installation guide works only for Ubuntu Linux 17.04 / 17.10:

1. Check out the source code from this repository via Git and SSH. If you don't have git or ssh installed, type the following command in Terminal:

   ```
   sudo apt install git ssh
   ```

2. Install MySQL database and related services/utilities:
   - Type the following command in Terminal to install Apache2 server:

     ```
     sudo apt install apache2
     ```

   - Type the following command to install MySQL (*This works for MySQL version before 5.7*):

     ```
     sudo apt install mysql-server mysql-client libmysqlclient-dev
     ```
     You will be asked to set a password for accessing MySQL.
   - For MySQL 5.7 or later, you cannot set password for root user. Refer to Step 3 for the user configuration.
   - Type the following command to install PHPMyAdmin, a GUI tool to manipulate MySQL:

     ```
     sudo apt install phpmyadmin
     ````
     You will be asked to type in the password accessing MySQL, which is the one you already set in the step above.
   - Type

     ```
     sudo gedit /etc/apache2/apache2.conf
     ```
     to open the config file of Apache2; add the following line in it:
   ```
   Include /etc/phpmyadmin/apache.conf
   ```
     Save and close the file; then type `sudo service apache2 restart` to restart Apache2.
   - Open any web browser, type `http://localhost/phpmyadmin` to open PHPMyAdmin.

3. (For MySQL 5.7 or later ONLY) Create a super user account in MySQL:
   - In Terminal, type the following command to login MySQL as root:
   ```
   sudo mysql
   ```
   - In MySQL shell, type the following command to create a user:
   ```
   CREATE USER 'yihming'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password' PASSWORD EXPIRE NEVER;
   ```
   In the command, you have create a user with name 'yihming' at host 'localhost'. You can change the user name, and change 'localhost' to '%' to allow remote access. Moreover, change 'password' to your own password.
   - Type the following command to assign all privileges to this user:
   ```
   GRANT ALL on *.* TO 'yihming'@'localhost';
   ```
   Note that you should change 'yihming' and 'localhost' to your own setting above.
   - When finished, type `\q` to exit MySQL shell.

4. Create Database and Table for the Project:
   - Access to MySQL via PHPMyAdmin; in the main window, click "Databases" button; create a database (say "gdax"), with recommended collation "utf8_bin"; then click "Create" button.
   - Click the created database "gdax" in the left panel; Click "Import" button in the main window; Choose "gdax.sql" file in the repository by clicking "Browse..." button; click "Go" button at the bottom.
   - Now you should see a table "history" created inside the database "gdax", with no entry but several fields set.

5. Set up the database connection config file in the repository:
   - In the repository, type `cp dbconn.json.example dbconn.json` to create a Database config file from the example.
   - Open "dbconn.json", replace "your-password" by your own password to MySQL; save and close.

6. Install necessary python packages:
   - Install python develop tools:
   ```
   sudo apt install python-setuptools python-dev build-essential python-pip ipython
   ```
     And type `sudo pip install --upgrade pip` to upgrade pip to the latest version.
   - Install the following packages via pip:
   ```
   sudo pip install gdax mysqlclient python-dateutil
   ```

7. Start to collect historic rates:
```
python collect_history.py
```
   To change the product, start and end datetime for the collection:
   - Open "collect_history.py" file; look for function "main()".
   - In the line `product = 'BTC-USD'`, change the value of `product` to the product you are interested.
   - Change the value of `von` (start datetime) and `bis` (end datetime) using ISO 8601 datetime format, and using UTC time zone.