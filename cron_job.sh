#!/bin/bash

# Morning run at 5:00 AM - tomorrow variable should be today
0 5 * * * cd /app && python3 -c "
from datetime import datetime, timedelta
import os
os.environ['RUN_TIME'] = 'morning'
exec(open('main.py').read())
" >> /var/log/cron/db_notifier.log 2>&1

# Evening run at 10:00 PM - tomorrow variable should be tomorrow
0 22 * * * cd /app && python3 -c "
from datetime import datetime, timedelta
import os
os.environ['RUN_TIME'] = 'evening'
exec(open('main.py').read())
" >> /var/log/cron/db_notifier.log 2>&1
