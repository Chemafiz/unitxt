import re
from typing import Any

from unitxt.blocks import (
    MapInstanceValues,
    Rename,
    TaskCard,
)
from unitxt.catalog import add_to_catalog
from unitxt.llm_as_judge_constants import DirectCriteriaCatalogEnum
from unitxt.loaders import LoadJsonFile
from unitxt.operators import Copy, FilterByCondition, Set
from unitxt.processors import GroupDictWithRegex
from unitxt.task import Task
from unitxt.test_utils.card import test_card

card = TaskCard(
    loader=LoadJsonFile(
        files={
            "test": "https://raw.githubusercontent.com/dmg-illc/JUDGE-BENCH/refs/heads/master/data/inferential-strategies/inferential_strategies.json",
        },
        data_classification_policy=["public"],
        data_field="instances",
    ),
    preprocess_steps=[
        GroupDictWithRegex(
            field="instance",
            pattern=(
                r".*?### PROBLEM STATEMENT\s+"
                r"(?P<problem_statement>.*?)\s+"
                r"Statements:\s+"
                r"(?P<statements>.*?)\s+"
                r"Let\'s think step by step\.\s*### MODEL RESPONSE\s+"
                r"(?P<model_reasoning>.*)"
            ),
            flags=re.DOTALL,
        ),
        FilterByCondition(
            values={"instance/problem_statement": True}, condition="exists"
        ),
        Rename(
            field_to_field={
                "instance/problem_statement": "problem statement",
                "instance/statements": "statements",
                "instance/model_reasoning": "model reasoning",
                "annotations/Sound Reasoning/majority_human": "label",
            }
        ),
        MapInstanceValues(
            mappers={
                "label": {"no": "No", "yes": "Yes"},
            }
        ),
        Copy(field="label", to_field="label_value"),
        MapInstanceValues(
            mappers={
                "label_value": DirectCriteriaCatalogEnum.LOGICAL_VALIDITY_OF_REASONING.value.option_map,
            }
        ),
        Set(
            fields={
                "criteria": "metrics.llm_as_judge.direct.criteria.logical_validity_of_reasoning"
            }
        ),
    ],
    task=Task(
        input_fields={
            "problem statement": str,
            "statements": str,
            "model reasoning": str,
            "label": str,
            "criteria": Any,
        },
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
    "cards.judge_bench.inferential_strategies.sound_reasoning",
    overwrite=True,
)
