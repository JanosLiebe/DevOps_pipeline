### DevOps Pipeline Demo
** Uses REST_Server implementation as server under development.

### Cloud virtual machines with AWS cloudformation stack
**Create the stack using ansible:**  
```
ansible-playbook -i inventories/localhost playbooks/create_aws_stack.yml
```
**Create the stack using AWS client:**
```
aws cloudformation create-stack --stack-name mystack --template-body file://playbooks/roles/aws_stack/files/stack.json --parameters ParameterKey=KeyPairName,ParameterValue=janos_aws.pem
```

### Ansible tags
Select **aws_hosts.py** inventory to provision the aws stack you created:
```
ansible-playbook -i inventories/aws_hosts.py --tags server_base playbooks/provision.yml
ansible-playbook -i inventories/aws_hosts.py --tags robotframework playbooks/provision.yml
ansible-playbook -i inventories/aws_hosts.py --tags jenkins playbooks/provision.yml
ansible-playbook -i inventories/aws_hosts.py --tags webserver playbooks/provision.yml
