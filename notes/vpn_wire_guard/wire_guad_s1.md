root@s1:/etc/wireguard# cat server_public.key
t28/GOZ7ISCoICDVdygcqtL2uEtdGjRWBPg1k3Rp7Fc=

root@s1:/etc/wireguard# cat server_private.key
+N1iuIBC0eU+NxwJQxkckacIsG7QsmeZpynbNFygxUg=

sudo nano /etc/wireguard/wg0.conf

[Interface]
Address = 10.8.0.1/24
SaveConfig = true
ListenPort = 51820
PrivateKey = +N1iuIBC0eU+NxwJQxkckacIsG7QsmeZpynbNFygxUg=
PostUp   = iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE



root@s1:/etc/wireguard# cat client1_public.key
AHSBiHTltWzc2nMZl9bsFtHdCohs2NyPYKZQ9gHTph4=

root@s1:/etc/wireguard# cat client1_private.key
IC6NuM8ktfyOtGZlXr8kn9emSJ78VqROsqT5YCJz7Eg=

![[Pasted image 20251201225721.png]]

![[Pasted image 20251201230058.png]]
sudo ufw allow 51820/udp 
|открыть порт|