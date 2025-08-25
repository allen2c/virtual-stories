from str_or_none import str_or_none

from virtual_stories import (
    list_dialogues,
    list_domains,
    list_topics,
    read_story_raw_text,
)


def test_list_domains():
    """Test that list_domains returns valid domains including automotive."""
    domains = list_domains()
    assert len(domains) > 0
    assert "automotive" in domains


def test_list_topics():
    """Test that list_topics returns valid topics for automotive domain."""
    topics = list_topics("automotive")
    assert len(topics) > 0
    assert "after_sales_service" in topics


def test_read_all_stories():
    """Test that all story files can be read and are valid across all domains."""
    domains = list_domains()
    for domain in domains:
        topics = list_topics(domain)
        for topic in topics:
            for dialogue in list_dialogues(domain, topic):
                _, _, _seq, _dialogue_name, _lang, _raw_text = read_story_raw_text(
                    domain, topic, dialogue_name=dialogue
                )
                read_story_raw_text(domain, topic, seq_num=_seq)
                read_story_raw_text(domain, topic, dialogue_name=_dialogue_name)
                assert _lang
                assert str_or_none(_raw_text)
