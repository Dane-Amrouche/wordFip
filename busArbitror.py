#!/usr/bin/env python3
from time import sleep
from math import gcd
from functools import reduce
from itertools import cycle
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, SO_REUSEPORT
from frame import ID_Dat,RP_Dat

#DEFINE RETURN TIME
_RETURN_TIME = 20
class BusArbitror(object):
    '''
    Représente un arbitre de bus du protocol World-FIP
    '''
    def __init__(self, table={}):
        self._table = table
        self._microcycle, self._macrocycle = self.cycles_from_table(table)

    def server_init(self, port=5432):
        self._socket = socket(AF_INET, SOCK_DGRAM)
        self._socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self._socket.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
        self._socket.settimeout(0)
        self._socket.bind(('', port))
        self._port = port

    def send_data(self, data: bytes):
        self._socket.sendto(data, ('<broadcast>', self._port))

    def loop_init(self):
        '''
        Loop over all messages and schedule IDs according to the table
        '''
        i=0
        
        for tmp, data in cycle(self.list_macrocycle()):
            i=0
            for tmp2,data in self.list_microcycle():
                if tmp2 != tmp:
                    tmp2 = tmp
                    sleep(self._microcycle  / 1000)
                    print(f"tmp = {tmp} ms")
                # Sent the message over the bus
                print(f'\tSending [{data}]')
                i+=1
                self.send_data(data.get_repr())
                print("size ID_Dat= {} size RP_Dat {} ".format(ID_Dat.size(),RP_Dat.size()))
                TTi= ((ID_Dat.size()+RP_Dat.size())*8 + 2* _RETURN_TIME)  / 1000
                sleep(TTi)
                sleep((self._microcycle-(i*TTi))/1000)

            print("nbr s'objets envoyes dans un macro cycle= ",i)
            print("temps d'attente entre microcycle = ",self._microcycle-(i*TTi))   
                #sleep((self._microcycle-(i*TTi))/1000)


    def list_macrocycle(self):
        '''
        Do a full macrocycle

        return a tuple `(time, Frame)`
        '''
        for tmp in range(0, self._macrocycle,self._microcycle):
            # Loop over the table to see what message should be send
            for id, period in self._table.items():
                if tmp % period == 0:
                    yield (tmp, ID_Dat(id))

    def list_microcycle(self):
        '''
        Do a full microcycle

        return a tuple `(time, Frame)`
        '''
        for tmp1 in range(0,self._macrocycle,self._microcycle):
            # Loop over the table to see what message should be send
            for id, period in self._table.items():
                if tmp1 % period == 0:
                    yield (tmp1, ID_Dat(id))                    

    @staticmethod
    def cycles_from_table(table):
        '''Return the microcycle and macrocycle from a period table'''
        def ppcm(values):
            '''Helper to compute the Least Commom Multiple'''
            return reduce(lambda x, y: x * y // gcd(x, y), values)
        return (min(table.values()), ppcm(table.values()))


if __name__ == '__main__':
    table = {
        101: 100 * 10,
        102: 200 * 10,
        103: 500 * 10,
        104: 100 * 10,
        105: 200 * 10,
    }

    bus = BusArbitror(table)
    bus.server_init()
    bus.loop_init()

