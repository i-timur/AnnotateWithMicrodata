import os.path

import click

from src.common.constants import CLASS_MAP


class HTMLInput(click.ParamType):
    name = "HTMLInput"

    def convert(self, value, param, ctx):
        if os.path.exists(os.path.expanduser(value)):
            with open(os.path.expanduser(value), "rt") as file:
                html = file.read()
        elif value.startswith('http://') or value.startswith('https://'):
            self.fail(f'URL input is not supported yet', param, ctx)
        else:
            html = value

        # TODO: Validate HTML before proceeding.
        if True:
            return html
        else:
            self.fail(f'HTML input is not valid', param, ctx)

class SkipItems(click.ParamType):
    name = "SkipItems"

    def convert(self, value, param, ctx):
        types = map(lambda schema: schema.split('/')[3], [item for _, item in CLASS_MAP.items()])

        values = value.split(',')

        for item in values:
            if item not in types:
                self.fail(f'{item} is not a valid type', param, ctx)

        return list(map(lambda item: 'https://schema.org/' + item, values))
