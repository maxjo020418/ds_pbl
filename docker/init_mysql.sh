#!/bin/bash
set -e

# Expand env vars in shell before sending to mysql
mysql -u root -p"$MYSQL_ROOT_PASSWORD" <<-EOSQL
  GRANT ALL PRIVILEGES ON *.* TO '$MYSQL_USER'@'%' WITH GRANT OPTION;
  FLUSH PRIVILEGES;
EOSQL
