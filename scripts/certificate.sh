#!/bin/sh
sudo yum -y install epel-release
sudo yum -y install snapd
sudo systemctl enable --now snapd.socket
sudo ln -s /var/lib/snapd/snap /snap
sudo snap install core; sudo snap refresh core
sudo yum remove certbot
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
sudo certbot certonly --standalone --register-unsafely-without-email --agree-tos -d ${domain}
cert=`sudo cat /etc/letsencrypt/live/${domain}/fullchain.pem`
key=`sudo cat /etc/letsencrypt/live/${domain}/privkey.pem`
cert_base64=`sudo cat /etc/letsencrypt/live/${domain}/fullchain.pem | base64`
key_base64=`sudo cat /etc/letsencrypt/live/${domain}/privkey.pem | base64`
ctx instance runtime-properties 'cert' "${cert}"
ctx instance runtime-properties 'key' "${key}"
ctx instance runtime-properties 'cert_base64' "${cert_base64}"
ctx instance runtime-properties 'key_base64' "${key_base64}"