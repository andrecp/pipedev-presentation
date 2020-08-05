# pipedev 2020-08-05 presentation: Infrastructure management

This is a hands-on tutorial on infrastructure management for a VFX pipeline meetup in Vancouver.

## Ansible

This tutorial is using Ansible! You should be able to do the same with another configuration management tool such as Puppet, Salt, Chef and etc.

https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html

We're using version 2.9.4!

## Digital Ocean

This tutorial is using digital ocean, you should be able to use Virtualbox / VMware or any other cloud provider.

My referral link if you want to use is https://m.do.co/c/73d2e2dcd335

# Step by step

## Digital Ocean Setup

1. Register at digital ocean, create an account, set two factor authentication, set a budget limit to alert you once you're getting close to it (for example 20 dollars per month).

2. Create an ssh key at https://cloud.digitalocean.com/account/security?i=ce2e94 so that you do not need to type your password to connect to VMs!

3. Create a new API Access Token (https://www.digitalocean.com/docs/apis-clis/api/create-personal-access-token/)

4. Create a .env file and export the access token to be used by Ansible, it is in `.gitignore` so you have no risk of commiting it by mistake!

### .env example

Be careful! This is the equivalent to your digital ocean account/password.

```bash
export DO_API_TOKEN=cbf9930d45928499d0139f493378...
export SSH_KEY_ID=280...
```

#### Finding your ssh key id

```bash
source .env
curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer $DO_API_TOKEN" "https://api.digitalocean.com/v2/account/keys"
```

## 01 - Create a VM

We have to start with a VM! In this case we will be using the create_vm.yml playbook which uses the ansible module for digital ocean. There are ansible modules for most cloud providers.

https://docs.ansible.com/ansible/latest/modules/digital_ocean_droplet_module.html


### Choosing a Linux image

This is a important step in the journey of creating our studio! We will be using CentOS8.

Look at their API for the available images: https://developers.digitalocean.com/documentation/v2/#images.

### Running the playbook

Our ansible playbook creates the VM and inserts our ssh key so that we can ssh in! It is important to note that *ansible is immutable*, that means you can re-run this playbook as many times as you want and Ansible will simply no-op if it is in the desired state already.

```bash
source .env
ansible-playbook 01_create_vm.yml
```

Voila! If you go to https://cloud.digitalocean.com/droplets/ you should be able to see your VM! 2 GB Ram / 40 GB of disk / 2 cores with your ssh key

You can also ssh to it with 

```bash
ssh-add /Users/$USER/.ssh/digitalocean_rsa
ssh root@XXX.XXX.XXX.XXX  # Your IP
```

It is worth noting that in a real life scenario we would'nt necessairly do things with the root ssh key. 

Users would be managed via something like LDAP and a sudoers list would be maintained allowing users (or more commonly groups) to execute sudo only for what they absolutely need to.

## Installing software on the image

Usually your IT department will have a blessed linux image that has some software baked into it.

We can do that using Ansible! In this example we will install `python3`, `python3-flask`, `htop` and `redis`.

### First add a hosts file

A hosts file in Ansible has your hosts! You can organize it in many ways and use either `ini` or `yml` format.

Create a `hosts.ini` file with IP of your VM under the group `pipedev`.

```
[pipedev]
XXX.XXX.XXX.XXX  # Your IP
```

### Install the software packages

Centos8 replaced `yum` with `dnf`!

```bash
source .env
ansible-playbook -i hosts.ini 02_install_software.yml
```

Of course this list is *much* bigger for your typical VFX studio with many many dependencies!

We won't do it here but you can export your Linux image as a new Custom Linux Image so that you don't need to re-install the base level software every time you create a new machine in your studio.

You can also run ansible as a cron job doing the equivalent of `git pull` a specific tag and then running `ansible-playbook` to ensure that the machine is always up-to-date.

## Install the app

Our app architecture is quite simple! It is the hello world service.

### Architecture

Flask app -> Redis DB

Each request to `/` returns hello world and keeps a request count in redis.
Each request to `/count` returns the count.

We're using `systemd` to manage the flask app and redis!

### Install the application

Create the folders, copy the files, start the servers!

```bash
source .env
ansible-playbook -i hosts.ini 03_install_app.yml
```

If we have one or 10 servers all we need to do to horizontally scale the app is add more hosts to `hosts.ini`! (Of course we do not have a load balancer set up or service discovery)

## Site

It is common to have a single playbook that imports every playbook so that you do not need to run every single step individually!

## Destroy VM

We don't want to be billed for this prototype too much! Let's destroy it by passing the droplet_id as a variable.

```bash
source .env
ansible-playbook 05_destroy_vm.yml -e"droplet_id=202731550"
```

# Final notes

This is by no means a production ready setup! Please use only as a simple application reference.

We barely scratched the surface of what Ansible is capable of. I recommend having a look on ansible `roles` and the `vars` system next!
