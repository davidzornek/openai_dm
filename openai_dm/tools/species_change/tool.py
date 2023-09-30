import json

from griptape.artifacts import TextArtifact
from griptape.utils.decorators import activity
from griptape.tools import BaseTool
from schema import Schema, Literal


class RaceChanger(BaseTool):
    @activity(
        config={
            "description": "Updates the players character sheet with a choice of race",
            "schema": Schema(
                {
                    Literal(
                        "new_vals",
                        description="A json containing information about the race",
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
        sheet["race"]["race"] = params["values"]["new_vals"]["race"]
        sheet["race"]["racial_bonuses"] = json.loads(
            params["values"]["new_vals"]["ability_scores"]
        )
        sheet["final_ability_scores"] = sheet["base_ability_scores"]
        for k, v in sheet["race"]["racial_bonuses"].items():
            sheet["final_ability_scores"][k] += v

        return TextArtifact(json.dumps(sheet))
