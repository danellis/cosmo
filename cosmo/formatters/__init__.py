from cosmo.formatters.nice import NiceFormatter
from cosmo.formatters.raw import RawFormatter
from cosmo.formatters.dot import DotFormatter

formatter_classes = {
    'nice': NiceFormatter,
    'raw': RawFormatter,
    'dot': DotFormatter
}

default_format_name = 'nice'
