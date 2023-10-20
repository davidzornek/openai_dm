import os
from typing import Optional
from attr import define, field, Factory
from jinja2 import Environment, FileSystemLoader


def abs_path(path: str) -> str:
    return os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, path)
    )


@define(frozen=True)
class J2:
    template_name: Optional[str] = field(default=None)
    templates_dir: str = field(default=abs_path(""), kw_only=True)
    environment: Environment = field(
        default=Factory(
            lambda self: Environment(
                loader=FileSystemLoader(self.templates_dir),
                trim_blocks=True,
                lstrip_blocks=True,
            ),
            takes_self=True,
        ),
        kw_only=True,
    )

    def render(self, **kwargs) -> str:
        return self.environment.get_template(self.template_name).render(kwargs)

    def render_from_string(self, value: str, **kwargs) -> str:
        return self.environment.from_string(value).render(kwargs)
