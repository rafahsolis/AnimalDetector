# Cloudflare Zero Trust Tunnel Setup for Label Studio

This guide will help you set up a Cloudflare Zero Trust tunnel to securely access your Label Studio instance from anywhere.

## Prerequisites

- Cloudflare account (free tier works)
- A domain managed by Cloudflare
- Docker and Docker Compose installed

## Step-by-Step Setup

### Step 1: Install cloudflared CLI

**On Linux:**
```bash
wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb
```

**Verify installation:**
```bash
cloudflared --version
```

### Step 2: Authenticate with Cloudflare

```bash
cloudflared tunnel login
```

This will open a browser window. Log in to your Cloudflare account and select the domain you want to use.

### Step 3: Create a Tunnel

```bash
cloudflared tunnel create labelstudio-tunnel
```

This will create a tunnel and output a tunnel ID and credentials file location.
**Important:** Save the tunnel ID - you'll need it.

### Step 4: Get Your Tunnel Token

You have two options:

#### Option A: Using Cloudflare Dashboard (Recommended for beginners)
1. Go to https://one.dash.cloudflare.com/
2. Navigate to **Access** → **Tunnels**
3. Find your tunnel and click **Configure**
4. Under **Public Hostname**, add:
   - **Subdomain:** labelstudio (or your choice)
   - **Domain:** yourdomain.com
   - **Service Type:** HTTP
   - **URL:** label-studio:8080
5. Click **Save**
6. Go back to the tunnel overview and copy the **Install and run connector** token

#### Option B: Using CLI
```bash
cloudflared tunnel route dns labelstudio-tunnel labelstudio.yourdomain.com
```

Then get the token:
```bash
cloudflared tunnel token labelstudio-tunnel
```

### Step 5: Configure Your Environment

1. Copy the example environment file:
```bash
cd label_studio
cp tunnel.env.example tunnel.env
```

2. Edit `tunnel.env` and add your tunnel token:
```bash
TUNNEL_TOKEN=your-actual-tunnel-token-here
```

**Important:** Never commit `tunnel.env` to git! It's already in `.gitignore`.

### Step 6: Update Label Studio Hostname

Edit your `tunnel.env` file to also include:
```bash
LABEL_STUDIO_HOSTNAME=https://labelstudio.yourdomain.com
```

### Step 7: Start Your Services

```bash
docker-compose up -d
```

### Step 8: Verify the Tunnel

1. Check tunnel status:
```bash
docker-compose logs cloudflared
```

2. Visit your domain: `https://labelstudio.yourdomain.com`

## Security Notes

- The tunnel uses Cloudflare's network for encryption and DDoS protection
- Your `tunnel.env` file is gitignored and will never be committed
- You can add Cloudflare Access policies for additional authentication
- Consider enabling Cloudflare Access to require login before accessing Label Studio

## Troubleshooting

### Tunnel won't connect
- Verify your token is correct in `tunnel.env`
- Check docker logs: `docker-compose logs cloudflared`
- Ensure no firewall is blocking outbound connections on port 443

### 502 Bad Gateway
- Ensure label-studio container is running: `docker-compose ps`
- Check that the service name and port match in your tunnel configuration

### Images not loading in Label Studio
- Verify `LABEL_STUDIO_HOSTNAME` is set to your public URL
- Check that the datasets volume is properly mounted

## Additional Security: Cloudflare Access

To add authentication before anyone can access your Label Studio:

1. Go to Cloudflare Zero Trust Dashboard
2. Navigate to **Access** → **Applications**
3. Click **Add an application** → **Self-hosted**
4. Configure:
   - **Application name:** Label Studio
   - **Subdomain:** labelstudio
   - **Domain:** yourdomain.com
5. Create access policies (e.g., require email login)

## Updating the Tunnel

If you need to change configuration:
```bash
# Edit docker-compose.yml or tunnel.env
docker-compose down
docker-compose up -d
```

## Removing the Tunnel

```bash
# Stop services
docker-compose down

# Delete tunnel from Cloudflare
cloudflared tunnel delete labelstudio-tunnel
```

