Да, давай сделаем удобный скрипт, который будет добавлять **любое количество новых клиентов** к твоему уже работающему WireGuard.

Скрипт:

- создаёт ключи для нового клиента,
    
- дописывает его в `wg0.conf` (секция `[Peer]`),
    
- создаёт отдельный файл-конфиг клиента `/etc/wireguard/<имя>.conf`,
    
- перезапускает `wg-quick@wg0`,
    
- показывает QR-код (если есть `qrencode`).
    

---

## 📝 Скрипт `wg-add-client.sh`

На сервере:

```bash
sudo nano /usr/local/bin/wg-add-client.sh
```

Вставь полностью:

```bash
#!/usr/bin/env bash
# wg-add-client.sh — добавить нового клиента WireGuard к существующему wg0
# Использование:
#   sudo wg-add-client.sh client_name 10.8.0.X
# пример:
#   sudo wg-add-client.sh phone2 10.8.0.3

set -euo pipefail

green() { printf "\033[32m%s\033[0m\n" "$*"; }
yellow() { printf "\033[33m%s\033[0m\n" "$*"; }
red()    { printf "\033[31m%s\033[0m\n" "$*"; }

require_root() {
  if [[ "${EUID}" -ne 0 ]]; then
    red "Запусти скрипт от root: sudo $0 client_name 10.8.0.X"
    exit 1
  fi
}

cmd_exists() { command -v "$1" >/dev/null 2>&1; }

WG_IF="wg0"
WG_DIR="/etc/wireguard"
DNS_DEFAULT="1.1.1.1"

require_root

if [[ $# -lt 2 ]]; then
  red "Нужно указать имя клиента и его IP в VPN-сети."
  echo "Пример:"
  echo "  sudo $0 wife 10.8.0.3"
  exit 1
fi

CLIENT_NAME="$1"
CLIENT_IP="$2"

if [[ ! -d "${WG_DIR}" ]]; then
  red "Каталог ${WG_DIR} не найден. WireGuard ещё не установлен или очищен."
  exit 1
fi

if [[ ! -f "${WG_DIR}/${WG_IF}.conf" ]]; then
  red "Файл ${WG_DIR}/${WG_IF}.conf не найден. Сначала настрой сервер (wg0)."
  exit 1
fi

# Получаем публичный ключ сервера
if ! cmd_exists wg; then
  red "Команда 'wg' не найдена. Установи wireguard-tools."
  exit 1
fi

SERVER_PUB="$(wg show ${WG_IF} public-key 2>/dev/null || true)"
if [[ -z "${SERVER_PUB}" ]]; then
  red "Не удалось получить публичный ключ сервера (wg show ${WG_IF} public-key)."
  exit 1
fi

# Пытаемся вытащить Endpoint из уже существующего клиента viktor.conf
ENDPOINT=""
if [[ -f "${WG_DIR}/viktor.conf" ]]; then
  ENDPOINT="$(grep -m1 '^Endpoint' "${WG_DIR}/viktor.conf" | awk '{print $3}' || true)"
fi

if [[ -z "${ENDPOINT}" ]]; then
  yellow "Не удалось автоматически определить Endpoint (IP:порт)."
  read -rp "Введи Endpoint вручную (например 185.182.184.40:51820): " ENDPOINT
fi

if [[ -z "${ENDPOINT}" ]]; then
  red "Endpoint не задан, выхожу."
  exit 1
fi

# Проверка, не занят ли этот IP уже в wg0.conf
if grep -q "${CLIENT_IP}/32" "${WG_DIR}/${WG_IF}.conf"; then
  red "Похоже, IP ${CLIENT_IP}/32 уже есть в ${WG_DIR}/${WG_IF}.conf"
  exit 1
fi

green "Создаю клиента '${CLIENT_NAME}' с IP ${CLIENT_IP}/24 и Endpoint ${ENDPOINT}"

umask 077
CLIENT_PRIV_FILE="${WG_DIR}/${CLIENT_NAME}_private.key"
CLIENT_PUB_FILE="${WG_DIR}/${CLIENT_NAME}_public.key"

wg genkey | tee "${CLIENT_PRIV_FILE}" | wg pubkey > "${CLIENT_PUB_FILE}"

CLIENT_PRIV="$(cat "${CLIENT_PRIV_FILE}")"
CLIENT_PUB="$(cat "${CLIENT_PUB_FILE}")"

green "Добавляю клиента в ${WG_DIR}/${WG_IF}.conf ..."

cat >> "${WG_DIR}/${WG_IF}.conf" <<EOF

[Peer]
# ${CLIENT_NAME}
PublicKey = ${CLIENT_PUB}
AllowedIPs = ${CLIENT_IP}/32
EOF

chmod 600 "${WG_DIR}/${WG_IF}.conf"

CLIENT_CONF="${WG_DIR}/${CLIENT_NAME}.conf"
green "Создаю конфиг клиента ${CLIENT_CONF} ..."

cat > "${CLIENT_CONF}" <<EOF
[Interface]
PrivateKey = ${CLIENT_PRIV}
Address = ${CLIENT_IP}/24
DNS = ${DNS_DEFAULT}

[Peer]
PublicKey = ${SERVER_PUB}
Endpoint = ${ENDPOINT}
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
EOF

chmod 600 "${CLIENT_CONF}"

green "Перезапускаю wg-quick@${WG_IF} ..."
systemctl restart "wg-quick@${WG_IF}"

sleep 1
wg show "${WG_IF}" || true

echo
green "Готово! Новый клиент добавлен: ${CLIENT_NAME}"
echo "Файл конфига: ${CLIENT_CONF}"
echo

if cmd_exists qrencode; then
  yellow "QR-код для мобильного клиента WireGuard (${CLIENT_NAME}):"
  qrencode -t ansiutf8 < "${CLIENT_CONF}"
else
  yellow "qrencode не установлен. Можно установить: apt install -y qrencode"
fi

echo
green "Импортируй ${CLIENT_CONF} на ПК/ноутбук или отсканируй QR в приложении WireGuard."
```

