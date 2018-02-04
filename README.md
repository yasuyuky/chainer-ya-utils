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


### If you want to use the logger you defined

```python
def train(args):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    rangelog.set_logger(logger)
    with rangelog("creating dataset"):
        data = TransformDataset(np.loadtxt(args.data_path, dtype=np.float32),
                                lambda in_data: (in_data[:-1], in_data[-1:]))
        train_set, eval_set = split_dataset_random(data, len(data)*7//10)
    with rangelog("creating iterator") as logger:
        logger.debug("train_set: {}, eval_set: {}".format(len(train_set), len(eval_set)))
        iterator = SerialIterator(train_set, args.batch, repeat=True)
        eval_iterator = SerialIterator(eval_set, args.batch, repeat=False)
    ...
```

### If you want to set start/end message

```python
def train(args):
    rangelog.set_start_msg("start... {name}")
    rangelog.set_end_msg("  end...")
    with rangelog("creating dataset"):
        data = TransformDataset(np.loadtxt(args.data_path, dtype=np.float32),
                                lambda in_data: (in_data[:-1], in_data[-1:]))
        train_set, eval_set = split_dataset_random(data, len(data)*7//10)
    with rangelog("creating iterator") as logger:
        logger.debug("train_set: {}, eval_set: {}".format(len(train_set), len(eval_set)))
        iterator = SerialIterator(train_set, args.batch, repeat=True)
        eval_iterator = SerialIterator(eval_set, args.batch, repeat=False)
    ...
```


## Trainer Extensions ( SourceBackup / ArgumentBackup / FinalRequest / SlackPost )

- SourceBackup: backups source code automatically.
- ArgumentBackup: backups argparse result.
- FinalRequest: requests to some url when training finished.
- SlackPost: posts result to Slack.
- MemoryUsage: record gpu memory usage.

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
        token = "YOUR_SLACK_TOKEN"
        channel = "YOUR_CHANNEL"
        trainer.extend(SlackPost(token, channel))
        url = "https://example.com/webhook"
        trainer.extend(FinalRequest(url, data={"msg": "training finished"}))
        memory_usage = MemoryUsage()
        trainer.extend(memory_usage)
    ...
    with rangelog("training"):
        trainer.run()
    print(max(memory_usage.total))
    ...
```

# License

MIT
