#!/usr/bin/python3

import boto3, pprint, datetime

ACCOUNT_ID = "###"

def get_old_snapshots():
    '''
    This function leverages the boto3 EC2 API to query for EBS snapshots that are older than 14 days.

    Returns a list of EBS snapshot IDs or an empty list.
    '''
    try:
        ebs_client = boto3.client('ec2')

        # Grab all snapshots based on the account ID.
        snapshots = ebs_client.describe_snapshots(OwnerIds=[ACCOUNT_ID])

        # Loop through snapshots and determine if snapshot start time is older than 14 days.
        old_snapshots = []
        for snapshot in snapshots['Snapshots']:
            start = snapshot['StartTime'].date()
            now = datetime.datetime.now().date()
            difference = now - start

            if difference.days > 14:
                old_snapshots.append(snapshot['SnapshotId'])

    except Exception as e:
        print(str(e))

    return old_snapshots

old_snapshots = get_old_snapshots()
pprint.pprint(old_snapshots)
