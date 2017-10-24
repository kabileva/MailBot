Current files should be located in /var/www/mailbotapp directory

You also need to add /etc/apache2/sites-available/mailbotapp.conf file with following contents:
<VirtualHost *:80>
                ServerName 143.248.140.198
                ServerAdmin t.b.alisher@gmail.com
                WSGIScriptAlias / /var/www/mailbotapp/mailbotapp.wsgi
                <Directory /var/www/mailbotapp/mailbotapp/>
                        Require all granted
                </Directory>
                Alias /static /var/www/mailbotapp/mailbotapp/static
                <Directory /var/www/mailbotapp/mailbotapp/static/>
                        Require all granted
                </Directory>
                ErrorLog ${APACHE_LOG_DIR}/error.log
                LogLevel warn
                CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost> 
