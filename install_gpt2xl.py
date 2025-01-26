from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "gpt2-xl"
save_directory = "./local_gpt2_xl"

print("Downloading the tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.save_pretrained(save_directory)

print("Downloading the model...")
model = AutoModelForCausalLM.from_pretrained(model_name)
model.save_pretrained(save_directory)

print(f"Model and tokenizer saved to {save_directory}")
