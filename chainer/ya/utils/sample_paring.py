from random import randrange
import chainer


class SamplePairingDataset(chainer.dataset.DatasetMixin):
    '''
    https://arxiv.org/abs/1801.02929
    '''

    def __init__(self, original, rate=1):
        self.original = original
        self.olen = len(self.original)
        self.len = round((1+rate)*self.olen)

    def __len__(self):
        return self.len

    def get_example(self, i):
        if i < self.olen:
            return self.original[i]
        else:
            a = self.original[randrange(self.olen)]
            b = self.original[randrange(self.olen)]
            return ((a[0]+b[0])/2, [a[1],b[1]][randrange(2)])
