from mcs_cycic_analysis.models.cycic3_sample_dataset import Cycic3SampleDataset


def test_load():
    dataset = Cycic3SampleDataset.load()
    assert len(dataset.entangled_question_pairs) == 100
    for part in (dataset.part_a, dataset.part_b):
        assert len(part.questions) == 100
