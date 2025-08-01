from datasets import get_dataset_config_names
from unitxt.blocks import (
    LoadHF,
    Rename,
    TaskCard,
)
from unitxt.catalog import add_to_catalog
from unitxt.collections_operators import Wrap
from unitxt.test_utils.card import test_card

configs = get_dataset_config_names("GEM/xlsum", trust_remote_code=True)  # the languages
# now configs is the list of all languages showing in the dataset


langs = configs

for lang in langs:
    card = TaskCard(
        loader=LoadHF(
            path="GEM/xlsum", name=lang, splits=["test", "train", "validation"]
        ),
        preprocess_steps=[
            Rename(field_to_field={"text": "document"}),
            Wrap(field="target", inside="list", to_field="summaries"),
        ],
        task="tasks.summarization.abstractive",
        templates="templates.summarization.abstractive.all",
        __tags__={
            "annotations_creators": "none",
            "arxiv": "1607.01759",
            "language": "und",
            "language_creators": "unknown",
            "license": "cc-by-nc-sa-4.0",
            "multilinguality": "unknown",
            "region": "us",
            "size_categories": "unknown",
            "source_datasets": "original",
            "task_categories": "summarization",
        },
        __description__=(
            "We present XLSum, a comprehensive and diverse dataset comprising 1.35 million professionally annotated article-summary pairs from BBC, extracted using a set of carefully designed heuristics. The dataset covers 45 languages ranging from low to high-resource, for many of which no public dataset is currently available. XL-Sum is highly abstractive, concise, and of high quality, as indicated by human and intrinsic evaluation… See the full description on the dataset page: https://huggingface.co/datasets/GEM/xlsum"
        ),
    )
    if lang == langs[0]:
        test_card(card, debug=False, strict=False)
    add_to_catalog(card, f"cards.xlsum.{lang}", overwrite=True)
