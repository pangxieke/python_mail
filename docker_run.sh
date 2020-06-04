#!/bin/bash

docker run --name mail -d \
  -v /data/services/mail/conf:/usr/src/app/conf \
	-v /data/logs:/usr/src/app/logs \
	mail:v1.0