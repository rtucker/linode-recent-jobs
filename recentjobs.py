#!/usr/bin/python

# Uses the Linode API to display recent jobs for your Linode.
# Useful for running on boot to see why your Linode rebooted.

# Run with the --help option to see the full scoop.

# Recent api.py available from http://www.linode.com/api/autodoc.cfm

# Ryan Tucker <rtucker@gmail.com>, 2009/08/04

import optparse
import sys

from operator import itemgetter

sys.path.insert(0,'api')
import api
del sys.path[0]

bootlabels = ['Lassie initiated boot', 'System Boot',
              'Host initiated restart', 'Lish initiated boot']

def get_jobs(instance, linodeid):
    return instance.linode_job_list(linodeid=linodeid)

def list_all_jobs(jobs):
    out = ''
    out += '%8s %16s %16s %s %s\n' % ('JobID', 'Submit', 'Finish', '?', 'Description')
    out += '-'*79 + '\n'
    for i in sorted(jobs, key=itemgetter('JOBID'), reverse=False):
        out += '%8i %16s %16s %i %s\n' % (i['JOBID'], i['ENTERED_DT'][:16], i['HOST_FINISH_DT'][:16], i['HOST_SUCCESS'], i['LABEL'])

    return out

def last_boot(jobs):
    for i in sorted(jobs, key=itemgetter('JOBID'), reverse=True):
        for j in bootlabels:
            if i['LABEL'].startswith(j):
                if i['HOST_SUCCESS'] == 1:
                    return 'Booted %s due to: %s\n' % (i['HOST_FINISH_DT'][:16], i['LABEL'])
    return 'No information.'

def list_linodes(instance):
    out = '%9s %12s %s\n' % ('LinodeID', 'Datacenter', 'Label')
    out += '-'*79+'\n'
    dcs = {}
    for i in instance.avail_datacenters():
        dcs[i['DATACENTERID']] = i['LOCATION'].split(',')[0]
    for i in instance.linode_list():
        out += '%9i %12s %s\n' % (i['LINODEID'], dcs[i['DATACENTERID']], i['LABEL'])
    return out

def main():
    parser = optparse.OptionParser()
    parser.add_option("-a", "--all-jobs", dest="alljobs", action="store_true",
        help="Display a list of all jobs in the job history.", default=False)
    parser.add_option("-l", "--last-boot", dest="lastboot", action="store_true",
        help="Display the timestamp and reason of the last boot. (default)",
        default=False)
    parser.add_option("-K", "--api-key", dest="apikey",
        help="Specify the API key (can also put in secrets.py).",
        default=False)
    parser.add_option("-I", "--linode-id", dest="linodeid",
        help="Specify the Linode ID (can also put in secrets.py).", 
        default=False)
    parser.add_option("--list-linodes", dest="listlinodes", action="store_true",
        help="List Linode IDs associated with this account.",
        default=False)

    (options, args) = parser.parse_args()

    try:
        import secrets
    except:
        secrets = False

    if not options.apikey:
        if secrets:
            apikey = secrets.API_KEY
        else:
            parser.error("Need either secrets.py or --api-key option")
    else:
        apikey = options.apikey

    if (not options.linodeid) and (not options.listlinodes):
        if secrets:
            linodeid = secrets.LINODE_ID
        else:
            parser.error("Need either secrets.py or --linode-id option")
    else:
        linodeid = options.linodeid

    instance = api.Api(key=apikey)

    if options.lastboot:
        jobs = get_jobs(instance, linodeid)
        sys.stdout.write(last_boot(jobs))
    elif options.alljobs:
        jobs = get_jobs(instance, linodeid)
        sys.stdout.write(list_all_jobs(jobs))
    elif options.listlinodes:
        sys.stdout.write(list_linodes(instance))
    else:
        jobs = get_jobs(instance, linodeid)
        sys.stdout.write(last_boot(jobs))

if __name__ == "__main__":
    main()

