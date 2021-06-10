import io
from typing import Dict, List, Optional

from .petit_python_publipost_connector import Template, make_connector


class T(Template):
    def __init__(self, _file: io.BytesIO):
        super().__init__(_file)
    def render(self, data: Dict[str, object], options: Optional[List[str]]) -> io.BytesIO:
        return super().render(data, options)

app = make_connector(T)
