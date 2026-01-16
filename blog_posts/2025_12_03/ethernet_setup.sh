#!/bin/bash

# 1. AUTO-DETECT the Ethernet interface name
# This looks for the first hardware device of type 'ethernet'
IFACE=$(nmcli -t -f DEVICE,TYPE device | grep ':ethernet' | head -n 1 | cut -d: -f1)

if [ -z "$IFACE" ]; then
    echo "Error: No Ethernet hardware detected!"
    exit 1
fi

# Define variables
IP_ADDR="192.168.1.210/24" # Change this to the desired IP address
GATEWAY="192.168.1.1"
DNS_SERVERS="1.1.1.1,8.8.8.8"
PROFILE_NAME="Home-Static"

echo "Detected Interface: $IFACE"

echo "Step 1: Removing old connection profiles..."
sudo nmcli con delete "Wired connection 1" || true
sudo nmcli con delete "$PROFILE_NAME" || true

echo "Step 2: Creating new profile '$PROFILE_NAME' for $IFACE..."
sudo nmcli con add type ethernet con-name "$PROFILE_NAME" ifname "$IFACE" \
  ip4 "$IP_ADDR" gw4 "$GATEWAY"

echo "Step 3: Configuring DNS and Method..."
sudo nmcli con mod "$PROFILE_NAME" ipv4.dns "$DNS_SERVERS"
sudo nmcli con mod "$PROFILE_NAME" ipv4.method manual

echo "Step 4: Disabling MAC Randomization..."
sudo nmcli con mod "$PROFILE_NAME" 802-3-ethernet.cloned-mac-address permanent

echo "Step 5: Activating the connection..."
sudo nmcli con up "$PROFILE_NAME"

echo "------------------------------------------------"
echo "Verification:"
ip addr show "$IFACE" | grep "inet "
