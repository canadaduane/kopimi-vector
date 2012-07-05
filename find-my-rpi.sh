echo "Looking for open SSH ports on subnet 192.168.1.0"
nmap -p 22 --open -sV 192.168.1.0/24
