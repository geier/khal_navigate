# Example plugin for khal showing how to add a new command

[khal](https://github.com/pimutils/khal/)

This plugin is based on [khal PR #1211](https://github.com/pimutils/khal/pull/1211)
by SOUKRAT Zakaria, CHOUMMIKH Meriam, and ELBAGHAZAOUI Azhar.

This will only work if you are currently running the
[develop/plugins branch](https://github.com/pimutils/khal/pull/1313).


Install the python project in this repository, e.g. 

```bash
pip install git+https://github.com/geier/khal_navigate
```

## Usage
This command supplies the new `navigate` command.

Example usage:

```sh
khal navigate -w 1 -m 12 -y 2023
```
