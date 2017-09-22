import os
import requests
import json
from chainer.training import extension


class SlackPost(extension.Extension):

    def __init__(self, token, channel, **kwargs):
        self.token = token
        self.channel = channel
        self.priority = 50

    def initialize(self, trainer):
        try:
            plot_report = trainer.get_extension("PlotReport")
        except:
            pass
        else:
            self.plotfilepath = os.path.join(trainer.out,
                                             plot_report._file_name)

        try:
            args = trainer.get_extension("ArgumentBackup").args
        except:
            pass
        else:
            self.args = ["{}:\t{}".format(k,getattr(args, k))
                         for k in vars(args)]

    def finalize(self):
        msgs = ["Training finished"]
        attachments = []
        if hasattr(self, "args"):
            msgs += self.args
        if hasattr(self, "plotfilepath"):
            data = {
                "token": self.token,
                "channels": self.channel,
                "initial_comment": "\n".join(msgs),
            }
            files = {'file': open(self.plotfilepath, 'rb')}
            requests.post("https://slack.com/api/files.upload",
                          data=data, files=files)
        else:
            data = {
                "token": self.token,
                "channel": self.channel,
                "as_user": False,
                "text": "\n".join(msgs),
                "icon_url": "https://chainer.org/images/chainer_icon_red.png",
                "unfurl_media": True,
                "attachments": json.dumps(attachments),
                "username": "Chainer Result",
            }
            requests.post("https://slack.com/api/chat.postMessage",
                          data=data)
