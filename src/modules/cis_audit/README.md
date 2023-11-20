# Run cis audit tool 

```
ansible_cis
|   README.md
|   run_cis_tool.yml
|   ubuntu_cis_audit.yml
|   ansible.cfg
|   
+---environment
|       group_vars
|           common_param.yml
|           debian_family_param.yml
|       hosts     
```

## Steps to run cis audit tool:
    -> Install ansible
    -> Install prerequisites 
        pip install -r docs/requirements.txt
    -> Update host and password details in src/modules/cis_audit/environment/hosts file:
            ansible_ssh_user and ansible_sudo_pass
    -> Run playbook to execute cis tool

Run below command from src folder:
cmd> cd src/
cmd> ansible-playbook -i modules/cis_audit/environment/hosts modules/cis_audit/run_cis_tool.yml --verbose
