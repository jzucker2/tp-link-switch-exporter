# Configuration

## Example

### Quick with Environmental Variables

```
    ...
    environment:
      # like `http://10.0.1.1`
      - TP_LINK_SWITCH_IP=${TP_LINK_SWITCH_IP}
      # this you can make up to be whatever you want, like `Living Room Switch`
      - TP_LINK_SWITCH_NAME=${TP_LINK_SWITCH_NAME}
      - TP_LINK_SWITCH_USERNAME=${TP_LINK_SWITCH_USERNAME}
      # hopefully something secret!
      - TP_LINK_SWITCH_PASSWORD=${TP_LINK_SWITCH_PASSWORD}
```

### Multiple Switches with yaml config file

```yaml
switches:
  - switch_name: Living Room Switch
    switch_ip: http://10.0.1.1
    switch_username: admin
    switch_password: foo

  - switch_name: Kitchen Switch
    switch_ip: http://10.0.1.2
    switch_username: admin
    switch_password: bar
```

## Development

I am using [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation) to parse the YAML configs
