# -*- coding: utf-8 -*-


from .arg_parsing import backwards_compatible_parser
from .client import Client
from .environment import Environment

def main():
    args = backwards_compatible_parser()

    client = Client()
    env = Environment()
    resp = client.send(env, **args)

    print(resp)

if __name__ == '__main__':

    main()
