Vagrant.configure("2") do |config|
  config.hostmanager.enabled = true 
  config.hostmanager.manage_host = true
  
  ### Ubuntu VM1 ####
  config.vm.define "ubuntu01" do |ubuntu01|
    ubuntu01.vm.box = "ubuntu/jammy64"
    ubuntu01.vm.hostname = "ubuntu01"
    ubuntu01.vm.network "private_network", ip: "192.168.56.15"
    ubuntu01.vm.provider "virtualbox" do |vb|
      vb.memory = "600"
    end
  end
  
  ### Ubuntu VM2 ####
  config.vm.define "ubuntu02" do |ubuntu02|
    ubuntu02.vm.box = "ubuntu/jammy64"
    ubuntu02.vm.hostname = "ubuntu02"
    ubuntu02.vm.network "private_network", ip: "192.168.56.14"
    ubuntu02.vm.provider "virtualbox" do |vb|
      vb.memory = "600"
    end
  end

end

