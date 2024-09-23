#importing the important libraries and credential

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient

print(
    "Provisioning a virtual machine...it might take a \
minute or two."
)

#Acquire a credential object
credential = DefaultAzureCredential()

#Retrieve subscription ID from environment.
subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]

#provisioning a resource group

#obtain the management object
resource_client = ResourceManagementClient(credential,subscription_id)

#Constants we need in multiple places: the resource group name and
#the region in which we provision resources. you can change these values however you want.
Resource_Group_Name = "Data_Engineer"
Location = "westeurope"

#provision the resource group.
rGroup_result = resource_client.resource_groups.create_or_update(
    Resource_Group_Name,{"location": Location}
)

print(
    f"Provisioned resource group {rGroup_result.name} in the \{rGroup_result.location} region"
)

#provision a virtual network

# Network and IP address names
VIRTUAL_NETWORK_NAME = "YatharthGautam-vnet"
IP_CONFIG_NAME = "yatharth-ip-config"
SUBNET_NAME = "yatharth-subnet"
NIC_NAME = "yatharth-nic"
IP_NAME = "yatharth-ip"
NSG_NAME = "yatharth-nsg"

# Obtaining management object for networks
network_client = NetworkManagementClient(credential, subscription_id)

# Provision the virtual network and wait for completion
poller = network_client.virtual_networks.begin_create_or_update(
    Resource_Group_Name,
    VIRTUAL_NETWORK_NAME,
    {
        "location": Location,
        "address_space": {"address_prefixes": ["10.0.0.0/16"]},
    },
)

vnet_result = poller.result()

print(
    f"Provisioned virtual network {vnet_result.name} with address \
prefixes {vnet_result.address_space.address_prefixes}"
)

nsg_poller = network_client.network_security_groups.begin_create_or_update(
    Resource_Group_Name,
    NSG_NAME,
    {"location": Location}
)
nsg_result = poller.result()

print(f"Network Security Group {nsg_result.name} with ID {nsg_result.id} created successfully")


nsg_result = nsg_poller.result()


#Provisioning the subnet and waiting for completion


poller = network_client.subnets.begin_create_or_update(
    Resource_Group_Name,
    VIRTUAL_NETWORK_NAME,
    SUBNET_NAME,
    subnet_parameters={
        "address_prefix": "10.0.0.0/24",
        "network_security_group": {"id": nsg_result.id}
        }
)
subnet_result = poller.result()
print(f"Associating NSG {nsg_result.id} with the subnet")

print(
    f"Provisioned virtual subnet {subnet_result.name} with address \
prefix {subnet_result.address_prefix}"
)

#provisioning the IP address and wait for completion

poller = network_client.public_ip_addresses.begin_create_or_update(
    Resource_Group_Name,
    IP_NAME,
    {
        "location": Location,
        "sku": {"name": "Standard"},
        "public_ip_allocation_method": "Static",
        "public_ip_address_version": "IPV4",
    },
)

ip_address_result = poller.result()

print(
    f"Provisioned public IP address {ip_address_result.name} \
with address {ip_address_result.ip_address}"
)

#Provisioning the network interface client

poller = network_client.network_interfaces.begin_create_or_update(
    Resource_Group_Name,
    NIC_NAME,
    {
        "location": Location,
        "ip_configurations": [
            {
                "name": IP_CONFIG_NAME,
                "subnet": {"id": subnet_result.id},
                "public_ip_address": {"id": ip_address_result.id},
            }
        ],
    },
)

nic_result = poller.result()

print(f"Provisioned network interface client {nic_result.name}")

#provisioning the VM
#Obtaining the mgmt object for VM

compute_client = ComputeManagementClient(credential, subscription_id)

VM_NAME = "VM-yatharth"
USERNAME = "yatharth-DE"
PASSWORD = "Yatharth@123"

print(
    f"Provisioning virtual machine {VM_NAME}; this operation might \
take a few minutes."
)

#provisioning the VM specifying only minimal arguments

poller = compute_client.virtual_machines.begin_create_or_update(
    Resource_Group_Name,
    VM_NAME,
    {
        "location": Location,
        "storage_profile": {
            "image_reference": {
                "publisher": "Canonical",
                "offer": "UbuntuServer",
                "sku": "16.04.0-LTS",
                "version": "latest",
            }
        },
        "hardware_profile": {"vm_size": "Standard_DS1_v2"},
        "os_profile": {
            "computer_name": VM_NAME,
            "admin_username": USERNAME,
            "admin_password": PASSWORD,
        },
        "network_profile": {
            "network_interfaces": [
                {
                    "id": nic_result.id,
                }
            ]
        },
    },
)

vm_result = poller.result()

print(f"Provisioned virtual machine {vm_result.name}")
