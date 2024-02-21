from crawler.hickwall_qmq_crawler import get_subject_produced_by_app, get_subject_consumed_by_app

produced_subject_list = get_subject_produced_by_app("100026856")
consumed_subject_list = get_subject_consumed_by_app("100026856")

print(produced_subject_list)
print(consumed_subject_list)