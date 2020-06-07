import argparse
from ReverseProxy import ReverseProxy

parser = argparse.ArgumentParser()

parser.add_argument('-pa', action='store', dest='proxy_address',
                    help='proxy address')

parser.add_argument('-pp', action='store', dest='proxy_port', type=int,
                    help='proxy port')

parser.add_argument('-pda', action='store', dest='proxy_destination_address',
                    help='proxy destination address')

parser.add_argument('-pdp', action='store', dest='proxy_destination_port', type=int,
                    help='proxy destination port')


results = parser.parse_args()

if results.proxy_address and results.proxy_port and results.proxy_destination_address and results.proxy_destination_port:

    proxy = ReverseProxy(results.proxy_address, results.proxy_port, results.proxy_destination_address,
                     results.proxy_destination_port)

    proxy.start_proxy()