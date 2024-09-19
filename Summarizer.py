from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("Meta-Llama-3-8B")
model = AutoModelForCausalLM.from_pretrained("Meta-Llama-3-8B").to('cuda' if torch.cuda.is_available() else 'cpu')

# Add padding token if not present
if tokenizer.pad_token is None:
    tokenizer.add_special_tokens({'pad_token': tokenizer.eos_token})

def generate_summary(text, max_length=150):
    # Tokenize the input text
    inputs = tokenizer(
        text,
        return_tensors='pt',
        padding=True,
        truncation=True,
        max_length=max_length
    ).to('cuda' if torch.cuda.is_available() else 'cpu')

    # Generate summary
    try:
        summary_ids = model.generate(
            inputs['input_ids'],
            attention_mask=inputs['attention_mask'],
            max_length=max_length,
            num_beams=4,
            length_penalty=2.0,
            early_stopping=True,
            pad_token_id=tokenizer.pad_token_id,
            temperature=0.7,  # Randomness
            top_k=50,         # Top-k sampling
            top_p=0.95        # Nucleus sampling
        )
        
        # Decode the summary
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary
    
    except Exception as e:
        print(f"Error during generation: {e}")
        return None

