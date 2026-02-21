#!/data/data/com.termux/files/usr/bin/bash
# Tor system — ATTA PATHAN
# Save as ~/All-country.sh and run: bash ~/All-country.sh

set -o errexit
set -o nounset
set -o pipefail

clear
echo -e "\e[1;31m  █████╗ ████████╗████████╗ █████╗ \e[0m"
echo -e "\e[1;31m ██╔══██╗╚══██╔══╝╚══██╔══╝██╔══██╗\e[0m"
echo -e "\e[1;31m ███████║   ██║      ██║   ███████║\e[0m"
echo -e "\e[1;31m ██╔══██║   ██║      ██║   ██╔══██║\e[0m"
echo -e "\e[1;31m ██║  ██║   ██║      ██║   ██║  ██║\e[0m"
echo -e "\e[1;31m ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝\e[0m"
echo -e "\e[1;37m ██████╗  █████╗ ████████╗██╗  ██╗ █████╗ ███╗   ██╗\e[0m"
echo -e "\e[1;37m ██╔══██╗██╔══██╗╚══██╔══╝██║  ██║██╔══██╗████╗  ██║\e[0m"
echo -e "\e[1;37m ██████╔╝███████║   ██║   ███████║███████║██╔██╗ ██║\e[0m"
echo -e "\e[1;37m ██╔═══╝ ██╔══██║   ██║   ██╔══██║██╔══██║██║╚██╗██║\e[0m"
echo -e "\e[1;37m ██║     ██║  ██║   ██║   ██║  ██║██║  ██║██║ ╚████║\e[0m"
echo -e "\e[1;37m ╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝\e[0m"

echo -e "\e[1;35m┌────────────────────────────────────────────┐\e[0m"
echo -e "\e[1;35m│           MADE BY: ATTA PATHAN             │\e[0m"
echo -e "\e[1;35m└────────────────────────────────────────────┘\e[0m"
echo ""

# ---------------------------
# Ensure required packages
# ---------------------------
echo -e "\e[33m[!] Checking dependencies...\e[0m"
pkg update -y >/dev/null 2>&1 || true
pkg install -y tor privoxy netcat-openbsd curl dos2unix >/dev/null 2>&1 || true
echo -e "\e[32m[OK] Dependencies ready\e[0m"

# ---------------------------
# Countries array: Name Flag ISO
# ---------------------------
COUNTRIES=(
"Afghanistan 🇦🇫 AF" "Albania 🇦🇱 AL" "Algeria 🇩🇿 DZ" "Andorra 🇦🇩 AD"
"Angola 🇦🇴 AO" "Argentina 🇦🇷 AR" "Australia 🇦🇺 AU" "Austria 🇦🇹 AT"
"Belgium 🇧🇪 BE" "Brazil 🇧🇷 BR" "Canada 🇨🇦 CA" "Chile 🇨🇱 CL"
"China 🇨🇳 CN" "Colombia 🇨🇴 CO" "Czechia 🇨🇿 CZ" "Denmark 🇩🇰 DK"
"Egypt 🇪🇬 EG" "Finland 🇫🇮 FI" "France 🇫🇷 FR" "Germany 🇩🇪 DE"
"India 🇮🇳 IN" "Indonesia 🇮🇩 ID" "Ireland 🇮🇪 IE" "Israel 🇮🇱 IL"
"Italy 🇮🇹 IT" "Japan 🇯🇵 JP" "Mexico 🇲🇽 MX" "Netherlands 🇳🇱 NL"
"New Zealand 🇳🇿 NZ" "Norway 🇳🇴 NO" "Pakistan 🇵🇰 PK" "Poland 🇵🇱 PL"
"Portugal 🇵🇹 PT" "Russia 🇷🇺 RU" "Saudi Arabia 🇸🇦 SA" "South Africa 🇿🇦 ZA"
"South Korea 🇰🇷 KR" "Spain 🇪🇸 ES" "Sweden 🇸🇪 SE" "Switzerland 🇨🇭 CH"
"Turkey 🇹🇷 TR" "United Arab Emirates 🇦🇪 AE" "United Kingdom 🇬🇧 GB" "United States 🇺🇸 US"
)

# ---------------------------
# Menu display
# ---------------------------
echo -e "\e[1;36mChoose a country by number (ATTA PATHAN Tool):\e[0m"
for i in "${!COUNTRIES[@]}"; do
    idx=$((i+1))
    echo -e "$(printf "%3d" "$idx") ) ${COUNTRIES[$i]}"
