#!/bin/sh
set -e
# Genera /etc/nginx/allowlist.conf desde $ALLOWED_IPS (lista separada por comas, IPs o CIDR)
CONF=/etc/nginx/allowlist.conf
if [ -n "$ALLOWED_IPS" ]; then
  echo "# Restricción por IP activada (ALLOWED_IPS)" > "$CONF"
  OLDIFS=$IFS; IFS=','
  for ip in $ALLOWED_IPS; do
    ip=$(echo "$ip" | tr -d ' ')
    [ -n "$ip" ] && echo "allow $ip;" >> "$CONF"
  done
  IFS=$OLDIFS
  echo "deny all;" >> "$CONF"
  echo "[lms] Acceso limitado a: $ALLOWED_IPS"
else
  echo "# Sin restricción por IP" > "$CONF"
  echo "allow all;" >> "$CONF"
  echo "[lms] Sin restricción por IP (ALLOWED_IPS vacío)"
fi
exec nginx -g 'daemon off;'
