#!/bin/bash

CHEF_DIR=chef-repository
CONCURRENCY=3
DESTROY_STRATEGY=always

cp ../kitchen.local.yml ${CHEF_DIR}/.kitchen.local.yml

cd $CHEF_DIR

[ -h test ] || ln -s cookbooks/DICETraffic/test
[ -h .kitchen.yml ] || ln -s cookbooks/DICETraffic/.kitchen.yml

kitchen test --concurrency=$CONCURRENCY --destroy=$DESTROY_STRATEGY
