# dot.py

class Dot(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delattr__

    def __init__(self, d):
        super().__init__()
        for key, value in d.items():
            if hasattr(value, 'keys'):
                value = Dot(value)
            self[key] = value
