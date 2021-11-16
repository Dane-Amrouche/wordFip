#!/usr/bin/env python3
from time import sleep
from math import gcd
from functools import reduce
from itertools import cycle
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, SO_REUSEPORT
from frame import ID_Dat,RP_Dat


def msleep(sec):
    sleep(sec / 1000)


RETURN_TIME = 50


class BusArbitror(object):
    '''
    Représente un arbitre de bus du protocol World-FIP
    '''
    def __init__(self, table={}):
        self._table = table
        self._microcycle, self._macrocycle = self.cycles_from_table(table)

    def run_server(self, port=5432):
        self._sock = socket(AF_INET, SOCK_DGRAM)
        self._sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self._sock.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
        self._sock.settimeout(0)
        self._sock.bind(('', port))
        self._port = port

    def send_msg(self, msg: bytes):
        self._sock.sendto(msg, ('<broadcast>', self._port))

    def do_loop(self):
        '''
        Boucle sur tous les messages et identifiants de planification selon le tableau

        '''
        t2 = None
        for t, msg in cycle(self.list_macrocycle()):
            if t != t2:
                t2 = t
                msleep(self._microcycle)
                print(f't = {t}ms')

            # Envoyé le message dans le bus
            print(f'\tsending {msg}')
            self.send_msg(msg.get_repr())
            print("taille ID_Dat = ",ID_Dat.size())
            #print("taille RP_Dat = ",RP_Dat.size(''))
            print("taille RP_Dat = ",RP_Dat.Taille)

            msleep((ID_Dat.size()+RP_Dat.Taille)* 8+ 2* RETURN_TIME)

    def list_macrocycle(self):
        '''
       Faire un macrocycle complet
        retouner les tuples `(time, Frame)`
        '''
        for t in range(0, self._macrocycle, self._microcycle):
            # Loop over the table to see what message should be send
            for id, period in self._table.items():
                if t % period == 0:
                    yield (t, ID_Dat(id))

    @staticmethod
    def cycles_from_table(table):
        '''Return the microcycle and macrocycle from a period table'''
        def lcm(numbers):
            '''Helper to compute the Least Commom Multiple'''
            return reduce(lambda a, b: a * b // gcd(a, b), numbers)
        return (min(table.values()), lcm(table.values()))


if __name__ == '__main__':
    bus = BusArbitror({
        101: 100 * 10,
        102: 200 * 10,
        103: 500 * 10,
        104: 100 * 10,
        105: 200 * 10,
    })
    bus.run_server()
    bus.do_loop()
