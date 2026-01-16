#!/usr/bin/env bash

set -eux

SCCACHE_NO_DAEMON=1 SCCACHE_LOG=trace sccache-dist scheduler --config scheduler.conf