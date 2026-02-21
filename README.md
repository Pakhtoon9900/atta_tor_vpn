pkg update && pkg upgrade -y
pkg install git python -y
git clone https://github.com/Pakhtoon9900/atta_tor_vpn
cd atta_tor_vpn
chmod +x *
mv vpn.py $PREFIX/bin/atta-tor
