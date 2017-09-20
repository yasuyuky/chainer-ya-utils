# chainer-ya-utils

Yet Another Utilities for Chainer

# Installation

```
pip install git+https://github.com/yasuyuky/chainer-ya-utils
```

# Usage

```python
from chainer.ya.utils import rangelog, SourceBackup, ArgumentBackup, FinalRequest
```


## rangelog

range based logger

```python
def train(args):
    with rangelog("creating dataset"):
        data = TransformDataset(np.loadtxt(args.data_path, dtype=np.float32),
                                lambda in_data: (in_data[:-1], in_data[-1:]))
        train_set, eval_set = split_dataset_random(data, len(data)*7//10)
    with rangelog("creating iterator") as logger:
        logger.info("train_set: {}, eval_set: {}"
                    .format(len(train_set), len(eval_set)))
        iterator = SerialIterator(train_set, args.batch, repeat=True)
        eval_iterator = SerialIterator(eval_set, args.batch, repeat=False)
    ...
```

Above code output like this.

```
--> Start: creating dataset
<-- End: creating dataset
--> Start: creating iterator
train_set: 7000, eval_set: 3000
<-- End: creating iterator
```

## Trainer Extensions ( SourceBackup / ArgumentBackup / FinalRequest )

- SourceBackup: backups source code automatically.
- ArgumentBackup: backups argparse result.
- FinalRequest: requests to some url when training finished.

```python

def train(args):
    ...
    with rangelog("creating trainer"):
        updater = StandardUpdater(iterator=iterator,
                                  optimizer=optimizer,
                                  device=args.device)
        trainer = training.Trainer(updater, (args.epoch, 'epoch'),
                                   out=args.store)
    with rangelog("trainer extension") as logger:
        trainer.extend(extensions.LogReport())
        trainer.extend(SourceBackup())
        trainer.extend(ArgumentBackup(args))
        url = "https://example.com/webhook"
        trainer.extend(FinalRequest(url, data={"msg": "training finished"}))
    ...
```

# License

MIT
