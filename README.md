# ansible-module-gce-facts
Ansible module to gather Google Cloud instance metadata and return it as facts

This is an alpha-version of the module. Known issues:

- facts variable names are pretty ugly at this moment:

```json
{
"ansible_gce_network_interfaces_0_access_configs_0_external_ip": "100.200.255.255",
"ansible_gce_network_interfaces_0_access_configs_0_type": "ONE_TO_ONE_NAT",
"ansible_gce_network_interfaces_0_ip": "10.240.2.255",
}
```

- values are not sanitized, example:
```
"ansible_gce_zone": "projects/111111111111/zones/us-central1-b"
```

Let me know if this module might be useful for you so I have some motivation to make it smarter (I will do it eventually anyway, but it might be not very fast :) )
