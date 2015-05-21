# ansible-module-gce-facts
Ansible module to gather [Google Cloud instance metadata](https://cloud.google.com/compute/docs/metadata) and return it as facts.
Until this module accepted by Ansible upstream, read on for usage instructions.

# Installation and usage

Clone this repository somewhere (`/full/path/to/ansible-module-gce-facts` in the examples below), and run Ansible with `--modules-dir` parameter:
```
# git clone https://github.com/br0ziliy/ansible-module-gce-facts.git /full/path/to/ansible-module-gce-facts
# ansible --modules-dir=/full/path/to/ansible-module-gce-facts -m gce_facts all
# ansible-playbook --modules-dir=/full/path/to/ansible-module-gce-facts playbook.yml
```

Alternatively you can export `ANSIBLE_LIBRARY` environment variable and run Ansible as usual:
```
# export ANSIBLE_LIBRARY=${ANSIBLE_LIBRARY}:/full/path/to/ansible-module-gce-facts
```
