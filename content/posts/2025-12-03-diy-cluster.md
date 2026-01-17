---
title: DIY Cluster and Distributed Building Machine
date: 2025-12-03
tags: [sccache, HPC]
excerpt: While I'm out on parental leave, I don't have access to my work cluster. Since I still want to build larger software projects in a reasonable amount of time, I decided to try and hook up several old computers I had lying around.
---

While I'm out on parental leave, I don't have access to my work cluster. Since I still want to build larger software projects in a reasonable amount of time, I decided to try and hook up several old computers I had lying around.

# The Plan

*The goal of this little project is just to speed up how fast I can build larger software projects (e.g. LLVM).*

1.  Compile time on a single computer
2.  Compile time on multiple computers connected via Ethernet
3.  Maybe setup slurm? (tbd on this since it's not necessary for my goal)

While I'm hoping to use this on projects the size of LLVM and PyTorch, for this I'm going to target a smaller project so I can iterate quickly.

# Setting up static IP Addresses for the Machines

Initially, I tried to set static IP addresses through the router, but the MAC address randomization made this a pain. So instead I created a script to setup the IP addresses on each machine.

```bash
#!/bin/bash

# Auto-detect the Ethernet interface name
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
```

# Setting up sccache

Following the [instructions](https://github.com/mozilla/sccache/blob/main/docs/DistributedQuickstart.md) on sccache's distributed setup. TLDR, I chose to setup a scheduler, client, and builder on my primary machine and then a builder on the secondary machine.

## Primary Machine

### Scheduler

```toml
# scheduler.conf
# Listen on LAN IP and a fixed port
public_addr = "192.168.1.210:10600" # Change this to the desired IP address

[client_auth]
type = "token"
token = "YOUR_CLIENT_TOKEN_HERE"

[server_auth]
type = "token"
token = "YOUR_SERVER_TOKEN_HERE"
```

Start the scheduler

```bash
SCCACHE_NO_DAEMON=1 SCCACHE_LOG=trace sccache-dist scheduler --config scheduler.conf
```

### Build Server

```toml
# server.conf
# Listen address for the builder
cache_dir = "/tmp/toolchains"
public_addr = "192.168.1.210:10501"
scheduler_url = "http://192.168.1.210:10600"

[builder]
type = "overlay"
build_dir = "/var/lib/sccache/build"
bwrap_path = "/usr/bin/bwrap"

[scheduler_auth]
type = "token"
token = "YOUR_SERVER_TOKEN_HERE"
```

Start the build server

```bash
mkdir -p /var/lib/sccache/build
sudo apt install bubblewrap
sudo SCCACHE_LOG=trace $(which sccache-dist) server --config server.conf
```

### Client

```toml
# client.conf
[dist]
scheduler_url = "http://192.168.1.210:10600"
toolchain_cache_size = 10737418240

[dist.auth]
type = "token"
token = "YOUR_CLIENT_TOKEN_HERE"
```

```bash
export SCCACHE_CONF=/PATH/TO/client.conf
sccache --start-server
sccache --dist-status
```

Example output for three connected servers:

```bash
{"SchedulerStatus":["http://192.168.1.210:10600/",{"num_servers":3,"num_cpus":28,"in_progress":0}]}
```