done
all_index=$(( ${#COUNTRIES[@]} + 1 ))
echo -e "$(printf "%3d" "$all_index") ) All countries 🌐"

read -rp $'\nEnter choice number: ' CHOICE
CHOICE="${CHOICE//$'\r'/}"

# ---------------------------
# Process selection
# ---------------------------
if [[ "$CHOICE" =~ ^[Aa]$ || "$CHOICE" == "$all_index" ]]; then
    EXIT_COUNTRY=""
    echo -e "\e[33mSelected: Global IP (ATTA PATHAN)\e[0m"
else
    if ! [[ "$CHOICE" =~ ^[0-9]+$ ]] || (( CHOICE < 1 || CHOICE > ${#COUNTRIES[@]} )); then
        echo -e "\e[31mInvalid. Exiting.\e[0m"
        exit 1
    fi
    selected="${COUNTRIES[$((CHOICE-1))]}"
    EXIT_COUNTRY="$(echo "$selected" | awk '{print $NF}')"
    echo -e "\e[32mSelected: $selected\e[0m"
fi

# ---------------------------
# Rotation interval
# ---------------------------
read -rp "Enter rotation time (sec, default 15): " ROTATION_TIME
ROTATION_TIME="${ROTATION_TIME:-15}"

# ---------------------------
# Runtime directories
# ---------------------------
RUNTIME_DIR="${HOME}/.atta_pathan_tor"
TOR_MULTI_DIR="${RUNTIME_DIR}/tor_multi"
PRIVOXY_DIR="${RUNTIME_DIR}/privoxy"
LOGFILE="${RUNTIME_DIR}/ips.log"
mkdir -p "$TOR_MULTI_DIR" "$PRIVOXY_DIR"
> "$LOGFILE"

pkill tor 2>/dev/null || true
pkill privoxy 2>/dev/null || true
sleep 1

# ---------------------------
# Start Tor nodes
# ---------------------------
NODES=3
START_SOCKS_PORT=9050
START_CTRL_PORT=9051
PORTS=()
CTRL_PORTS=()

for i in $(seq 0 $((NODES-1))); do
    socks_port=$((START_SOCKS_PORT + i*10))
    ctrl_port=$((START_CTRL_PORT + i*10))
    PORTS+=("$socks_port")
    CTRL_PORTS+=("$ctrl_port")
    NODE_DIR="${TOR_MULTI_DIR}/tor${i}"
    mkdir -p "$NODE_DIR"

    cat > "${NODE_DIR}/torrc" <<EOF
SocksPort ${socks_port}
ControlPort ${ctrl_port}
DataDirectory ${NODE_DIR}/data
CookieAuthentication 0
EOF

    if [[ -n "$EXIT_COUNTRY" ]]; then
        echo "ExitNodes {${EXIT_COUNTRY}}" >> "${NODE_DIR}/torrc"
        echo "StrictNodes 1" >> "${NODE_DIR}/torrc"
    fi

    tor -f "${NODE_DIR}/torrc" > /dev/null 2>&1 &
    sleep 1
done

# ---------------------------
# Privoxy setup
# ---------------------------
PRIVOXY_CONF="${PRIVOXY_DIR}/config"
cat > "$PRIVOXY_CONF" <<EOF
listen-address 127.0.0.1:8118
EOF
for p in "${PORTS[@]}"; do
    echo "forward-socks5 / 127.0.0.1:${p} ." >> "$PRIVOXY_CONF"
done
privoxy "$PRIVOXY_CONF" > /dev/null 2>&1 &
sleep 1

# ---------------------------
# Rotation & IP logging
# ---------------------------
get_ip() { curl --silent --max-time 10 --proxy http://127.0.0.1:8118 https://api64.ipify.org || echo "FAILED"; }

PREV_IP="$(get_ip)"
echo -e "\e[32mInitial IP: $PREV_IP\e[0m"

echo -e "\e[36mRotating IP every ${ROTATION_TIME}s. ATTA PATHAN power!\e[0m"
while true; do
    for ctrl in "${CTRL_PORTS[@]}"; do
        printf 'AUTHENTICATE ""\r\nSIGNAL NEWNYM\r\nQUIT\r\n' | nc 127.0.0.1 "$ctrl" >/dev/null 2>&1 || true
    done
    sleep 3
    NEW_IP="$(get_ip)"
    if [[ "$NEW_IP" != "$PREV_IP" && "$NEW_IP" != "FAILED" ]]; then
        echo -e "\e[1;32m[+] New IP: $NEW_IP ✅\e[0m"
        PREV_IP="$NEW_IP"
    fi
    sleep "$ROTATION_TIME"
done
