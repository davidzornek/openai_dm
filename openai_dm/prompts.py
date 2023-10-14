# flake8: noqa
from langchain.prompts.prompt import PromptTemplate

RACE_CHANGE_EXAMPLES = [
    """Input: I'll be a wood elf.
Thought: I need to use the CharacterSheetUpdater tool to update the race to wood elf.
Action: CharacterSheetUpdater.update_race(race="wood elf", racial_bonuses={"dexterity": 2})
Observation: {"race": "wood elf", racial_bonuses={"dexterity": 2}
Thought: The character sheet has been updated.
Action: Finish["race"]""",
    """Input: Teifling sounds fun to me.
Thought: I need to use the CharacterSheetUpdater tool to update the race to human.
Action: CharacterSheetUpdater.update_race(race="human", racial_bonuses={"dexterity": 2})
Observation: {"race": "wood elf", racial_bonuses={"dexterity": 2}
Thought: The character sheet has been updated.
Action: Finish["race"]""",
]
SUFFIX = f"""\Input: {input} | {agent_scratchpad}"""

RACE_CHANGE_PROMPT_TEMPLATE = PromptTemplate.from_examples(
    EXAMPLES, SUFFIX, ["input", "agent_scratchpad"]
)
