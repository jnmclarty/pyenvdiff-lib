# -*- coding: utf-8 -*-


from .import_macros import import_sys
from .client import P2PClient
from .environment import Environment

def main():

    sys = import_sys()

    if len(sys.argv) >= 1:
        client = P2PClient(server=sys.argv[1])
    else:
        client = P2PClient() # Will default to localhost on 8080


    env = Environment()
    resp = client.send(env)

    print(resp)

if __name__ == '__main__':

    main()
