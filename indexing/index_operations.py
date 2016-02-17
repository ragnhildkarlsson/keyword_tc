
def get_merged_posting_lists(posting_list_1, posting_list_2):
    result =[]
    p1_index = 0
    p2_index = 0
    while(p1_index<len(posting_list_1)) and (p2_index<len(posting_list_2)):
        p1_doc_id = posting_list_1[p1_index][0]
        p1_doc_freq = posting_list_1[p1_index][1]
        p2_doc_id = posting_list_2[p2_index][0]
        p2_doc_freq = posting_list_2[p2_index][1]

        if p1_doc_id == p2_doc_id:
            result.append((p1_doc_id,p1_doc_freq+p2_doc_freq))
            p1_index += 1
            p2_index += 1
        elif p1_doc_id < p2_doc_id:
            result.append((p1_doc_id,p1_doc_freq))
            p1_index += 1
        else:
            result.append((p2_doc_id,p2_doc_freq))
            p2_index += 1

    while p1_index< len(posting_list_1):
        p1_doc_id = posting_list_1[p1_index][0]
        p1_doc_freq = posting_list_1[p1_index][1]
        result.append((p1_doc_id, p1_doc_freq))
        p1_index += 1

    while p2_index < len(posting_list_2):
        p2_doc_id = posting_list_2[p2_index][0]
        p2_doc_freq = posting_list_2[p2_index][1]
        result.append((p2_doc_id,p2_doc_freq))
        p2_index += 1
    return result


def get_document_frequency(index_term, index):
    posting_list = index["index"][index_term]
    n_document_in_index = index["n_documents"]
    return len(posting_list)/n_document_in_index


def intersection_search(posting_list_1, posting_list_2):
    result =[]
    p1_index = 0
    p2_index = 0
    while(p1_index<len(posting_list_1)) and (p2_index<len(posting_list_2)):
        p1_doc_id = posting_list_1[p1_index][0]
        p2_doc_id = posting_list_2[p2_index][0]
        if p1_doc_id == p2_doc_id:
            result.append(p1_doc_id)
            p1_index += 1
            p2_index += 1
        elif p1_doc_id < p2_doc_id:
            p1_index += 1
        else:
            p2_index += 1

    return result