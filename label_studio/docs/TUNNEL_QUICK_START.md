# Quick Start: Cloudflare Tunnel Setup

Follow these steps in order.

## 1. Install cloudflared
```bash
wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb && sudo dpkg -i cloudflared-linux-amd64.deb
cloudflared --version
```

## 2. Login
```bash
cloudflared tunnel login
```

## 3. Create Tunnel
```bash
cloudflared tunnel create labelstudio-tunnel
```
Save the tunnel ID.

## 4. Configure Hostname (Dashboard)
Add public hostname:
- Subdomain: labelstudio
- Service: `label-studio:8080`

## 5. Get Token
Copy token from install connector snippet.

## 6. Create `tunnel.env`
```bash
cd /home/rafa/PycharmProjects/AnimalDetector/label_studio
cp tunnel.env.example tunnel.env
nano tunnel.env
```
Add:
```
TUNNEL_TOKEN=<token>
LABEL_STUDIO_HOSTNAME=https://label.montedelavilla.org
```

## 7. Start
```bash
docker compose up -d
```

## 8. Verify
```bash
docker compose logs cloudflared | grep -i registered
curl -I https://label.montedelavilla.org
```
Expect 302 redirect.

## 9. External Test
Open from phone (mobile data) to confirm accessibility.

## 10. Security Check
```bash
git status
```
`tunnel.env` should NOT appear.

## Troubleshooting
- Recheck token format
- Inspect logs: `docker compose logs cloudflared --tail=100`
- Confirm hostname in dashboard matches env file

Done 🎉
# Cloudflare Tunnel Setup for Label Studio

This guide explains how the Cloudflare Zero Trust tunnel is configured to provide secure external access to Label Studio.

## Overview

The setup uses Cloudflare Tunnel to securely expose Label Studio at `https://label.montedelavilla.org` without opening ports on your firewall.

## Architecture

```
Internet → Cloudflare Edge → Cloudflare Tunnel (cloudflared) → Label Studio (Docker)
```

## Configuration Files

### 1. `tunnel.env` (PROTECTED - Not in Git)
Contains sensitive tunnel credentials:
```env
TUNNEL_TOKEN=<your-tunnel-token>
LABEL_STUDIO_HOSTNAME=https://label.montedelavilla.org
```

⚠️ IMPORTANT: This file contains sensitive credentials and is excluded from Git via `.gitignore`.

### 2. `config.yml` (PROTECTED - Not in Git)
Defines tunnel ingress rules:
```yaml
tunnel: 3663beb6-957e-4620-99bd-65ac5b9187c1
credentials-file: /etc/cloudflared/creds.json

ingress:
  - hostname: label.montedelavilla.org
    service: http://label-studio:8080
  - service: http_status:404
```

⚠️ IMPORTANT: The `tunnel` field must use the tunnel ID (UUID), not the tunnel name.

### 3. `tunnel.env.example`
Template for creating your own `tunnel.env` file.

## Setup Instructions

### Prerequisites
- Cloudflare account with domain `montedelavilla.org`
- Docker and Docker Compose installed
- `cloudflared` CLI installed on your system

### Step 1: Authenticate with Cloudflare
```bash
cloudflared tunnel login
```
This creates `~/.cloudflared/cert.pem`.

### Step 2: Create the Tunnel
```bash
cloudflared tunnel create labelstudio-tunnel
```
This creates credentials at `~/.cloudflared/3663beb6-957e-4620-99bd-65ac5b9187c1.json`.

### Step 3: Configure DNS Route
```bash
cloudflared tunnel route dns labelstudio-tunnel label.montedelavilla.org
```
This creates a CNAME record pointing `label.montedelavilla.org` to the tunnel.

### Step 4: Get the Tunnel Token
```bash
cloudflared tunnel token labelstudio-tunnel
```
Copy the token output.

### Step 5: Create Configuration Files
1. Copy `tunnel.env.example` to `tunnel.env`:
   ```bash
   cp tunnel.env.example tunnel.env
   ```

2. Edit `tunnel.env` and paste your tunnel token:
   ```env
   TUNNEL_TOKEN=<paste-token-here>
   LABEL_STUDIO_HOSTNAME=https://label.montedelavilla.org
   ```

3. The `config.yml` file should already exist with the correct configuration.

### Step 6: Start Services
```bash
docker compose up -d
```

### Step 7: Verify
Check that all services are running:
```bash
docker compose ps
docker compose logs cloudflared
```

Verify the tunnel has active connections:
```bash
cloudflared tunnel info labelstudio-tunnel
```

Test external access:
```bash
curl -I https://label.montedelavilla.org
```

## Services

The Docker Compose stack includes:

