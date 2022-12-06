#!/bin/sh

set -e

envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf
# in default.conf.tpl, ${x} will be replaced with the x environment variable
nginx -g 'daemon off;'
# run nginx on the foreground