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
        """7 year old victim discovered strangled in bed; victim\u2019s mother also found deceased in residence with head trauma, and the suspect, victim\u2019s stepfather, found hanging from a stairway""",
        """7-year-old victim discovered strangled in bed; victim\u2019s mother also found deceased in residence with head trauma, and the suspect, victim\u2019s stepfather, found hanging from a stairway"""
    )
]
for s1, s2 in pairs[-1:]:
    a = seq_merge.extract(s1, s2)
    print(a)

print("""7 year old victim discovered strangled in bed; victim\u2019s mother also found deceased in residence with head trauma, and the suspect, victim\u2019s stepfather, found hanging from a stairway"""[8:])