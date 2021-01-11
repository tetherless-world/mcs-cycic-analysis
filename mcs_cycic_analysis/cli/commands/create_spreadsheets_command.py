import csv
from copy import copy
from typing import Tuple, Dict, Optional

from mcs_cycic_analysis.cli.commands._command import _Command
from mcs_cycic_analysis.models.cycic3_label import Cycic3Label
from mcs_cycic_analysis.models.cycic3_part import Cycic3Part
from mcs_cycic_analysis.models.cycic3_question import Cycic3Question
from mcs_cycic_analysis.models.cycic3_sample_dataset import Cycic3SampleDataset
from mcs_cycic_analysis.paths import DATA_DIR_PATH


class CreateSpreadsheetsCommand(_Command):
    def __call__(self):
        dataset = Cycic3SampleDataset.load()
        self.__create_all_questions_csv_file(dataset=dataset)
        self.__create_entangled_question_pairs_csv_file(dataset=dataset)
        self.__create_part_csv_file(part=dataset.part_a)
        self.__create_part_csv_file(part=dataset.part_b)

    def __create_all_questions_csv_file(self, dataset: Cycic3SampleDataset):
        self.__write_csv_file(
            file_stem="all_questions",
            row_dicts=tuple(
                list(self.__get_part_question_columns_dicts(dataset.part_a))
                + list(self.__get_part_question_columns_dicts(dataset.part_b))
            ),
        )

    def __create_entangled_question_pairs_csv_file(self, dataset: Cycic3SampleDataset):
        row_dicts = []
        for entangled_question_pair in dataset.entangled_question_pairs:
            row_dict = {}
            row_dict.update(
                self.__get_question_columns_dict(
                    question=entangled_question_pair.part_a_question,
                    label=entangled_question_pair.part_a_label,
                    prefix="part_a_",
                )
            )
            row_dict.update(
                self.__get_question_columns_dict(
                    question=entangled_question_pair.part_b_question,
                    label=entangled_question_pair.part_b_label,
                    prefix="part_b_",
                )
            )
            row_dicts.append(row_dict)
        self.__write_csv_file(
            file_stem="entangled_question_pairs", row_dicts=tuple(row_dicts)
        )

    def __create_part_csv_file(self, *, part: Cycic3Part):
        self.__write_csv_file(
            file_stem=f"part_{part.letter}_questions",
            row_dicts=self.__get_part_question_columns_dicts(part),
        )

    def __get_part_question_columns_dicts(
        self, part: Cycic3Part
    ) -> Tuple[Dict[str, str], ...]:
        row_dicts = []
        for question in part.questions:
            row_dict = {"part": part.letter}
            row_dict.update(
                self.__get_question_columns_dict(
                    question=question, label=part.labels_by_run_id[question.run_id]
                )
            )
            row_dicts.append(row_dict)
        return tuple(row_dicts)

    def __get_question_columns_dict(
        self,
        *,
        question: Cycic3Question,
        label: Optional[Cycic3Label] = None,
        prefix: str = "",
    ) -> Dict[str, str]:
        row_dict = {
            prefix + "question": question.question,
            prefix + "answer_option0": question.answer_option0,
            prefix + "answer_option1": question.answer_option1,
        }
        if label is not None:
            row_dict[prefix + "correct_answer"] = str(label.correct_answer)
        categories_max = 1
        assert len(question.categories) <= categories_max
        categories = copy(question.categories)
        while len(categories) < categories_max:
            categories.append("")
        for category_i, category in enumerate(categories):
            row_dict[f"category{category_i}"] = category
        row_dict.update(
            {
                # prefix + "question_type": question.questionType,
                # prefix + "blanks": str(question.blanks),
                prefix + "guid": question.guid,
                prefix + "run_id": question.run_id,
            }
        )

        return row_dict

    def __write_csv_file(
        self, *, file_stem: str, row_dicts: Tuple[Dict[str, str], ...]
    ):
        assert row_dicts, file_stem
        data_dir_path = DATA_DIR_PATH / "spreadsheets" / "cycic3_sample"
        data_dir_path.mkdir(exist_ok=True, parents=True)
        file_path = data_dir_path / (file_stem + ".csv")
        with open(file_path, "w+", newline="\n") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=tuple(row_dicts[0].keys()))
            writer.writeheader()
            for row_dict in row_dicts:
                writer.writerow(row_dict)
        self._logger.info("wrote %s", file_path)
