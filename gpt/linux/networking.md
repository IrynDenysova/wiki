# Сетевые состояния и диагностика — шпаргалка

Коротко: используйте системные утилиты (`ip`, `ss`, `netstat`, `ping`, `traceroute`, `curl` и др.) для контроля сетевых интерфейсов, соединений, маршрутов и задержек.
#networking, #linux, #network, #ip, #ping, #netstat, #traceroute, #curl
---

## Интерфейсы и маршруты

- `ip addr` — показать интерфейсы, IP-адреса, MTU
- `ip link set dev eth0 up/down` — включить/выключить интерфейс
- `ip -br addr` — краткий формат
- `ip route` — таблица маршрутов
- `ip route get 8.8.8.8` — какое устройство/враг используется
- `route -n` — старый стиль таблиц
- `nmcli device status` — состояние NetworkManager (если есть)

## Состояния соединений

- `ss -tulwn` — TCP/UDP слушатели (с учетом локального порта)
- `ss -tunap` — активные TCP/UDP соединения с PID
- `ss -s` — статистика (timewait, estab, etc.)
- `netstat -tunlp` *(если установлена)* — аналог `ss`
- `lsof -i :80` — кто держит порт 80
- `iptables -L -n -v` — фильтры (firewall)
- `nft list ruleset` — если используется nftables

## Проверка доступности и маршрута

- `ping 8.8.8.8` — базовое ICMP (с `-c 4` для количества)
- `ping -I eth0 1.1.1.1` — указать интерфейс
- `traceroute 1.1.1.1` / `tracepath` — трассировка маршрута
- `mtr 1.1.1.1` — интерактивная трассировка (показывает пинг/потери по хопам)
- `curl -I https://example.com` — HTTP-запрос (полезно для контроля TLS/Headers)
- `curl --max-time 5 http://localhost/health` — таймауты
- `wget --spider` — проверка URL без загрузки

## DNS и проверка имен

- `dig example.com` / `dig +short example.com` — DNS-запрос A, AAAA, CNAME и т.д.
- `dig @8.8.8.8 example.com` — конкретный резолвер
- `nslookup example.com` — альтернативный клиент
- `host example.com` — показывает указатели A/AAAA/CNAME

## Мониторинг сетевых интерфейсов

- `ethtool eth0` — статистика драйвера, авто-согласование
- `ethtool -S eth0` — статистика по очередям/ошибкам
- `ifconfig eth0` *(устарело)* — общий вывод, но до сих пор встречается
- `watch -n 1 cat /proc/net/dev` — обновляемая статистика
- `nload`, `bmon`, `iptraf-ng` — консольные графики трафика

## Сетевые состояния и их значения

| Состояние | Обозначает |
|-----------|------------|
| `ESTAB` | соединение установлено (обычно `ss | grep ESTAB`)
| `LISTEN` | процесс слушает порт
| `SYN-SENT`/`SYN-RECV` | в процессе установления TCP
| `TIME-WAIT` | ожидает завершения (обычно быстро исчезает)
| `CLOSE-WAIT` | ожидает закрывающий FIN от приложения
| `FIN-WAIT` | закрывающий сокет не завершён
| `CLOSED` | соединение закрыто
| `UNCONN` | UDP без привязки

## Советы по диагностике

- Начинайте с `ip addr`/`ip route`, затем `ss -tulwn`, чтобы увидеть локальные слушатели
- Используйте `ping`/`traceroute` для проверки reachability, `dig` для DNS, `curl`/`wget` для уровня приложения
- Сравнивайте `ss` с `ps`/`lsof` чтобы увидеть, какой процесс держит порт
- Проверяйте `/etc/resolv.conf` и `systemd-resolved` (если активен) для DNS-проблем
- Используйте `tcpdump -i eth0 port 53` для отладки DNS или `tcpdump -i eth0 host 10.0.0.5` для захвата трафика
- Проверяйте сложные firewall-правила (`iptables`, `nftables`, `firewalld`) при неожиданных блокировках

## Источники и справка

- `man ip`, `man ss`, `man curl`, `man dig`, `man traceroute`
- iproute2 docs: https://wiki.linuxfoundation.org/networking/iproute2
- ss/netstat comparison: https://wiki.archlinux.org/title/Netstat
- tcpdump: https://www.tcpdump.org

---

Вернуться к [главной странице](./README.md).
