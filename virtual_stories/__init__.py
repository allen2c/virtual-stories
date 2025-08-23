import pathlib
import typing

import pydantic
import universal_message as um
from google_language_support import LanguageCodes
from openai.types.shared.function_definition import FunctionDefinition

__version__ = pathlib.Path(__file__).parent.joinpath("VERSION").read_text().strip()

_package_root = pathlib.Path(__file__).parent

STORY_FILE_PATTERN = "{DOMAIN}/{TOPIC}/{SEQ_NUM}_{DIALOGUE_NAME}_{LANGUAGE_CODE}.txt"


def list_domains() -> typing.List[str]:
    """List domains that contain at least one valid topic with a valid story file."""
    valid_domains: typing.List[str] = []
    for domain_path in _package_root.iterdir():
        if not domain_path.is_dir():
            continue
        domain_name: str = domain_path.name
        # Skip template or hidden directories
        if "{" in domain_name or "}" in domain_name or domain_name.startswith("_"):
            continue
        domain_topics: typing.List[str] = list_topics(domain_name)
        if domain_topics:
            valid_domains.append(domain_name)
    return sorted(valid_domains)


def list_topics(domain: str) -> typing.List[str]:
    """List topics in a domain that contain at least one valid story file."""
    domain_root: pathlib.Path = _package_root.joinpath(domain)
    if not domain_root.is_dir():
        return []

    valid_topics: typing.List[str] = []
    for topic_path in domain_root.iterdir():
        if not topic_path.is_dir():
            continue
        topic_name: str = topic_path.name
        # Check for any file that matches the filename schema
        has_valid_file: bool = False
        for file_path in topic_path.glob("*.txt"):
            stem: str = file_path.stem
            try:
                seq_part_str, rest = stem.split("_", 1)
                name_part, lang_part = rest.rsplit("_", 1)
                # Validate sequence number
                int(seq_part_str)
                # Validate language code using enum or common name fallback
                try:
                    LanguageCodes(lang_part)
                except Exception:
                    LanguageCodes.from_common_name(lang_part)
                # Ensure dialogue name is non-empty
                if not name_part:
                    continue
                has_valid_file = True
                break
            except Exception:
                continue

        if has_valid_file:
            valid_topics.append(topic_name)

    return sorted(valid_topics)


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
