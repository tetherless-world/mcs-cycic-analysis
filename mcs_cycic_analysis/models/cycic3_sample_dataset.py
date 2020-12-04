import csv
import json
from dataclasses import dataclass
from typing import Tuple

from mcs_cycic_analysis.models.cycic3_entangled_question_pair import (
    Cycic3EntangledQuestionPair,
)
from mcs_cycic_analysis.models.cycic3_label import Cycic3Label
from mcs_cycic_analysis.models.cycic3_part import Cycic3Part
from mcs_cycic_analysis.models.cycic3_question import Cycic3Question
from mcs_cycic_analysis.paths import DATA_DIR_PATH


@dataclass(frozen=True)
class Cycic3SampleDataset:
    entangled_question_pairs: Tuple[Cycic3EntangledQuestionPair, ...]
    part_a: Cycic3Part
    part_b: Cycic3Part

    @classmethod
    def load(cls):
        def read_jsonl_file(*, jsonl_file_stem: str, model_class):
            with open(DATA_DIR_PATH / (jsonl_file_stem + ".jsonl")) as jsonl_file:
                for line in jsonl_file:
                    line = line.strip()
                    if not line:
                        continue
                    json_object = json.loads(line)
                    yield model_class.from_json(json_object)

        def read_part(letter):
            labels = tuple(
                read_jsonl_file(
                    jsonl_file_stem=f"cycic3{letter}_sample_labels",
                    model_class=Cycic3Label,
                )
            )

            questions = tuple(
                read_jsonl_file(
                    jsonl_file_stem=f"cycic3{letter}_sample_questions",
                    model_class=Cycic3Question,
                )
            )

            return Cycic3Part(
                labels=labels,
                labels_by_run_id={label.run_id: label for label in labels},
                letter=letter,
                questions=questions,
                questions_by_run_id={
                    question.run_id: question for question in questions
                },
            )

        part_a = read_part("a")
        part_b = read_part("b")

        links = {}
        reverse_links = {}
        with open(
            DATA_DIR_PATH / "cycic3_question_links.csv"
        ) as question_links_csv_file:
            for row in csv.DictReader(question_links_csv_file):
                cycic3a = row["cycic3a"]
                cycic3b = row["cycic3b"]
                assert cycic3a not in links, cycic3a
                links[cycic3a] = cycic3b
                assert cycic3b not in reverse_links, cycic3b
                links[cycic3b] = cycic3a

        entangled_question_pairs = []
        for cycic3a_question_run_id, cycic3b_question_run_id in links.items():
            entangled_question_pairs.append(
                Cycic3EntangledQuestionPair(
                    part_a_question=part_a.questions_by_run_id[cycic3a_question_run_id],
                    part_a_label=part_a.labels_by_run_id[cycic3a_question_run_id],
                    part_b_question=part_b.questions_by_run_id[cycic3b_question_run_id],
                    part_b_label=part_b.questions_by_run_id[cycic3b_question_run_id],
                )
            )

        return cls(
            entangled_question_pairs=tuple(entangled_question_pairs),
            part_a=part_a,
            part_b=part_b,
        )
