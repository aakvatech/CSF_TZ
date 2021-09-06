#!/bin/bash

if [ -z "$1" ]; then
  echo 
  echo "    Usage: ./lets-encrypt.sh [sitename]"
  echo "        [sitename]:       Name of the site e.g. dev-erp.mydomain.com"
  echo 

  exit
fi

sudo certbot certonly --nginx -d $1
bench --site $1 set-config ssl_certificate /etc/letsencrypt/live/$1/fullchain.pem
bench --site $1 set-config ssl_certificate_key /etc/letsencrypt/live/$1/privkey.pem
bench setup nginx --yes
sudo systemctl reload nginx
./bench-restart.sh

