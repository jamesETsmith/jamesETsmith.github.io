---
title: Setting up monitorying for the DIY cluster
date: 2026-01-07
tags: [netdata, cluster, monitoring]
excerpt: Setting up monitorying for the DIY cluster.
---

Since the DIY cluster is now up and running (see previous post [DIY Cluster and Distributed Building Machine](2025_12_03.html)), I wanted to set up some monitoring to help me keep track of the cluster's resource usage (especially during building larger software projects).

In my limited experience, I was thinking of setting something up using Grafana and Prometheus. I did a little research with gemini and it's three top suggestions were:

*   netdata
*   Grafana and Prometheus
*   Glances

I don't really need to maintain historical data and the setup for netdata and Glances seemed simple enough so I tried them first.

```bash
# install netdata
wget -O /tmp/netdata-kickstart.sh https://get.netdata.cloud/kickstart.sh && sh /tmp/netdata-kickstart.sh --no-updates --stable-channel --disable-telemetry
```

