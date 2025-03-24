# **AI Basic**

This project implements a chatbot powered by a fine-tuned GPT-2 model. The chatbot is designed to generate short, factual, and contextually relevant responses. It uses a Flask backend to handle user requests and serves an interactive web-based interface for seamless communication. The GPT-2 model is locally hosted, ensuring flexibility and control over its behavior and performance.

---

## **Features**
- GPT-2 model for generating concise, factual responses.
- Flask backend for handling requests and serving responses.
- Interactive web-based chat interface with dynamic message handling.

---

## **Installation**

### **Clone the repository:**
```bash
git clone https://github.com/levzu/AI-Basic
cd AI-Basic
```

### **Create a virtual environment:**
```bash
python -m venv ai
source ai/bin/activate   # Linux/MacOS
ai\Scripts\activate      # Windows
```

### **Install dependencies:**
```bash
pip install -r requirements.txt
```

### **Install GPT-2 model:**
```bash
python install_gpt2xl.py
```

---

## **Usage**

### **Start the Flask server:**
```bash
python app.py
```

### **Open the web interface:**
Go to: (in your browser)
```bash
http://127.0.0.1:5000
```

---

### **License**
This project is licensed under the MIT License.

---
### 1. Overall Purpose and Architecture

This project centers on creating a short-answer AI using a local GPT-2 XL model. The primary goal is to produce concise and factual responses rather than long, open-ended text. This design is particularly useful for situations where users require quick, direct answers—like a chatbot that delivers precise information, or a Q&A tool for frequently asked questions.

    Core Idea: We load and run the GPT-2 XL model locally. GPT-2 XL is a variant of GPT-2 with more parameters, allowing for richer language understanding.

    Key Class: The GPT2XLShortAnswers class manages all essential AI logic—tokenization, model inference, and short-answer generation.

    Custom Stopping Logic: Instead of relying on default “end-of-sequence” checks, we introduce a specialized mechanism (StopOnTokens) that ensures we can terminate generation as soon as an end-of-sequence (or other defined) token appears.

In other words, this code not only loads a powerful language model but also constrains its output to deliver short, direct answers, which is often more user-friendly for question-and-answer scenarios.
### 2. GPT2XLShortAnswers Class

Within the code, you’ll see a class named GPT2XLShortAnswers. It is the heart of the project, and here’s a conceptual breakdown of its responsibilities:

    Model Loading: The class loads the tokenizer (which turns text into numerical tokens) and the GPT-2 XL model itself. It also identifies which device (CPU or GPU) to use, automatically falling back to CPU if no GPU is available.

    System Prompt: We define a preset “system message” that instructs the model to give short, factual answers and respond with “I don’t know” when uncertain. This helps guide the AI’s behavior, so it tries to remain concise and limit speculation.

    Core Generation Method: The generate_text method handles all the logic for transforming a user prompt into a short, one-sentence response. It merges the system prompt with the user’s question, tokenizes this combined string, and passes the tokens to the GPT-2 XL model under specific parameters (e.g., temperature, top_k, repetition_penalty).

    Output Post-Processing: After the model generates text, the class extracts just the first sentence or so, discarding any extra lines. This ensures we get an answer that is short and direct.

By encapsulating all these details into a single class, the code remains well-organized. Developers can easily reuse or adapt it for similar short-response AI applications.
### 3. Short-Answer Logic and Stopping Criteria

One of the notable features here is the StopOnTokens mechanism. Since the code aims for answers that end promptly, we need custom stopping rules:

    StopOnTokens Class: This small piece of logic identifies when the AI has generated a token matching a “stop ID” (often the end-of-sequence token). As soon as that token is detected, the generation process terminates.

    Why Use StopOnTokens? GPT-2 XL can potentially generate very long responses if left unchecked. By explicitly telling the model to stop, we keep the outputs concise and factual, aligned with the primary goal of short answers.

In practical terms, this means that once the AI has reached a natural stopping point—like a period or the model’s built-in “end-of-sequence” token—it won’t continue rambling. This ensures cleaner, more efficient outputs.
### 4. Interactive Chat vs. Direct Generation

Finally, the code also features an interactive chat function, though the fundamental short-answer logic remains the same:

    Direct Generation: In many cases, you might want to call generate_text(...) for a single user prompt, using the AI as a “question-in, answer-out” system.

    Interactive Chat: The code includes a loop that repeatedly asks for user input and prints the model’s short response. This can be helpful for real-time demonstrations, testing the AI’s ability to handle varied prompts, or simple Q&A sessions.

Whether you incorporate the interactive mode or not, the same GPT2XLShortAnswers class and short-response strategy underlie both approaches. This design separates how text is generated (the “engine”) from how the conversation is handled (the “interface”), letting you tailor the user experience without altering the AI’s core logic.

### **Contributing**
1. Fork the repository.
2. Create a new branch for your feature or fix:
```bash
git checkout -b my-feature-branch
```
