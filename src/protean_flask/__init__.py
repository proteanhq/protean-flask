from protean.conf import active_config

from .core.base import Protean
from . import config

__version__ = '0.0.1'

__all__ = ('Protean',)


# Update the config here so that loading the repo will load the config
active_config.update_defaults(config)
