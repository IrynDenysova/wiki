```bash
    1  apt update && apt -y upgrade && apt -y autoremove
    2  apt install -y sudo vim ufw fail2ban htop net-tools curl wget git lsb-release ca-certificates
    3  adduser viktor
    4  usermod -aG sudo viktor
    5  mkdir -p /home/viktor/.ssh
    6  nano /home/viktor/.ssh/authorized_keys
    7  chmod 700 /home/viktor/.ssh
    8  chmod 600 /home/viktor/.ssh/authorized_keys
    9  chown -R viktor:viktor /home/viktor/.ssh
   10  systemctl restart ssh
   11  exit
   12  cd /etc/wireguard
   13  ls -lah
   14  umask 077
   15  wg genkey | tee server_private.key | wg pubkey | tee server_public.key
   16  sudo cat /etc/wireguard/server_public.key
   17  sudo nano /etc/wireguard/wg0.conf
   18  sudo cat /etc/wireguard/server_private.key
   19  ip a
   20  sudo nano /etc/wireguard/wg0.conf
   21  echo "net.ipv4.ip_forward=1" | sudo tee /etc/sysctl.d/99-wireguard.conf
   22  sudo sysctl --system
   23  sudo systemctl enable wg-quick@wg0
   24  sudo systemctl start wg-quick@wg0
   25  sudo systemctl status wg-quick@wg0
   26  cd /etc/wireguard
   27  sudo wg genkey | sudo tee client1_private.key | sudo wg pubkey | sudo tee client1_public.key
   28  sudo cat client1_private.key
   29  sudo cat client1_public.key
   30  sudo nano /etc/wireguard/wg0.conf
   31  sudo systemctl restart wg-quick@wg0
   32  sudo nano /etc/wireguard/wg0.conf
   33  history   подготовь шпаргалку подробно
```

---
## 0. Исходные данные

- ОС: **Debian 12**
    
- Внешний IP: **45.140.146.143**
    
- Внешний интерфейс: **ens3** (смотрели по `ip a`)
    
- VPN-сеть: **10.8.0.0/24**
    
- Сервер (WG): **10.8.0.1**
    
- Первый клиент: **10.8.0.2**
    
- Порт WG: **51820/udp**
    

---

## 1. Первичная настройка сервера

```bash
apt update && apt -y upgrade && apt -y autoremove
apt install -y sudo vim ufw fail2ban htop net-tools curl wget git lsb-release ca-certificates
```

- `sudo` — чтобы не всё делать из-под root
    
- `ufw` / `fail2ban` — безопасность
    
- `htop` / `net-tools` — удобство
    

---

## 2. Создать пользователя и подготовить SSH

```bash
adduser viktor
usermod -aG sudo viktor
mkdir -p /home/viktor/.ssh
nano /home/viktor/.ssh/authorized_keys   # сюда вставляешь свой публичный ключ
chmod 700 /home/viktor/.ssh
chmod 600 /home/viktor/.ssh/authorized_keys
chown -R viktor:viktor /home/viktor/.ssh
systemctl restart ssh
```

Теперь можно заходить как обычный юзер:

```bash
ssh viktor@s2.viktorplus.com
```

---

## 3. Установка и подготовка WireGuard

(ты уже сделал, но в шпаргалке должно быть)

```bash
apt install -y wireguard
cd /etc/wireguard
umask 077
wg genkey | tee server_private.key | wg pubkey | tee server_public.key
```

- `server_private.key` — в конфиг сервера
    
- `server_public.key` — отдаём клиентам
    

Смотрим ключи:

```bash
cat /etc/wireguard/server_private.key
cat /etc/wireguard/server_public.key
```

---

## 4. Конфиг сервера `/etc/wireguard/wg0.conf`

```ini
[Interface]
Address = 10.8.0.1/24
ListenPort = 51820
PrivateKey = ВСТАВЬ_СЮДА_СВОЙ_server_private.key

# NAT + маршрутизация через ens3 (у тебя именно ens3!)
PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -A FORWARD -o %i -j ACCEPT; iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -D FORWARD -o %i -j ACCEPT; iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
```

