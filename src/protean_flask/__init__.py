from protean.conf import active_config

from . import config
from .core.base import Protean

__version__ = '0.0.2'

__all__ = ('Protean',)


# Update the config here so that loading the repo will load the config
active_config.update_defaults(config)
