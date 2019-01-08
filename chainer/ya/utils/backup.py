import ast
import glob
import inspect
import json
import os
import shutil

from chainer.training import extension


class SourceBackup(extension.Extension):
    def __init__(self, backupdir=None):
        self.backupdir = backupdir

    def initialize(self, trainer):
        if not self.backupdir:
            self.backupdir = trainer.out
        root = inspect.stack()[-1][1]
        self.backup_file(root)
        self.retrieve_file(root)

    def retrieve_file(self, filepath):
        try:
            source = open(filepath).read()
        except:
            return
        tree = ast.parse(source)
        for name in self.retrieve_ast(tree):
            if not name: continue
            name_seq = name.split('.')
            path = os.path.join(os.path.dirname(filepath), *name_seq)
            if os.path.exists(path + '.py'):
                self.backup_file(path + '.py')
                self.retrieve_file(path + '.py')
            elif os.path.isdir(path):
                for subpath in glob.glob(os.path.join(path, '*')):
                    self.retrieve_file(subpath)

    def retrieve_ast(self, nodes):
        for node in ast.iter_child_nodes(nodes):
            if isinstance(node, ast.Import):
                yield self.get_import(ast.iter_fields(node))
            elif isinstance(node, ast.ImportFrom):
                yield self.get_import(ast.iter_fields(node))
            else:
                self.retrieve_ast(node)

    def get_import(self, nodes):
        d = dict(nodes)
        if 'module' in d:
            return d['module']
        elif 'names' in d:
            for k, v in ast.iter_fields(d['names'][0]):
                if k == 'name':
                    return v

    def backup_file(self, f):
        dst = os.path.join(self.backupdir, f)
        if not os.path.exists(os.path.dirname(dst)):
            os.makedirs(os.path.dirname(dst))
        os.chmod(os.path.dirname(dst), 0o755)
        shutil.copyfile(f, dst)


class ArgumentBackup(extension.Extension):
    def __init__(self, args, filename='args.json', backupdir=None):
        self.args = args
        self.filename = filename
        self.backupdir = backupdir

    def initialize(self, trainer):
        if not self.backupdir:
            self.backupdir = trainer.out
        self.store_args()

    def store_args(self):
        with open(os.path.join(self.backupdir, self.filename), 'w') as f:
            if not os.path.exists(self.backupdir):
                os.makedirs(self.backupdir)
            args_dict = vars(self.args)
            args = {k: args_dict[k] for k in args_dict}
            json.dump(args, f)
