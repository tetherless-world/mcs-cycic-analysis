import csv
from copy import copy
from typing import Tuple, Dict, Optional

from mcs_cycic_analysis.cli.commands._command import _Command
from mcs_cycic_analysis.models.cycic3_label import Cycic3Label
from mcs_cycic_analysis.models.cycic3_question import Cycic3Question
from mcs_cycic_analysis.models.cycic3_sample_dataset import Cycic3SampleDataset
from mcs_cycic_analysis.paths import DATA_DIR_PATH


class CreateSpreadsheetsCommand(_Command):
    def __call__(self):
        dataset = Cycic3SampleDataset.load()
        self.__create_entangled_question_pair_csv_file(dataset=dataset)

    def __create_entangled_question_pair_csv_file(self, dataset: Cycic3SampleDataset):
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
                # prefix + "guid": question.guid,
                prefix
                + "run_id": question.run_id,
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
