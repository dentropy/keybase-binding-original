# ELasticsearch stuff

## Install

To run convert.js you require nodejs which can be installed from one of the links below

* [Download | Node.js](https://nodejs.org/en/download/)
* [nvm-sh/nvm: Node Version Manager - POSIX-compliant bash script to manage multiple active node.js versions](https://github.com/nvm-sh/nvm)
* [Installing Node.js via package manager | Node.js](https://nodejs.org/en/download/package-manager/)

# Instructions

1. Change line 3 of elastic.js to the export of your choice
2. Run the following command substituting a username and password

``` bash
npm install -g elasticdump

# Please update the output portion of the command with your elasticsearch credentials
elasticdump \
  --input=./user.json \
  --output=https://elastic:PASSWORD@elasticsearch.URL.TLD:9200/dentropydaemon \
  --type=data

```
