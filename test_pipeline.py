from transformers import AutoModelForMaskedLM, AutoTokenizer
from pipeline import FillMaskPipeline
from PARAM import MODEL_NAME_OR_PATH


model = AutoModelForMaskedLM.from_pretrained(MODEL_NAME_OR_PATH)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME_OR_PATH)
# unmasker = FillMaskPipeline(model=model, tokenizer=tokenizer)
unmasker = FillMaskPipeline(model=model, tokenizer=tokenizer, device=0)
# s = 'New York Times, as well as the <mask> is a newspaper.'
s = 'New York Times, as well as the <mask><mask> is a newspaper.'
ls = unmasker(s)
print(ls)

