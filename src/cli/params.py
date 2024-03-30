import os.path

import click

class HTMLInput(click.ParamType):
    name = "HTMLInput"

    def convert(self, value, param, ctx):
        if os.path.exists(os.path.expanduser(value)):
            with open(os.path.expanduser(value), "rt") as file:
                html = file.read()
        else:
            html = value

        # TODO: Validate HTML before proceeding.
        if True:
            return html
        else:
            self.fail(f'HTML input is not valid', param, ctx)
