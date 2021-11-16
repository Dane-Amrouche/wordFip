#!/usr/bin/env python3
from time import sleep
from argparse import ArgumentParser
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, SO_REUSEPORT
from frame import ID_Dat,RP_Dat
#import RPi.GPIO as GPIO #Importe la bibliothèque pour contrôler les GPIOs



#GPIO.setmode(GPIO.BOARD) #Définit le mode de numérotation (Board)
#GPIO.setwarnings(False) #On désactive les messages d'alerte

#ED_LED = 7 #Définit le numéro du port GPIO qui alimente la led
#GREEN_LED = 11
#GPIO.setup(RED_LED, GPIO.OUT) #Active le contrôle du GPIO
#GPIO.setup(GREEN_LED, GPIO.OUT) #Active le contrôle du GPIO



def msleep(sec):
    sleep(sec / 1000)


RETURN_TIME = 100


class Producer(object):
    def __init__(self, id: int, data: bytes):
        self._id = id
        self._data = data

    def run_server(self, port=5432):
        self._sock = socket(AF_INET, SOCK_DGRAM)
        self._sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self._sock.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
        self._sock.bind(('', port))
        self._port = port

    def send_rp_dat(self, msg: RP_Dat):
        self._sock.sendto(msg.get_repr(), ('<broadcast>', self._port))

    def recv_id_dat(self):
        data, addr = self._sock.recvfrom(ID_Dat.size())
        try:
            return ID_Dat.from_repr(data)
        except:
            return "Data non reçue"

    def do_loop(self):
        while True:
            # 1. Get the ID_Dat
            id_dat = self.recv_id_dat()

            # 2. Ignore messages for which we are not the producer
            #if not id_dat or id_dat.id != self._id:
            #    continue
            #state = GPIO.input(RED_LED) #Lit l'état actuel du GPIO, vrai si allumé, faux si éteint
            #if state : #Si GPIO allumé
             #   GPIO.output(RED_LED, GPIO.LOW) #On l’étein
              #  GPIO.output(GREEN_LED,GPIO.HIGH)
            #else:
             #   GPIO.output(GREEN_LED,GPIO.LOW)
              #  GPIO.output(RED_LED,GPIO.HIGH)
            # 3. Send back the object to the bus
            msleep(RETURN_TIME)
            rp_dat = RP_Dat(self._data)
            print(f'sending {rp_dat}')
            self.send_rp_dat(rp_dat)
            #GPIO.output(RED_LED, GPIO.HIGH) #On l'allume
            #sleep(1)
            #GPIO.output(GREEN_LED,GPIO.LOW)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('id', type=int)
    parser.add_argument('msg', default='tititata', nargs='?')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    prod = Producer(args.id, bytes(args.msg, 'utf-8'))
    prod.run_server()
    prod.do_loop()
