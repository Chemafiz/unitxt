from typing import Any

from unitxt.blocks import (
    MapInstanceValues,
    Rename,
    TaskCard,
)
from unitxt.catalog import add_to_catalog
from unitxt.llm_as_judge_constants import DirectCriteriaCatalogEnum
from unitxt.loaders import LoadJsonFile
from unitxt.operators import Copy, Set
from unitxt.task import Task
from unitxt.test_utils.card import test_card

card = TaskCard(
    loader=LoadJsonFile(
        files={
            "test": "https://raw.githubusercontent.com/dmg-illc/JUDGE-BENCH/refs/heads/master/data/cola/cola.json",
        },
        data_classification_policy=["public"],
        data_field="instances",
    ),
    preprocess_steps=[
        Rename(field="instance", to_field="response"),
        Rename(field="annotations/grammaticality/majority_human", to_field="label"),
        Copy(field="label", to_field="label_value"),
        MapInstanceValues(
            mappers={
                "label_value": DirectCriteriaCatalogEnum.GRAMMAR_AND_PUNCTUATION.value.option_map,
            }
        ),
        Set(
            fields={
                "criteria": "metrics.llm_as_judge.direct.criteria.grammar_and_punctuation"
            }
        ),
    ],
    task=Task(
        input_fields={"response": str, "label": str, "criteria": Any},
        reference_fields={"label_value": float},
        prediction_type=float,
        metrics=["metrics.accuracy", "metrics.f1_macro"],
        default_template="templates.empty[postprocessors=[processors.cast_to_float_return_nan_if_failed]]",
    ),
    templates=[],
)

test_card(card, demos_taken_from="test", strict=False)

add_to_catalog(
    card,
    "cards.judge_bench.cola.grammaticality",
    overwrite=True,
)
