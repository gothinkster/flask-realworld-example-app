# -*- mode: ruby -*-
# vi: set ft=ruby :
# Postgres config based on Davis Ford's config: https://gist.github.com/davisford/8000332

$script = <<SCRIPT
    #!/usr/bin/env bash

    # Update package list

    echo "Updating packages list"
    sudo add-apt-repository -y ppa:deadsnakes/ppa
    sudo apt-get update

    # Install necessary packages
    echo "Installing python and postgres"
    sudo apt-get install -y python3.7 python3-pip postgresql-10  

    # Setting postgres config
    echo "Fixing listen_addresses on postgresql.conf"
    sudo sed -i "s/#listen_address.*/listen_addresses '*'/" /etc/postgresql/9.5/main/postgresql.conf
    echo "Fixing postgres pg_hba.conf file"
    
    # Replace the ipv4 host line with the above line
    sudo cat >> /etc/postgresql/9.5/main/pg_hba.conf << EOF
    # Accept all IPv4 connections - FOR DEVELOPMENT ONLY!!!
    host    all         all         0.0.0.0/0             md5
EOF
    echo "Creating postgres vagrant role with password vagrant"
    # Create Role and login
    sudo -i -u postgres psql -c "create role vagrant with superuser login password 'vagrant';"

    #Install requeriments, assuming you have your Pipfile in the shared folder. If not, pipenv will create a new
    # virtual environment and a new Pipfile
    echo "Installing project dependencies"
    python3.7 -m pip install pipenv
    cd /vagrant
    python3.7 -m pipenv install --dev
SCRIPT

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "bento/ubuntu-18.04"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  config.vm.network "forwarded_port", guest: 5432, host: 55432, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision :shell, inline: $script
end
