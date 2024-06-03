import argparse
import asyncio
from aioquic.quic.configuration import QuicConfiguration
import echo_client
import quic_engine
import os
import echo_server
from subprocess import run

def client_mode(args):
    server_address = args.server
    server_port = args.port
    try: # tests if client cert exists
        cert_file = args.cert_file
        config = quic_engine.build_client_quic_config(cert_file)
    except:
        config = quic_engine.build_client_quic_config(cert_file)
    
    
    asyncio.run(quic_engine.run_client(server_address, server_port, config))
    
    
def server_mode(args):
    listen_address = args.listen
    listen_port = args.port
    cert_file = args.cert_file
    key_file = args.key_file
    
    server_config = quic_engine.build_server_quic_config(cert_file, key_file)
    asyncio.run(quic_engine.run_server(listen_address, listen_port, server_config))

def parse_args():
    parser = argparse.ArgumentParser(description='Echo example')
    subparsers = parser.add_subparsers(dest='mode', help='Mode to run the application in', required=True)
    client_parser = subparsers.add_parser('client')
    client_parser.add_argument('-s','--server', default='localhost', help='Host to connect to')   
    client_parser.add_argument('-p','--port', type=int, default=3074, help='Port to connect to')
    if os.path.isfile('certs/quic_certificate.pem'):
        client_parser.add_argument('-c','--cert-file', default='./certs/quic_certificate.pem', help='Certificate file (for self signed certs)')

    server_parser = subparsers.add_parser('server')
    if os.path.isfile('certs/quic_certificate.pem') and os.path.isfile('certs/quic_private_key.pem'): 
        server_parser.add_argument('-c','--cert-file', default='./certs/quic_certificate.pem', help='Certificate file (for self signed certs)')
        server_parser.add_argument('-k','--key-file', default='./certs/quic_private_key.pem', help='Key file (for self signed certs)')
    else:
        run("./certs/gencert.sh",shell=True)
        server_parser.add_argument('-c','--cert-file', default='./certs/quic_certificate.pem', help='Certificate file (for self signed certs)')
        server_parser.add_argument('-k','--key-file', default='./certs/quic_private_key.pem', help='Key file (for self signed certs)')
    server_parser.add_argument('-l','--listen', default='localhost', help='Address to listen on')
    server_parser.add_argument('-p','--port', type=int, default=3074, help='Port to listen on')
       
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    if args.mode == 'client':
        client_mode(args)
    elif args.mode == 'server':
        server_mode(args)
    else:
        print('Invalid mode')

