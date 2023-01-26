from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
print(torch.cuda.is_available())

checkpoint = "gpt2-medium"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForCausalLM.from_pretrained(checkpoint)
print(checkpoint + ' model created!')

prompt = ' '
while prompt != 'end':
    prompt = input()
    inputs = tokenizer(prompt, return_tensors="pt")

    # Using contrastive search
    # https://huggingface.co/docs/transformers/v4.26.0/en/generation_strategies#customize-text-generation
    outputs = model.generate(**inputs, penalty_alpha=0.6, top_k=4, max_new_tokens=50)
    print(tokenizer.batch_decode(outputs, skip_special_tokens=True)[0])


