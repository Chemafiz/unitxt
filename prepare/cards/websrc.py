from unitxt import get_from_catalog
from unitxt.blocks import LoadHF, Set, TaskCard
from unitxt.catalog import add_to_catalog
from unitxt.collections_operators import Wrap
from unitxt.image_operators import DecodeImage, ToImage
from unitxt.operators import Shuffle
from unitxt.splitters import RenameSplits
from unitxt.test_utils.card import test_card

templates = get_from_catalog("templates.qa.with_context.all")

card = TaskCard(
    loader=LoadHF(path="rootsautomation/websrc", streaming=True),
    preprocess_steps=[
        Shuffle(),
        RenameSplits(mapper={"train": "train", "dev": "test"}),
        "splitters.small_no_dev",
        Wrap(field="answer", inside="list", to_field="answers"),
        DecodeImage(field="image", to_field="context"),
        ToImage(field="context"),
        Set(fields={"context_type": "image"}),
    ],
    task="tasks.qa.with_context.with_domain[metrics=[metrics.websrc_squad_f1]]",
    templates=["templates.qa.with_context.websrc", *templates.items],
    __tags__={
        "license": "Unknown",
        "multilinguality": "monolingual",
        "modalities": ["image", "text"],
        "size_categories": "10K<n<100K",
        "task_categories": "question-answering",
        "task_ids": "extractive-qa",
    },
    __description__=(
        "WebSRC v1.0 is a dataset for reading comprehension on structural web pages. The task is to answer questions about web pages, which requires a system to have a comprehensive understanding of the spatial structure and logical structure. WebSRC consists of 6.4K web pages and 400K question-answer pairs about web pages. This cached copy of the dataset is focused on Q&A using the web screenshots (HTML and other metadata are omitted). Questions in WebSRC were created for each segment. Answers are either text spans from web pages or yes/no."
    ),
)

test_card(card)
add_to_catalog(card, "cards.websrc", overwrite=True)
