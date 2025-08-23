import pathlib
import typing

import pydantic
import universal_message as um
from google_language_support import LanguageCodes
from openai.types.shared.function_definition import FunctionDefinition

__version__ = pathlib.Path(__file__).parent.joinpath("VERSION").read_text().strip()

_package_root = pathlib.Path(__file__).parent

STORY_FILE_PATTERN = "{DOMAIN}/{TOPIC}/{SEQ_NUM}_{DIALOGUE_NAME}_{LANGUAGE_CODE}.txt"


def read_story_raw_text(
    domain: str,
    topic: str,
    seq_num: int | None = None,
    dialogue_name: str | None = None,
) -> typing.Tuple[
    typing.Annotated[str, "Domain"],
    typing.Annotated[str, "Topic"],
    typing.Annotated[int, "Sequence Number"],
    typing.Annotated[str, "Dialogue Name"],
    typing.Annotated[LanguageCodes, "LanguageCode"],
    typing.Annotated[str, "Raw Plain Text Content"],
]:
    """Read story file matching constraints; return resolved metadata and content."""
    topic_root = _package_root.joinpath(domain, topic)
    if not topic_root.is_dir():
        raise FileNotFoundError(f"Topic root not found: {topic_root}")

    # Require at least one narrowing constraint
    if seq_num is None and dialogue_name is None:
        raise ValueError("Either seq_num or dialogue_name must be provided")

    # Build precise glob pattern based on known filename schema
    seq_glob: str = str(seq_num) if seq_num is not None else "*"
    name_glob: str = dialogue_name if dialogue_name is not None else "*"
    pattern: str = f"{seq_glob}_{name_glob}_*.txt"

    for dialogue_path in topic_root.glob(pattern):
        stem: str = dialogue_path.stem
        try:
            seq_part_str, rest = stem.split("_", 1)
            name_part, lang_part = rest.rsplit("_", 1)
            resolved_seq_num: int = int(seq_part_str)
            try:
                resolved_lang: LanguageCodes = LanguageCodes(lang_part)
            except Exception:
                resolved_lang = LanguageCodes.from_common_name(lang_part)
        except Exception as exc:
            raise ValueError(
                f"Filename does not match expected pattern: {dialogue_path.name}"
            ) from exc

        return (
            domain,
            topic,
            resolved_seq_num,
            name_part,
            resolved_lang,
            dialogue_path.read_text(),
        )

    raise FileNotFoundError(
        f"No dialogue found for {domain}/{topic} with pattern {pattern}"
    )


"virtual_stories/automotive/after_sales_service/1_warranty_repair_request_en.txt"


class Story(pydantic.BaseModel):
    domain: str
    topic: str
    seq_num: int
    dialogue_name: str
    language_code: LanguageCodes
    description: str = pydantic.Field(default="")
    tools: typing.List[FunctionDefinition] = pydantic.Field(default_factory=list)
    messages: typing.List[um.Message]
