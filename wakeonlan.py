import string
import socket
import struct


class WoLClient:

    def __init__(self, machines):
        self._machines = machines

    @property
    def machines(self):
        return self._machines

    @staticmethod
    def sanitize_mac(untrusted_mac):
        if len(untrusted_mac) != 17:
            raise AttributeError(f'Invalid MAC address length')

        untrusted_mac = untrusted_mac.replace(':', '')

        for c in untrusted_mac:
            if c not in string.hexdigits:
                raise AttributeError(f'Invalid character found in MAC address')

        mac = untrusted_mac
        return mac

    def wake_on_lan(self, untrusted_mac):
        mac = self.sanitize_mac(untrusted_mac)
        if mac:
            # Magic Packet
            hex_magic_packet = 'FFFFFFFFFFFF' + 16 * mac

            # convert raw_payload byte-wise
            magic_packet = b''.join([struct.pack('!B', int(
                hex_magic_packet[i] + hex_magic_packet[i + 1], 16)) for i in
                                     range(0, len(hex_magic_packet), 2)])

            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(magic_packet, ('<broadcast>', 7))
            sock.close()
