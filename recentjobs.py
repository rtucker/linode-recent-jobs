#!/usr/bin/python

# Uses the Linode API to display recent jobs for your Linode.
# Useful for running on boot to see why your Linode rebooted.

# Needs api.py somewhere nearby.  You can get this from:
#   Python Bindings @ http://www.linode.com/api/autodoc.cfm

# Ryan Tucker <rtucker@gmail.com>, 2009/08/04

import api
import secrets
import sys

instance = api.Api(key=secrets.API_KEY)

jobs = instance.linode_job_list(linodeid=secrets.LINODE_ID)

if jobs:
    sys.stdout.write('%8s %16s %16s %s %s\n' % ('JobID', 'Submit', 'Finish', '?', 'Description'))
    sys.stdout.write('-'*79 + '\n')
    for i in jobs:
        sys.stdout.write('%8i %16s %16s %i %s\n' % (i['JOBID'], i['ENTERED_DT'][:16], i['HOST_FINISH_DT'][:16], i['HOST_SUCCESS'], i['LABEL']))
else:
    sys.stdout.write('No jobs detected for LinodeID %i' % secrets.LINODE_ID)

