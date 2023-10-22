from openai_dm.tools import RaceTool, ClassTool, CharacterSheetInspector

COST_PER_1000_TOKENS = {
    "text-davinci-003": {
        "input": 0.002,
        "output": 0.002,
    },
    "gpt-3.5-turbo": {
        "input": 0.0015,
        "output": 0.002,
    },
    "gpt-4": {
        "input": 0.03,
        "output": 0.06,
    },
}

NODE_RULES = {
    "race": [
        "After the player indicates their choice of race, use the appropriate tool to update their character sheet.",  # noqa: E501
    ],
    "class_": [
        "After the player indicates their choice of class, use the appropriate tool to update their character sheet.",  # noqa: E501
    ],
}

NODE_TOOLS = {
    "race": [RaceTool, CharacterSheetInspector],
    "class_": [ClassTool, CharacterSheetInspector],
}
