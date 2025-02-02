#!/bin/bash
echo $@

cp /tinyproxy/tinyproxy.conf /tmp/tinyproxy.conf
ip=$(cat /etc/hosts | grep \\. | grep -v localhost | awk '{print $1}')
gateway=$(route -n | grep 'UG[ \t]' | awk '{print $2}')
echo "" >> /tmp/tinyproxy.conf
echo "#Added by start.sh. These will be overwridden " >> /tmp/tinyproxy.conf
echo "Listen $ip" >> /tmp/tinyproxy.conf
echo "Allow $ip" >> /tmp/tinyproxy.conf
echo "Allow $gateway" >> /tmp/tinyproxy.conf
echo "Allow 127.0.0.1" >> /tmp/tinyproxy.conf

#Run tinyproxy
# Not sure if we need to set host and allowed IPs
#cat /tmp/tinyproxy.conf
#tinyproxy -c /tmp/tinyproxy.conf
tinyproxy -c /tinyproxy/tinyproxy.conf
#Run Wireguard normally

# WSL
WG_QUICK_PATH="/usr/bin/wg-quick"
sed -i 's|\| cmd \$iptables-restore -n||g' "$WG_QUICK_PATH"

unset WG_CONFS
rm -rf /app/activeconfs
# Enumerate interfaces
for wgconf in $(ls /config/wg_confs/*.conf); do
    if grep -q "\[Interface\]" "${wgconf}"; then
        echo "**** Found WG conf ${wgconf}, adding to list ****"
        WG_CONFS+=("${wgconf}")
    else
        echo "**** Found WG conf ${wgconf}, but it doesn't seem to be valid, skipping. ****"
    fi
done

if [[ -z "${WG_CONFS}" ]]; then
    echo "**** No valid tunnel config found. Please create a valid config and restart the container ****"
    ip route del default
    exit 0
fi

unset FAILED
for tunnel in ${WG_CONFS[@]}; do
    echo "**** Activating tunnel ${tunnel} ****"
    if ! wg-quick up "${tunnel}"; then
      FAILED="${tunnel}"
      break
    fi
done

if [[ -z "${FAILED}" ]]; then
    declare -p WG_CONFS > /app/activeconfs
    echo "**** All tunnels are now active ****"
else
    echo "**** Tunnel ${FAILED} failed, will stop all others! ****"
    for tunnel in ${WG_CONFS[@]}; do
        if [[ "${tunnel}" = "${FAILED}" ]]; then
            break
        else
            echo "**** Disabling tunnel ${tunnel} ****"
            wg-quick down "${tunnel}" || :
        fi
    done
    ip route del default
    echo "**** All tunnels are now down. Please fix the tunnel config ${FAILED} and restart the container ****"
fi

sleep infinity
