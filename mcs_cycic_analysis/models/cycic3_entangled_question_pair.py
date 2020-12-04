from dataclasses import dataclass

from mcs_cycic_analysis.models.cycic3_label import Cycic3Label
from mcs_cycic_analysis.models.cycic3_question import Cycic3Question


@dataclass
class Cycic3EntangledQuestionPair:
    part_a_question: Cycic3Question
    part_a_label: Cycic3Label
    part_b_question: Cycic3Question
    part_b_label: Cycic3Label
