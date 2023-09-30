import json

from griptape.artifacts import TextArtifact
from griptape.utils.decorators import activity
from griptape.tools import BaseTool
from schema import Schema, Literal


class CharacterSheetUpdater(BaseTool):
    @activity(
        config={
            "description": "Can be used to update the player's character sheet and return the updated sheet as json",
            "schema": Schema(
                {
                    Literal(
                        "new_vals", description="A json of ability score bonuses"
                    ): str,
                    Literal(
                        "character_sheet", description="A character sheet json"
                    ): str,
                }
            ),
        }
    )
    def update_character_sheet(self, params: dict) -> TextArtifact:
        sheet = json.loads(params["values"]["character_sheet"])
        for k, v in json.loads(params["values"].get("new_vals"))[
            "ability_scores"
        ].items():
            sheet["ability_scores"][k] += v
        return TextArtifact(json.dumps(sheet))
