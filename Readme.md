# Python publipost connector

This connector is meant to get used with the [petit_publipost_gateway](https://github.com/Plawn/petit_publipost_gateway)

It's a connector which can used in order to create a new publipost engine

As of now, it works using an HTTP interface, handled by an express server.

It implements the required endpoints needed to work with the [petit_publipost_gateway](https://github.com/Plawn/petit_publipost_gateway)

- POST /publipost
- POST /get_placeholders
- GET /list
- DELETE /remove_template
- POST /load_templates
- GET /live
- POST /configure

It is used by :

- [petit_html_engine](https://github.com/Plawn/petit_html_engine)
- [petit_docx_engine](https://github.com/Plawn/petit_docx_engine)

It exposes 2 things:

- make_connector
- Template

Example:

```python
# ...
import io
import re
from typing import Dict, List, Optional

import pdfkit
from jinja2 import Template as JinjaTemplate
from petit_python_publipost_connector import Template as BaseTemplate, make_connector

local_funcs: List[str] = []


def extract_variable(var: str):
    """Extracts variable and removes some stuff
    """
    # remove the '(' and ')'
    # in the case values in {{data + "test"}}
    # we want to get the 'data' part
    r = var.split('+')
    r = [
        i
        .replace('(', "")
        .replace(')', "")
        .strip()
        for i in r if '"' not in i
    ]
    return r


def get_placeholder(text: str, local_funcs: List[str]) -> List[str]:
    for name in local_funcs:
        text = text.replace(name, '')
    # finding between {{ }}
    res: List[str] = re.findall(
        r"\{{(.*?)\}}", text, re.MULTILINE
    )
    # finding between {% %}
    res2 = []
    for i in res:
        res2.extend(extract_variable(i.strip()))
    return res2


class BytesIO(io.BytesIO):
    @staticmethod
    def of(content: bytes):
        f = io.BytesIO()
        f.write(content)
        return f


class Template(BaseTemplate):

    def __init__(self, _file: io.BytesIO):
        self.fields: List[str] = list()
        self.content = _file.getvalue().decode('utf-8')
        self.template = JinjaTemplate(self.content)
        self.__load_fields()

    def __load_fields(self):
        self.fields = fields = get_placeholder(self.content, local_funcs)
        return fields

    def __apply_template(self, data: Dict[str, str]) -> str:
        """
        Applies the data to the template and returns a `Template`
        """
        return self.template.render(data)

    def render(self, data: Dict[str, object], options: Optional[List[str]]) -> io.BytesIO:
        rendered = self.__apply_template(data)
        # if need pdf conversion
        # if options is not None and 'pdf' in options:
        if True:
            # always true for now
            rendered = pdfkit.from_string(rendered, output_path=False)
        return BytesIO.of(rendered)



app = make_connector(Template)

```
