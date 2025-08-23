import pathlib
import re
import typing

import pydantic
import universal_message as um
from google_language_support import LanguageCodes
from openai.types.shared.function_definition import FunctionDefinition

__version__ = pathlib.Path(__file__).parent.joinpath("VERSION").read_text().strip()

_package_root = pathlib.Path(__file__).parent
_stories_root = _package_root.joinpath("stories")

STORY_FILE_PATTERN = (
    "stories/{DOMAIN}/{TOPIC}/{SEQ_NUM}_{DIALOGUE_NAME}_{LANGUAGE_CODE}.txt"
)


def list_domains() -> typing.List[str]:
    """List domains that contain at least one valid topic with a valid story file."""
    valid_domains: typing.List[str] = []
    for domain_path in _stories_root.iterdir():
        if not domain_path.is_dir():
            continue
        domain_name: str = domain_path.name
        # Skip template or hidden directories
        if "{" in domain_name or "}" in domain_name or domain_name.startswith("_"):
            continue
        has_valid_topic: bool = False
        for topic_path in domain_path.iterdir():
            if not topic_path.is_dir():
                continue
            # Short-circuit as soon as we find one valid story file in any topic
            for file_path in topic_path.glob("*.txt"):
                stem: str = file_path.stem
                try:
                    _ = _stem_to_valid_parts(stem)
                    has_valid_topic = True
                    break
                except Exception:
                    continue
            if has_valid_topic:
                break

        if has_valid_topic:
            valid_domains.append(domain_name)

    return sorted(valid_domains)


def list_topics(domain: str) -> typing.List[str]:
    """List topics in a domain that contain at least one valid story file."""
    domain_root: pathlib.Path = _stories_root.joinpath(domain)
    if not domain_root.is_dir():
        return []

    valid_topics: typing.List[str] = []
    for topic_path in domain_root.iterdir():
        if not topic_path.is_dir():
            continue
        topic_name: str = topic_path.name
        # Check for any file that matches the filename schema, break early when found
        for file_path in topic_path.glob("*.txt"):
            stem: str = file_path.stem
            try:
                _ = _stem_to_valid_parts(stem)
                valid_topics.append(topic_name)
                break
            except Exception:
                continue

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
    topic_root = _stories_root.joinpath(domain, topic)
    if not topic_root.is_dir():
        raise FileNotFoundError(f"Topic root not found: {topic_root}")

    # Require at least one narrowing constraint
    if seq_num is None and dialogue_name is None:
        raise ValueError("Either seq_num or dialogue_name must be provided")

    # Build precise glob pattern based on known filename schema
    seq_glob: str = str(seq_num) if seq_num is not None else "*"
    name_glob: str = dialogue_name if dialogue_name is not None else "*"
    pattern: str = f"{seq_glob}_{name_glob}_*.txt"

    # Deterministic order to avoid filesystem-order nondeterminism
    candidate_paths: typing.List[pathlib.Path] = sorted(topic_root.glob(pattern))

    for dialogue_path in candidate_paths:
        stem: str = dialogue_path.stem
        try:
            resolved_seq_num, name_part, resolved_lang = _stem_to_valid_parts(stem)
        except Exception:
            # Skip files that do not match the expected pattern
            continue

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


class Story(pydantic.BaseModel):
    domain: str
    topic: str
    seq_num: int
    dialogue_name: str
    language_code: LanguageCodes
    description: str = pydantic.Field(default="")
    tools: typing.List[FunctionDefinition] = pydantic.Field(default_factory=list)
    messages: typing.List[um.Message]


# Helper functions
_STEM_RE: typing.Pattern[str] = re.compile(
    r"^(?P<seq>\d+)_(?P<name>.+)_(?P<lang>[A-Za-z0-9_-]+)$"
)


def _stem_to_valid_parts(stem: str) -> typing.Tuple[int, str, LanguageCodes]:
    """Parse file stem into (seq_num, name, language_code)."""
    match: typing.Optional[re.Match[str]] = _STEM_RE.match(stem)
    if match is None:
        raise ValueError(f"Invalid stem format: {stem}")

    seq_str: str = match.group("seq")
    name_part: str = match.group("name")
    lang_str: str = match.group("lang")

    seq_num: int = int(seq_str)
    # First try direct enum lookup; then fallback to common-name resolution
    try:
        language_code: LanguageCodes = LanguageCodes(lang_str)
    except Exception:
        language_code = LanguageCodes.from_common_name(lang_str)

    return seq_num, name_part, language_code
