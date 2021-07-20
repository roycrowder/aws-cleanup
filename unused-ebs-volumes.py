#!/usr/bin/python3

import boto3, pprint

def get_unused_ebs_volumes():
    '''
    This function leverages the boto3 EC2 API to query for EBS volumes that are not attached to an instance.

    Returns a list of EBS volume IDs or an empty list.
    '''
    try:
        ebs_client = boto3.client('ec2')

        # Grab all the volumes
        unused_volumes = []
        ebs_volumes = ebs_client.describe_volumes()

        # Confirm valid response.
        # Loop through all described volumes looking for attachments.
        if ebs_volumes['ResponseMetadata']['HTTPStatusCode'] == 200:
            for ebs_volume in ebs_volumes['Volumes']:
                if len(ebs_volume['Attachments']) == 0 and ebs_volume['State'] == 'available':
                    unused_volumes.append(ebs_volume['VolumeId'])

    except Exception as e:
        print(str(e))

    return unused_volumes

unused_volumes = get_unused_ebs_volumes()
pprint.pprint(unused_volumes)
