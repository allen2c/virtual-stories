from virtual_stories import (
    list_dialogues,
    list_domains,
    list_topics,
    read_dialogue,
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
    dialogues_count = 0
    messages_count = 0

    domains = list_domains()
    for domain in domains:
        topics = list_topics(domain)
        for topic in topics:
            for dialogue in list_dialogues(domain, topic):
                _dialogue = read_dialogue(domain, topic, dialogue_name=dialogue)
                _dialogue.dialogue_full_name
                assert len(_dialogue.messages) > 0
                messages_count += len(_dialogue.messages)
                dialogues_count += 1
    print(f"Total dialogues: {dialogues_count}")
    print(f"Total messages: {messages_count}")
