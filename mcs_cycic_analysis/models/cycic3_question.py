from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class Cycic3Question:
    answer_option0: str
    answer_option1: str
    blanks: bool
    categories: List[str]
    guid: str
    question: str
    questionType: str
    run_id: int

