from socket import inet_pton
from socket import inet_ntop
from socket import AF_INET
from pyroute2.dhcp import dhcpmsg
from pyroute2.dhcp import option


class dhcp4msg(dhcpmsg):
    #
    # https://www.ietf.org/rfc/rfc2131.txt
    #
    fields = (('op', 'uint8'),
              ('htype', 'uint8'),
              ('hlen', 'uint8'),
              ('hops', 'uint8'),
              ('xid', 'uint32'),
              ('secs', 'uint16'),
              ('flags', 'uint16'),
              ('ciaddr', 'ip4addr'),
              ('yiaddr', 'ip4addr'),
              ('siaddr', 'ip4addr'),
              ('giaddr', 'ip4addr'),
              ('chaddr', 'l2paddr'),
              ('sname', '64s'),
              ('file', '128s'),
              ('cookie', '4s', b'c\x82Sc'))
    #
    # https://www.ietf.org/rfc/rfc2132.txt
    #
    options = ((0, 'pad', 'none'),
               (1, 'subnet_mask', 'ip4addr'),
               (2, 'time_offset', 'be32'),
               (3, 'router', 'ip4list'),
               (4, 'time_server', 'ip4list'),
               (5, 'ien_name_server', 'ip4list'),
               (6, 'name_server', 'ip4list'),
               (7, 'log_server', 'ip4list'),
               (8, 'cookie_server', 'ip4list'),
               (9, 'lpr_server', 'ip4list'),
               (53, 'message_type', 'uint8'),
               (55, 'parameter_list', 'array8'),
               (57, 'messagi_size', 'be16'),
               (60, 'vendor_id', 'string'),
               (61, 'client_id', 'client_id'),
               (255, 'end', 'none'))

    class ip4addr(option):
        policy = {'fmt': '4s',
                  'encode': lambda x: inet_pton(AF_INET, x),
                  'decode': lambda x: inet_ntop(AF_INET, x)}

    class ip4list(option):
        policy = {'fmt': 'string',
                  'encode': lambda x: ''.join([inet_pton(AF_INET, i) for i
                                               in x]),
                  'decode': lambda x: [inet_ntop(AF_INET, x[i*4:i*4+4]) for i
                                       in range(len(x)//4)]}