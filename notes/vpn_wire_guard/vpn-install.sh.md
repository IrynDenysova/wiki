Скопируй это в файл `vpn-install.sh` на сервере и запусти — он сам:

- установит WireGuard и qrencode,
    
- создаст серверный конфиг `wg0` (с NAT),
    
- добавит клиента **viktor**, выведет QR-код,
    
- откроет порт `51820/udp` в UFW,
    
- включит автозапуск и запустит VPN.
    

```bash
#!/usr/bin/env bash
# vpn-install.sh — WireGuard installer for Debian 13 (Trixie)
# Creates server wg0 + client "viktor" and prints QR for mobile.
set -euo pipefail

# --- Helpers ---------------------------------------------------------------
green() { printf "\033[32m%s\033[0m\n" "$*"; }
yellow() { printf "\033[33m%s\033[0m\n" "$*"; }
red()    { printf "\033[31m%s\033[0m\n" "$*"; }

require_root() {
  if [[ "${EUID}" -ne 0 ]]; then
    red "Please run as root: sudo bash vpn-install.sh"
    exit 1
  fi
}

cmd_exists() { command -v "$1" >/dev/null 2>&1; }

detect_iface() {
  # Default route interface
  ip route get 1.1.1.1 2>/dev/null | awk '/dev/{for(i=1;i<=NF;i++){if($i=="dev"){print $(i+1);exit}}}'
}

detect_public_ip() {
  # Best-effort
  curl -4s https://ipv4.icanhazip.com 2>/dev/null || curl -4s https://api.ipify.org 2>/dev/null || true
}

timestamp() { date +"%Y%m%d-%H%M%S"; }

# --- Main ------------------------------------------------------------------
require_root

green "=== WireGuard VPN installer (Debian 13) ==="

# Variables (you can change defaults here)
WG_IF="wg0"
WG_NET="10.8.0.0/24"
WG_SRV_IP="10.8.0.1"
WG_PORT="51820"
WG_DIR="/etc/wireguard"
CLIENT_NAME="viktor"
CLIENT_IP="10.8.0.2"
CLIENT_DNS="1.1.1.1"

IFACE="$(detect_iface || true)"
PUBLIC_IP="$(detect_public_ip || true)"

if [[ -z "${IFACE}" ]]; then
  yellow "Could not detect default network interface automatically."
  read -rp "Enter your WAN interface name (e.g. eth0): " IFACE
fi

if [[ -z "${PUBLIC_IP}" ]]; then
  yellow "Could not detect public IPv4 automatically."
  read -rp "Enter your public IPv4 (e.g. 185.182.184.40): " PUBLIC_IP
fi

green "Using interface: ${IFACE}"
green "Using public IP: ${PUBLIC_IP}"
green "WireGuard port: ${WG_PORT}/udp"

# Backup old config if exists
if [[ -d "${WG_DIR}" ]]; then
  BK="${WG_DIR}.bak.$(timestamp)"
  yellow "Existing ${WG_DIR} found. Backing up to ${BK}"
  mv "${WG_DIR}" "${BK}"
fi
mkdir -p "${WG_DIR}"
chmod 700 "${WG_DIR}"

green "[1/7] Installing packages..."
export DEBIAN_FRONTEND=noninteractive
apt update -y
apt install -y wireguard wireguard-tools qrencode ufw iptables curl

green "[2/7] Enabling IPv4 forwarding..."
SYSCTL_CONF="/etc/sysctl.d/99-wireguard-forward.conf"
echo "net.ipv4.ip_forward = 1" > "${SYSCTL_CONF}"
sysctl --system >/dev/null

green "[3/7] Generating keys..."
umask 077
wg genkey | tee "${WG_DIR}/server_private.key" | wg pubkey > "${WG_DIR}/server_public.key"
wg genkey | tee "${WG_DIR}/${CLIENT_NAME}_private.key" | wg pubkey > "${WG_DIR}/${CLIENT_NAME}_public.key"

SERVER_PRIV="$(cat ${WG_DIR}/server_private.key)"
SERVER_PUB="$(cat ${WG_DIR}/server_public.key)"
CLIENT_PRIV="$(cat ${WG_DIR}/${CLIENT_NAME}_private.key)"
CLIENT_PUB="$(cat ${WG_DIR}/${CLIENT_NAME}_public.key)"

green "[4/7] Writing server config ${WG_DIR}/${WG_IF}.conf ..."
cat > "${WG_DIR}/${WG_IF}.conf" <<EOF
[Interface]
Address = ${WG_SRV_IP}/24
ListenPort = ${WG_PORT}
PrivateKey = ${SERVER_PRIV}
SaveConfig = true
# NAT + forwarding rules (iptables; works with nft backend too)
PostUp   = iptables -A FORWARD -i %i -j ACCEPT; iptables -A FORWARD -o %i -j ACCEPT; iptables -t nat -A POSTROUTING -o ${IFACE} -j MASQUERADE
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -D FORWARD -o %i -j ACCEPT; iptables -t nat -D POSTROUTING -o ${IFACE} -j MASQUERADE

[Peer]
# ${CLIENT_NAME}
PublicKey = ${CLIENT_PUB}
AllowedIPs = ${CLIENT_IP}/32
EOF
chmod 600 "${WG_DIR}/${WG_IF}.conf"

green "[5/7] Creating client profile ${WG_DIR}/${CLIENT_NAME}.conf ..."
cat > "${WG_DIR}/${CLIENT_NAME}.conf" <<EOF
[Interface]
PrivateKey = ${CLIENT_PRIV}
Address = ${CLIENT_IP}/24
DNS = ${CLIENT_DNS}

[Peer]
PublicKey = ${SERVER_PUB}
Endpoint = ${PUBLIC_IP}:${WG_PORT}
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
EOF
chmod 600 "${WG_DIR}/${CLIENT_NAME}.conf"

green "[6/7] Opening firewall UDP ${WG_PORT}..."
ufw allow "${WG_PORT}"/udp || true
ufw reload || true

green "[7/7] Enabling and starting WireGuard..."
systemctl enable "wg-quick@${WG_IF}"
systemctl restart "wg-quick@${WG_IF}"

sleep 1
wg show || true

echo
green "=== Client config (${CLIENT_NAME}) ==="
echo "Location: ${WG_DIR}/${CLIENT_NAME}.conf"
echo
if cmd_exists qrencode; then
  yellow "QR code for mobile WireGuard (scan in the app):"
  qrencode -t ansiutf8 < "${WG_DIR}/${CLIENT_NAME}.conf"
else
  yellow "Install qrencode to print QR: apt install -y qrencode"
fi

echo
green "Done! Connect using the above config/QR."
yellow "If you change WAN interface later, update PostUp/PostDown in ${WG_DIR}/${WG_IF}.conf"
```

## Как запустить

```bash
nano vpn-install.sh     # вставь скрипт целиком и сохрани
sudo bash vpn-install.sh
```

После запуска увидишь:

- статус WireGuard,
    
- путь к файлу `viktor.conf`,
    
- QR-код для мобильного приложения WireGuard (Android/iOS).
    

## Что дальше

- Импортируй `viktor.conf` на ноутбуке/ПК (клиент WireGuard) **или** отсканируй QR в приложении на телефоне.
    
- Проверь подключение: на клиенте включи туннель — должен появиться интернет через сервер.
    

Если хочешь, добавлю команды: как **создать ещё одного клиента** (второй конфиг и QR) или как **полностью удалить/очистить** WireGuard (мы часть уже проходили).