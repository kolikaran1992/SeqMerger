from merge_subseq.main import MergeSubSeq

seq_merge = MergeSubSeq()

pairs = [
    (
        'I do not have the power',
        'I will have the power'
    ),
    (
        'power',
        'I will have the power'
    ),
    (
        'We want the power',
        'I have the power'
    ),
    (
        'I have power',
        'I have the power'
    )

]
for s1, s2 in pairs:
    a = seq_merge.extract(s1, s2)
    print(a)