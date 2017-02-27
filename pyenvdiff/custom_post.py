# -*- coding: utf-8 -*-


from pyenvdiff.arg_parsing import backwards_compatible_parser
from pyenvdiff.client import Client
from pyenvdiff.environment import Environment
from pyenvdiff.collectors import Collector

class MyCollector(Collector):
    @staticmethod
    def from_env():
        from this import s, d
        info = [d.get(c, c) for c in s]
        return info
    def __str__(self):
        return "".join(self.info)

def main():
    args = backwards_compatible_parser()

    client = Client(server='https://osa.pyenvdiff.com', api_key=None)
    env = Environment() + MyCollector()
    resp = client.send(env, **args)
    print(resp)

if __name__ == '__main__':

    main()
