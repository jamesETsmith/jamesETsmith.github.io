#!/usr/bin/env bash

set -eux

sudo SCCACHE_LOG=trace $(which sccache-dist) server --config server.conf
