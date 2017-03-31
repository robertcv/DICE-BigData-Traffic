# BigData-Transport

This project is a real world example of how to use DICE tools. Its main
purpose is to collect, store and process transportation data in
Ljubljana.

The project contains:

* **python_package** – Set of python scripts (collectors) combined into a python
module for ease of installation via pip and ease of usage via the CLI tool. 
Collectors collect data from different sources and foreword them to Apache
Kafka.

* **virtual_machines** – Set of Vagrantfiles and bash scripts for
deploying VMs for testing purposes. Later those will be replaced with
blueprints.
