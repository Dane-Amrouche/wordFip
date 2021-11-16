import struct
from abc import ABC, abstractmethod


class Frame(ABC):
    DEFAULT_INIT_SEQUENCE = 42  # à définir : séquence de début de trame sur 2 octets
    DEFAULT_END_SEQUENCE = b'\042'  # à définir : séquence de fin de trame sur 1 octets

    def __init__(self, type: bytes):
        self._init_sequence = self.DEFAULT_INIT_SEQUENCE
        self._end_sequence = self.DEFAULT_END_SEQUENCE
        assert len(type) == 1, 'The type of a frame must be one byte'
        self._type = type

    def __repr__(self):
        return str(self.__dict__)

    @abstractmethod
    def get_repr(self):
        pass

    @classmethod
    @abstractmethod
    def from_repr(cls, repr: bytes):
        raise NotImplementedError('Frame does not exists, use a concrete frame instead')


class ID_Dat(Frame):
    '''
    Trame envoyée par l'arbitre de bus pour indiqué l'objet à transmettre
    '''
    TYPE = b'I'

    def __init__(self, id: int, *args, **kwargs):
        super().__init__(self.TYPE, *args, **kwargs)
        self._id = id

    @property
    def id(self):
        return self._id

    def get_repr(self):
        fmt = f'hchc'
        vals = (self._init_sequence, self._type, self._id, self._end_sequence)
        return struct.pack(fmt, *vals)

    @classmethod
    def from_repr(cls, repr: bytes):
        fmt = f'hchc'
        _, type, id, _ = struct.unpack(fmt, repr)
        assert type == cls.TYPE, f'Bad frame type, expected {cls.TYPE}, got {type}'
        return cls(id)

    @classmethod
    def size(cls):
        '''The ID_Dat frame is represented with 7 bytes'''
        return 6


class RP_Dat(Frame):
    '''
    Trame envoyée par les producteur en réponse à une trame ID_Dat
    '''
    TYPE = b'D'
    Taille=0 
    def __init__(self, data: bytes, *args, **kwargs):
        super().__init__(self.TYPE, *args, **kwargs)
        self.data = data
        self.rp = len(self._data)
       

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data: bytes):
        '''
        Contenu de la trame (128 bytes max)
        '''
        assert len(data) <= 128, 'RP_Dat frame data must be <= 128 bytes'
        self._data= data
        print("taille(data)= ",len(self._data))
        RP_Dat.Taille = len(self._data)

    def get_repr(self):
        fmt = f'hc{len(self._data)}sc'
        vals = (self._init_sequence, self._type, self.data, self._end_sequence)
        return struct.pack(fmt, *vals)

    @classmethod
    def from_repr(cls, repr: bytes):
        fmt = f'hc{0}sc'
        size = len(repr) - struct.calcsize(fmt)
        fmt = f'hc{size}sc'
        _, type, data, _ = struct.unpack(fmt, repr)
        assert type == cls.TYPE, 'Bad frame type'
        return cls(data)

    @classmethod
    def size(cls):
        '''The RP_Dat frame is represented with 4 + `n` bytes where `n` vary'''
        return 4 + 12 


if __name__ == '__main__':
    # f = Frame()
    f1 = ID_Dat(666)
    print(f1)
    r = f1.get_repr()
    f2 = type(f1).from_repr(r)
    print(f2)

    print('===============')

    f1 = RP_Dat(b'0123456789')
    print(f1)
    r = f1.get_repr()
    f2 = type(f1).from_repr(r)
    print(f2)