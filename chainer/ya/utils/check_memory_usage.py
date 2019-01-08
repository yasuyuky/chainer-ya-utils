import chainer
from chainer.training import extension


class MemoryUsage(extension.Extension):
    def __init__(self, trigger=(1, "epoch")):
        self.total = []
        self.trigger = trigger

    def initialize(self, _):
        if chainer.cuda.available:
            chainer.cuda.memory_pool.free_all_blocks()

    def __call__(self, _):
        if chainer.cuda.available:
            total = chainer.cuda.memory_pool.total_bytes() / (1024 * 1024)
            self.total.append(total)

    def finalize(self):
        pass
