## Selecting multiple configs from a Config Group

Here: https://hydra.cc/docs/patterns/select_multiple_configs_from_config_group/



### Problem

In some scenarios, one may need to *select multiple configs* from the *same Config Group*.



### Solution

Use a **list of config names** as the value of the config group in the *Defaults List or in the command line*.



### Example

In this example, we configure a server. The server *can host multiple websites at the same time*.

`Config directory`
```
├── config.yaml
└── server
    ├── apache.yaml
    └── site
        ├── amazon.yaml
        ├── fb.yaml
        └── google.yaml
```

`config.yaml:`
```yaml
defaults:
  - server/apache
```

`server/apache.yaml:`
```yaml
defaults:
  - site:  # NOTE 2 here.
    - fb
    - google

host: localhost
port: 443
```

Server > sites:

`server/site/amazon.yaml`
```yaml
amazon:
  domain: amazon.com
```

`server/site/fb.yaml:`
```yaml
fb:
  domain: facebook.com
```

`server/site/google.yaml:`
```yaml
google:
  domain: google.com
```

Output:
```sh
$ python my_app.py
server:
  site:
    fb:
      domain: facebook.com
    google:
      domain: google.com
  host: localhost
  port: 443
```

**Override the selected sites from the command line by passing a list. e.g:**
```sh
$ python my_app.py 'server/site=[google,amazon]'
server:
  site:
    google:
      domain: google.com
    amazon:
      domain: amazon.com
  host: localhost
  port: 443
```



### Overriding packages

You can *relocate the package* of all the configs in the list. e.g:

> Swap `apache.yaml` content with `apache_https.yaml` content, then proceed.

`server/apache.yaml:`
```yaml
defaults:
  - site@https:  # NOTE the relocation.
    - fb
    - google
```

```sh
$ python my_app.py
server:
  https:  # NOTE.
    fb:
      domain: facebook.com
    google:
      domain: google.com
```

❓ I don't understand the below statement.

When overriding the selected configs of config groups with overridden packages you need to use the package. e.g:
```sh
$ python my_app.py server/site@server.https=amazon

server:
  https:
    amazon:
      domain: amazon.com
  host: localhost
  port: 443
```



### Implementation considerations

❓ I don't understand this entire section.

A nested list in the Defaults List is interpreted as a list of **non-overridable** configs:

`server/apache.yaml:`
```yaml
defaults:
  - site:
    - fb
    - google
```

`Equivalent to`
```yaml
defaults:
  - site/fb
  - site/google
```

All default package for all the configs in server/site is server.site. This example uses an explicit nesting level inside each of the website configs to prevent them stepping over one another:

`server/site/amazon.yaml`
```yaml
amazon:
  ...
```
