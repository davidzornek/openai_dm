from dataclasses import asdict

from griptape.utils.decorators import activity
from griptape.tools import BaseTool
from schema import Schema, Literal

from openai_dm.character_sheet import (
    Character,
)


class CharacterSheetInspector(BaseTool):
    def __init__(self, character_sheet: Character, **kwargs):
        super().__init__(**kwargs)
        self.character_sheet = character_sheet

    @activity(
        config={
            "description": "Use this whenever you need information about a players character.",
            "schema": Schema(
                {
                    Literal(
                        "fields",
                        description=f"""
                        A list of attributes to obtain from the character sheet.
                        Must me a subset of {list(Character.__dataclass_fields__.keys())}
                        Example 1:
                        ["race", "class_"]
                        Example 2:
                        ['saving_throw_proficiences', 'skill_proficiences']
                        """,
                    ): list,
                }
            ),
        }
    )
    def query_character_sheet(self, params: dict) -> Character:
        output = {
            k: getattr(self.character_sheet, k) for k in params["values"]["fields"]
        }
        return {
            k: asdict(v) if not isinstance(v, str) else v for k, v in output.items()
        }
