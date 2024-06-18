from transformers import pipeline


classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")


sequence_to_classify = "one day I will see the world"
candidate_labels = ['cooking','travel','dancing']

A1=classifier(sequence_to_classify, candidate_labels)


candidate_labels = ['travel', 'cooking','exploration','dancing', ]
A2=classifier(sequence_to_classify, candidate_labels, multi_label=True)

print(A1)
print(A2)

