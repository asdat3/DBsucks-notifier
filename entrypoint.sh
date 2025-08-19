#!/bin/bash

# Start cron service
service cron start

# Keep container running
tail -f /var/log/cron/db_notifier.log