Если нужен UFW — откроем позже 51820/udp.

# Этап 6. Разрешаем порт в фаерволе (UFW)

`sudo ufw allow 51820/udp sudo ufw reload`


---

## 5. Включить форвардинг в системе

```bash
echo "net.ipv4.ip_forward=1" | tee /etc/sysctl.d/99-wireguard.conf
sysctl --system
```

---

## 6. Запуск и автозапуск WireGuard

```bash
systemctl enable wg-quick@wg0
systemctl start wg-quick@wg0
systemctl status wg-quick@wg0
```

Проверить:

```bash
wg
```

Должен показать интерфейс `wg0`.

---

## 7. Создание клиента на сервере

(чтобы всё хранить в одном месте)

```bash
cd /etc/wireguard
wg genkey | tee client1_private.key | wg pubkey | tee client1_public.key
cat client1_private.key
cat client1_public.key
```

Теперь добавляем этого клиента в **серверный** конфиг:

```bash
nano /etc/wireguard/wg0.conf
```

в конец:

```ini
[Peer]
# Viktor Windows
PublicKey = СЮДА_ИЗ_client1_public.key
AllowedIPs = 10.8.0.2/32
```

Перезапускаем:

```bash
systemctl restart wg-quick@wg0
```

---

## 8. Конфиг клиента (Windows) `client1.conf`

Этот файл ты у себя и сделал:
ls -l /etc/wireguard/

```ini
[Interface]
PrivateKey = СЮДА_ИЗ_client1_private.key
Address = 10.8.0.2/32
DNS = 1.1.1.1

[Peer]
PublicKey = СЮДА_СЕРВЕРНЫЙ_server_public.key
Endpoint = s2.viktorplus.com:51820
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
```

- если не нужен весь интернет через VPN → в `AllowedIPs` можно поставить `10.8.0.0/24`.
    

---

## 9. Подключение с Windows

1. Установить WireGuard для Windows.
    
2. **Add Tunnel → Import from file** → выбрать `client1.conf`.
    
3. Нажать **Activate**.
    
4. Готово.
# Этап 8. Подключение клиента

Скопируй файл `client1.conf` на устройство:

- на **Windows/Mac/Linux**: импортируй через приложение _WireGuard_;
    
- на **Android/iPhone**: отсканируй QR-код.
    
```
sudo ufw allow 51820/udp
# открыть порт
```

```
#QR-код можно вывести:
sudo apt install -y qrencode sudo qrencode -t ansiutf8 < /etc/wireguard/client1.conf
```

```

---

## 10. Проверка работы

**На сервере:**

```bash
wg
```

видим:

- endpoint клиента
    
- latest handshake (должен быть несколько секунд назад)
    
- bytes sent/received
    

**С Windows:**

```cmd
ping 10.8.0.1
```

если отвечает — туннель жив.

Проверка IP в браузере — чтобы понять, идёт ли интернет через VPN.

---

## 11. UFW (опционально)

Если будешь включать UFW — не забудь впустить WireGuard:

```bash
ufw allow 22/tcp
ufw allow 51820/udp
ufw enable
ufw status
```

---

## 12. Полезные команды

```bash
# посмотреть состояние WG
wg

# подробный вывод интерфейса
wg show wg0

# перезапустить VPN
systemctl restart wg-quick@wg0

# посмотреть логи
journalctl -u wg-quick@wg0 -f

# показать IP-интерфейсы
ip a

# показать таблицу маршрутов
ip route

# показать слушающие порты
ss -uln | grep 51820
```

---

Это уже рабочая памятка именно под твою машину (Debian 12 + ens3 + WireGuard + клиент из Windows). Если хочешь — могу ниже добавить блок “как добавить второго клиента” и “как сделать чтобы только приватные сети шли через VPN”.