# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

$script = <<EOF
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y --force-yes python-setuptools python-mock python-unittest2 python-wheel
EOF

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "ubuntu/trusty64"

  config.vm.hostname = "pysss.local"

  config.vm.provision "shell", inline: $script

end
