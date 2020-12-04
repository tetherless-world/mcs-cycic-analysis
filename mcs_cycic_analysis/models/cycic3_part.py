from dataclasses import dataclass
from typing import Tuple, Dict

from mcs_cycic_analysis.models.cycic3_label import Cycic3Label
from mcs_cycic_analysis.models.cycic3_question import Cycic3Question


@dataclass
class Cycic3Part:
    labels: Tuple[Cycic3Label, ...]
    labels_by_run_id: Dict[str, Cycic3Label]
    letter: str
    questions: Tuple[Cycic3Question, ...]
    questions_by_run_id: Dict[str, Cycic3Question]

    def __post_init__(self):
        if len(self.labels) != len(self.questions):
            raise ValueError(
                f"unequal number of labels ({len(self.labels)}) and questions ({len(self.questions)})"
            )
