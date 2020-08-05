# pipedev 2020-08-05 presentation: Infrastructure management

## Ansible

This tutorial is using Ansible! You should be able to do the same with another configuration management tool such as Puppet, Salt, Chef and etc.

https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html

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

Our ansible playbook creates the VM and inserts our ssh key so that we can ssh in!

```bash
source .env
ansible-playbook 01_create_vm.yml
```

and voila! If you go to https://cloud.digitalocean.com/droplets/ you should be able to see your VM! 2 GB Ram / 40 GB of disk /  with your ssh key

You can also ssh to it with 

```bash
ssh-add /Users/$USER/.ssh/digitalocean_rsa
ssh root@178.128.234.242
```

## Installing software on the image

Usually your IT department will have a blessed linux image that has some software baked into it.

We can do that using Ansible! In this example we will install `python3`, `htop` and `redis`.


