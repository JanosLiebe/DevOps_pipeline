#!/usr/bin/env python

import sys
import json
from awswrapper import aws_ec2

class ActiveInstanceNotFoundException(Exception):
    pass

def list_hosts():

    def filter_active(instances):
        active = filter(lambda x: x['Instances'][0]['State']['Name'] == 'running', instances['Reservations'])
        if len(active) == 0:
            raise ActiveInstanceNotFoundException('Active instance not found. Did you create the stack?')
        elif len(active) > 1:
            raise MultipleInstancesFoundException('Multiple active instances found. Go see a cloudformation stack doctor.')
        return active[0]['Instances'][0]

    #jenkins_instances = aws_ec2('describe-instances --filter Name=tag:Name,Values=StackJenkinsInstance')
    #jenkins_instance = filter_active(jenkins_instances)
    #jenkins_ip = jenkins_instance['PublicIpAddress']

    aws_server_instances = aws_ec2('describe-instances --filter Name=tag:Name,Values=StackServerInstance')
    aws_server_instance = filter_active(aws_server_instances)
    aws_server_ip = aws_server_instance['PublicIpAddress']

    return  {
                "all": {
                    #"hosts": ["jenkins", "webserver"],
                    "hosts": ["aws_server"],
                    "vars": {
                        "ansible_ssh_port": "22",
                        "ansible_ssh_user": "ubuntu",
                        "ansible_ssh_private_key_file": "janos_aws.pem",
                    }
                },
                # _meta is for adding host vars
                # If _meta is present, script is not called with --host <hostname>
                # for each host, resulting in a major performance increase
                "_meta" : {
                    "hostvars" : {
                        #"jenkins": {
                        #    "ansible_connection": "ssh",
                        #    "ansible_ssh_host": jenkins_ip,
                        #},
                        "aws_server": {
                            "ansible_connection": "ssh",
                            "ansible_ssh_host": aws_server_ip,
                        },
                    }
                }
            }

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '--list':
        print json.dumps(list_hosts())
    elif len(sys.argv) == 2 and sys.argv[1] == '--test':
        print json.dumps(list_hosts(), indent=4, sort_keys=True)
