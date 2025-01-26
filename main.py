import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, StoppingCriteria, StoppingCriteriaList, GenerationConfig

class StopOnTokens(StoppingCriteria):
    def __init__(self, stop_ids):
        super().__init__()
        self.stop_ids = stop_ids
    def __call__(self, input_ids, scores, **kwargs):
        if input_ids[0, -1].item() in self.stop_ids:
            return True
        return False

class GPT2XLShortAnswers:
    def __init__(self, model_path="./local_gpt2_xl", device=None):
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(model_path)
        self.model.to(self.device)
        self.model.eval()
        self.eos_token_id = self.tokenizer.eos_token_id
        if self.eos_token_id is None:
            self.eos_token_id = 50256
        self.system_prompt = (
            "System: You are a helpful AI assistant. Give short, factual answers. "
            "If uncertain, say 'I don't know'.\n"
        )

    def generate_text(
        self,
        prompt,
        max_new_tokens=40,
        temperature=0.4,
        top_k=50,
        top_p=0.7,
        repetition_penalty=1.1,
        pad_token_id=None,
        stop_on_eos=True
    ):
        if pad_token_id is None:
            pad_token_id = self.eos_token_id

        full_prompt = self.system_prompt + f"User: {prompt}\nAnswer:"

        input_ids = self.tokenizer.encode(full_prompt, return_tensors="pt").to(self.device)
        stopping_criteria = StoppingCriteriaList([])
        if stop_on_eos:
            stopping_criteria.append(StopOnTokens([self.eos_token_id]))

        gen_config = GenerationConfig(
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
            pad_token_id=pad_token_id,
            eos_token_id=self.eos_token_id
        )

        with torch.no_grad():
            output_ids = self.model.generate(
                input_ids,
                generation_config=gen_config,
                stopping_criteria=stopping_criteria
            )

        result = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)

        prefix = "Answer:"
        idx = result.find(prefix)
        if idx != -1:
            raw_reply = result[idx + len(prefix):].strip()
        else:
            raw_reply = result

        first_line = raw_reply.split("\n", 1)[0].strip()
        dot_pos = first_line.find(".")
        if dot_pos != -1:
            short_reply = first_line[: dot_pos + 1]
        else:
            short_reply = first_line

        return short_reply.strip()

    def interactive_chat(self):
        print("Enter 'exit' to quit.")
        while True:
            user_input = input("User: ")
            if user_input.strip().lower() == "exit":
                print("Goodbye.")
                break
            reply = self.generate_text(user_input)
            print("Bot:", reply)

def main():
    bot = GPT2XLShortAnswers("./local_gpt2_xl")
    user_input = "Hello"
    answer = bot.generate_text(user_input)
    print("User:", user_input)
    print("Bot:", answer)
    bot.interactive_chat()

if __name__ == "__main__":
    main()
