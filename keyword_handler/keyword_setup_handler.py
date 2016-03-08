__CONTEXT_WORDS_KEY = "context_words"
__REFERENCE_WORDS_KEY = "reference_words"


def get_no_reference_word_in_context_words_setup(original_keyword_setup):
    print("romve_all_reference_word_from context setup")
    for category in original_keyword_setup[__REFERENCE_WORDS_KEY]:
        for word_group_id in original_keyword_setup[__REFERENCE_WORDS_KEY][category]:
            reference_words = original_keyword_setup[__REFERENCE_WORDS_KEY][category][word_group_id]
            context_words = original_keyword_setup[__CONTEXT_WORDS_KEY][category][word_group_id]
            context_words_set = set(context_words)
            for reference_word in reference_words:
                if reference_word in context_words_set:
                    context_words_set.remove(reference_word)
            original_keyword_setup[__CONTEXT_WORDS_KEY][category][word_group_id] = list(context_words_set)

    return original_keyword_setup

def get_all_reference_word_in_context_word_setup(original_keyword_setup):
    print("add_all_reference_word_from context setup")
    for category in original_keyword_setup[__REFERENCE_WORDS_KEY]:
        for word_group_id in original_keyword_setup[__REFERENCE_WORDS_KEY][category]:
            reference_words = original_keyword_setup[__REFERENCE_WORDS_KEY][category][word_group_id]
            context_words = original_keyword_setup[__CONTEXT_WORDS_KEY][category][word_group_id]
            context_words_set = set(context_words)
            for reference_word in reference_words:
                    context_words_set.add(reference_word)
            original_keyword_setup[__CONTEXT_WORDS_KEY][category][word_group_id] = list(context_words_set)
    return original_keyword_setup