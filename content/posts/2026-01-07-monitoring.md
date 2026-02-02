---
title: Setting up monitoring for the DIY cluster
date: 2026-01-07
tags: [netdata, cluster, monitoring]
excerpt: Setting up monitorying for the DIY cluster.
---

Since the DIY cluster is now up and running (see previous post [DIY Cluster and Distributed Building Machine](2025-12-03-diy-cluster.md)), I wanted to set up some monitoring to help me keep track of the cluster's resource usage (especially during building larger software projects).

In my limited experience, I was thinking of setting something up using Grafana and Prometheus. I did a little research with gemini and it's three top suggestions were:

*   [netdata](https://www.netdata.cloud/)
*   [Grafana](https://www.grafana.com/) and [Prometheus](https://prometheus.io/)
*   [Glances](https://nicolargo.github.io/glances/)


<br>
**netdata seemed like the easiest to setup and had the best looking interface so I went with that.**


# Setup and Testing

Initially, I was hoping to set things up without connecting to a netdata account, but eventually just ended up creating one because it seemed like it was mandatory.

!!! implementation "Netdata Account"
    It may not have been strictly necessary, but setting things up to run in isolation on my local cluster seemed like more work than it was worth.

On my first pass setting things up, I setup one of my nodes as a parent and the others as children, which required a few easy modifications to the config file for netdata.
Eventually realized that this wasn't strictly necessary, so I set up all my machines on the cluster as simple children.
To set them up, all you need to do is run the following on the command line (if you're on their website you can follow the links to "add node" and it will generate the full command for your account with the appropriate tokens):

```bash
wget -O /tmp/netdata-kickstart.sh https://get.netdata.cloud/kickstart.sh && sh /tmp/netdata-kickstart.sh --nightly-channel --claim-token <YOUR_CLAIM_TOKEN_>--claim-rooms <CLAIM_ROOM_UUID_> --claim-url https://app.netdata.cloud
```

