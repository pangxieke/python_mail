#!/bin/bash

set -e

app="mail"

commitid="v1.0"

echo "commitid = ${commitid}"

docker build --no-cache -t ${app}:${commitid} -f Dockerfile .
