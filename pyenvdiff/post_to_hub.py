# -*- coding: utf-8 -*-


from .import_macros import import_sys
from .client import HubClient
from .environment import Environment

def main():

    sys = import_sys()

    if len(sys.argv) >= 2:
        client = HubClient(server=sys.argv[-1])
    else:
        print("Assuming http://localhost:8080, add the base URL as a single argument for a different hub.")
        client = HubClient() # Will default to localhost on 8080


    env = Environment()
    resp = client.send(env)

    print(resp)

if __name__ == '__main__':

    main()
