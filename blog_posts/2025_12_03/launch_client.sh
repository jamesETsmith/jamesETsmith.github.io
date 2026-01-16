#!/usr/bin/env bash

set -eux

export SCCACHE_CONF=/home/james/projects/jamesETsmith.github.io/blog_posts/2025_12_03/client.conf
sccache --start-server
# sudo SCCACHE_LOG=trace $(which sccache-dist) server --config client.conf
