# celebalweek2


# Azure Infrastructure Deployment Guide

## Table of Contents
1. [Virtual Machines Deployment](#1-virtual-machines-deployment)
2. [App Service Plan & Web App](#2-app-service-plan--web-app)
3. [Azure Container Registry (ACR)](#3-azure-container-registry-acr)
4. [Container Instances & Groups](#4-container-instances--groups)
5. [Virtual Network Setup](#5-virtual-network-setup)
6. [Load Balancers](#6-load-balancers)
7. [Application Gateway](#7-application-gateway)
8. [DNS Configuration](#8-dns-configuration)
9. [Storage Account](#9-storage-account)

---

## 1. Virtual Machines Deployment

### Deploy Linux VM (Ubuntu 22.04)
```bash
az vm create   --name LinuxVM   --resource-group TrustedVM-RG   --image Ubuntu2204   --size Standard_B2s   --admin-username azureuser   --generate-ssh-keys   --public-ip-address-allocation static
```

**Post-Deployment:**

Get public IP:
```bash
az vm show --name LinuxVM --resource-group TrustedVM-RG --show-details --query publicIps -o tsv
```

SSH access:
```bash
ssh azureuser@<public-ip>
```

### Deploy Windows VM (Server 2022)
```bash
az vm create   --name WinVM   --resource-group TrustedVM-RG   --image Win2022Datacenter   --size Standard_B2ms   --admin-username azureuser   --admin-password "SecurePassword123!"   --public-ip-address-allocation static
```

**RDP Access:**
- Open `mstsc` on Windows
- Connect to: `<public-ip>`
- Use credentials: `azureuser/SecurePassword123!`

---

## 2. App Service Plan & Web App

### Create App Service Plan
```bash
az appservice plan create   --name MyAppPlan   --resource-group TrustedVM-RG   --sku B1   --is-linux
```

### Deploy Web App from GitHub
```bash
az webapp create   --name mywebapp-vivek   --resource-group TrustedVM-RG   --plan MyAppPlan   --runtime "PYTHON|3.9"

az webapp deployment source config   --name mywebapp-vivek   --resource-group TrustedVM-RG   --repo-url "https://github.com/VivekSingh12330/celebalweek2"   --branch main   --manual-integration
```

---

## 3. Azure Container Registry (ACR)

### Create ACR
```bash
az acr create   --name vivekacr   --resource-group TrustedVM-RG   --sku Basic   --admin-enabled true
```

### Push Image to ACR
```bash
docker pull nginx
docker tag nginx vivekacr.azurecr.io/nginx:v1
az acr login --name vivekacr
docker push vivekacr.azurecr.io/nginx:v1
```

---

## 4. Container Instances & Groups

### Single Container Instance
```bash
az container create   --name mynginx   --resource-group TrustedVM-RG   --image vivekacr.azurecr.io/nginx:v1   --ports 80   --dns-name-label vivek-nginx-aci
```

### Multi-Container Group (YAML)
```yaml
# multi-container.yaml
apiVersion: 2021-07-01
location: eastus
name: app-with-redis
properties:
  containers:
  - name: nginx
    properties:
      image: vivekacr.azurecr.io/nginx:v1
      ports:
      - port: 80
  - name: redis
    properties:
      image: mcr.microsoft.com/oss/redis/redis:latest
      ports:
      - port: 6379
  osType: Linux
  ipAddress:
    type: Public
    ports:
    - protocol: tcp
      port: 80
    dnsNameLabel: vivek-multi-app
```

**Deploy with:**
```bash
az container create   --resource-group TrustedVM-RG   --file multi-container.yaml
```

---

## 5. Virtual Network Setup

### Create VNet with Subnets
```bash
az network vnet create   --name MainVNet   --resource-group TrustedVM-RG   --address-prefixes 10.0.0.0/16

az network vnet subnet create   --name Subnet-1   --vnet-name MainVNet   --resource-group TrustedVM-RG   --address-prefixes 10.0.1.0/24

az network vnet subnet create   --name Subnet-2   --vnet-name MainVNet   --resource-group TrustedVM-RG   --address-prefixes 10.0.2.0/24
```

---

## 6. Load Balancers

### Internal Load Balancer
```bash
az network lb create   --name MyIntLB   --resource-group TrustedVM-RG   --sku Standard   --vnet-name MainVNet   --subnet Subnet-1   --private-ip-address 10.0.1.100
```

---

## 7. Application Gateway

### Create Gateway
```bash
az network application-gateway create   --name MyAppGateway   --resource-group TrustedVM-RG   --capacity 2   --vnet-name MainVNet   --subnet Subnet-2   --public-ip-address MyGatewayIP
```

---

## 8. DNS Configuration

### Create Private DNS Zone
```bash
az network private-dns zone create   --name mydomain.local   --resource-group TrustedVM-RG
```

---

## 9. Storage Account

### Create Storage Account
```bash
az storage account create   --name vivstorage   --resource-group TrustedVM-RG   --location eastus   --sku Standard_LRS
```

### Create File Share
```bash
az storage share create   --name myshare   --account-name vivstorage
```

---

## Verification & Cleanup

### List All Resources
```bash
az resource list --resource-group TrustedVM-RG -o table
```

### Delete Resource Group
```bash
az group delete --name TrustedVM-RG --yes
```
