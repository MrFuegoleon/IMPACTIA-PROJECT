from transformers import pipeline
classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")

sequence_to_classify = "Coca-Cola, sometimes abbreviated as Coca-Cola in French-speaking countries or Coke in North America and some European and African countries, is an American brand of cola-type soda manufactured by The Coca-Cola Company. This trademark was registered in 1886. This name comes from two ingredients used for its original composition: the coca leaf and the kola nut."

candidate_labels = ['cooking','exploration','travel', 'dancing', 'Music']
res=classifier(sequence_to_classify, candidate_labels)
#{'labels': ['travel', 'exploration', 'dancing', 'cooking'],
# 'scores': [0.9945111274719238,
#  0.9383890628814697,
#  0.0057061901316046715,
#  0.0018193122232332826],
# 'sequence': 'one day I will see the world'}
print(res)