1. **label-studio**: The main Label Studio application
2. **cloudflared**: Cloudflare Tunnel connector
3. **db**: PostgreSQL database for Label Studio

## Troubleshooting

### Tunnel Not Connecting
```bash
# Check cloudflared logs
docker compose logs cloudflared

# Verify tunnel status
cloudflared tunnel info labelstudio-tunnel

# Restart the tunnel
docker compose restart cloudflared
```

### Site Not Loading (Shows Blank or 404)
**Common Issue**: The `config.yml` file must use the tunnel ID (UUID), not the tunnel name.

❌ **Wrong**:
```yaml
tunnel: labelstudio-tunnel
```

✅ **Correct**:
```yaml
tunnel: 3663beb6-957e-4620-99bd-65ac5b9187c1
```

After fixing, restart the cloudflared service:
```bash
docker compose restart cloudflared
```

### Label Studio Not Accessible
```bash
# Check Label Studio logs
docker compose logs label-studio

# Verify Label Studio is running
curl http://localhost:8080

# Check if hostname is configured correctly
docker compose exec label-studio env | grep LABEL_STUDIO_HOSTNAME
```

### CSRF Verification Failed (403 Forbidden)
**Common Issue**: Label Studio shows "CSRF verification failed. Request aborted." when trying to log in through the tunnel.

**Solution**: Add the following environment variables to the `label-studio` service in `docker-compose.yml`:
```yaml
environment:
  - LABEL_STUDIO_HOST=https://label.montedelavilla.org
  - CSRF_TRUSTED_ORIGINS=https://label.montedelavilla.org
```

After adding these, restart Label Studio:
```bash
docker compose restart label-studio
```

Clear your browser cookies for the site and try again.

### DNS Not Resolving
```bash
# Check DNS record
dig label.montedelavilla.org

# Verify route
cloudflared tunnel route list
```

## Security Notes

1. **Tunnel Token**: The `TUNNEL_TOKEN` in `tunnel.env` is sensitive. Never commit it to Git.
2. **Credentials File**: The tunnel credentials at `~/.cloudflared/*.json` should be protected.
3. **HTTPS**: All traffic goes through Cloudflare's edge, providing automatic HTTPS.
4. **No Open Ports**: No ports need to be opened on your firewall.

## Files Protected from Git

The following files are excluded via `.gitignore`:
- `tunnel.env` - Contains tunnel token
- `config.yml` - Contains tunnel configuration
- `data/` - Label Studio data directory

## Monitoring

### Check Tunnel Status
```bash
cloudflared tunnel info labelstudio-tunnel
```

### View Live Logs
```bash
docker compose logs -f cloudflared
docker compose logs -f label-studio
```

### View Metrics
The tunnel exposes metrics on port 20241 (accessible only within the container).

## Updating

### Update Cloudflared
```bash
docker compose pull cloudflared
docker compose up -d cloudflared
```

### Update Label Studio
```bash
docker compose pull label-studio
docker compose up -d label-studio
```

## Backup

### Backup Label Studio Data
```bash
# Backup database
docker compose exec db pg_dump -U postgres labelstudio > labelstudio_backup.sql

# Backup data directory
tar -czf labelstudio_data_backup.tar.gz data/
```

### Restore Label Studio Data
```bash
# Restore database
cat labelstudio_backup.sql | docker compose exec -T db psql -U postgres labelstudio

# Restore data directory
tar -xzf labelstudio_data_backup.tar.gz
```

## Access

- **Public URL**: https://label.montedelavilla.org
- **Local URL**: http://localhost:8080

## Support

For issues with:
- **Cloudflare Tunnel**: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/
- **Label Studio**: https://labelstud.io/guide/

## Testing the Setup

Run these commands to verify everything is working:

```python
import unittest
import requests
from typing import Optional

class TunnelHealthChecker:
    def __init__(self, public_url: str) -> None:
        self.public_url = public_url
    def is_accessible(self) -> bool:
        try:
            response = requests.head(self.public_url, timeout=10, allow_redirects=False)
            return response.status_code in [200, 301, 302]
        except Exception:
            return False
    def get_status_code(self) -> Optional[int]:
        try:
            response = requests.head(self.public_url, timeout=10, allow_redirects=False)
            return response.status_code
        except Exception:
            return None

class TestTunnelSetup(unittest.TestCase):
    def setUp(self) -> None:
        self.checker = TunnelHealthChecker("https://label.montedelavilla.org")
    def test_tunnel_is_accessible(self) -> None:
        self.assertTrue(self.checker.is_accessible())
    def test_returns_redirect_to_login(self) -> None:
        status_code = self.checker.get_status_code()
        self.assertEqual(status_code, 302)

if __name__ == "__main__":
    unittest.main()
```

