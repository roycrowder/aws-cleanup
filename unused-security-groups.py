#!/usr/bin/python3

import boto3, pprint

# To think about:
#  - include exclusion list via db table, etc.

def get_unused_security_groups():
    '''
    This function leverages the boto3 EC2 API to query for all security groups within an account region
    and determine which ones are not attached (used) by an EC2 instance.

    Returns a list of security group IDs or an empty list.
    '''
    # TODO: Could include an exclusion list for security group exceptions.
    try:
        ec2_resource = boto3.resource('ec2')

        # The ec2 resource’s describe instances method automatically handles pagination for us.
        security_groups = ec2_resource.security_groups.all()
        ec2_instances = ec2_resource.instances.all()

        # Grab security group IDs using list comprehension, we make it a set to enforce uniqueness
        security_group_ids = set([security_group.id for security_group in security_groups])

        # Loop through instances and grab a unique list of their security group IDs.
        ec2_instances_security_group_ids = []

        for ec2_instance in ec2_instances:
            for security_group in ec2_instance.security_groups:
                ec2_instances_security_group_ids.append(security_group.get('GroupId'))
    except Exception as e:
        print(str(e))

    # Establish a unique list of instance security group IDs.
    ec2_instances_security_group_ids = set(ec2_instances_security_group_ids)

    # Determine list of unused security groups
    unused_security_group_ids = security_group_ids - ec2_instances_security_group_ids

    return unused_security_group_ids

unused_sgs = get_unused_security_groups()
pprint.pprint(unused_sgs)
