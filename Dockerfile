FROM kalilinux/kali-rolling:latest

WORKDIR /usr/src/app

COPY . .

RUN chmod o+r /etc/resolv.conf

RUN apt-get update \
	&& apt-get install -y procps iptables net-tools gcc python3 python3-pip \
	python3-setuptools hostapd dnsmasq openssl libnl-3-dev libnl-genl-3-dev libssl-dev

RUN pip3 install --no-cache-dir -r requirements.txt

# RUN git clone https://github.com/wifiphisher/wifiphisher.git

RUN cd wifiphisher && python3 setup.py install --record files.txt \
	&& cd .. && apt-get clean

CMD ["wifiphisher"]