Сохрани файл и сделай его исполняемым:

```bash
sudo chmod +x /usr/local/bin/wg-add-client.sh
```

---

## 🚀 Как пользоваться скриптом

Каждый новый клиент = уникальное имя + свободный IP в твоей VPN-сети `10.8.0.0/24`.

Например:

### 1️⃣ Клиент для жены (телефон)

```bash
sudo wg-add-client.sh wife 10.8.0.3
```

### 2️⃣ Клиент для ноутбука

```bash
sudo wg-add-client.sh laptop 10.8.0.4
```

Скрипт:

1. Проверит, что ты root.
    
2. Сгенерирует ключи `wife_private.key` / `wife_public.key`.
    
3. Допишет в `wg0.conf` блок:
    
    ```ini
    [Peer]
    # wife
    PublicKey = ...
    AllowedIPs = 10.8.0.3/32
    ```
    
4. Создаст `/etc/wireguard/wife.conf`.
    
5. Перезапустит `wg-quick@wg0`.
    
6. Покажет QR-код для подключения с телефона.
    

---

## 💡 Где искать новые конфиги

Все файлы клиентов будут лежать здесь:

```bash
ls -l /etc/wireguard/
# viktor.conf, wife.conf, laptop.conf и т.д.
```

Эти `.conf` можно:

- скопировать на компьютер (SCP, WinSCP),
    
- отправить себе (только аккуратно, они содержат private key),
    
- или просто сканировать QR прямо из терминала.
    

---

Если хочешь, дальше можем сделать **мини-шпаргалку по WireGuard**:  
как посмотреть кто подключен, как временно заблокировать клиента, как сменить ему IP и т.п.