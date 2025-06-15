#!/bin/bash
set -e

# 주의: -p"password"에서 -p flag랑 비번이랑 붙어있어야함. 
mysql -u root -p"$MYSQL_ROOT_PASSWORD" <<-EOSQL
  GRANT ALL PRIVILEGES ON *.* TO '$MYSQL_USER'@'%' WITH GRANT OPTION;
  FLUSH PRIVILEGES;
EOSQL
