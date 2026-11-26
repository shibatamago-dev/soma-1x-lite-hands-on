"""Run Amini Soma-1X Lite on a document image (Transformers version).

Usage:
    python run_soma_1x_lite.py --image document.png --output output.txt

Notes:
- Model ID verified character by character: "AminiTech/Soma-1X-lite".
- The README quickstart's generate(enable_thinking=False) does NOT run on
  transformers 5.24.1 (ValueError: unused model kwargs), so enable_thinking
  is intentionally NOT passed here.
- Requires a GPU with ~6 GB free VRAM (2B BF16 weights are 4.43 GB;
  verified on a free Colab T4, 15,360 MiB).
"""

import argparse

import torch
from huggingface_hub import hf_hub_download
from PIL import Image
from transformers import AutoProcessor, Qwen3_5ForConditionalGeneration

MODEL_ID = "AminiTech/Soma-1X-lite"


def read_prompt(name: str) -> str:
    with open(hf_hub_download(MODEL_ID, name), encoding="utf-8") as f:
        return f.read()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True, help="Path to a document image")
    parser.add_argument("--output", default="output.txt", help="Where to write the output")
    args = parser.parse_args()

    model = Qwen3_5ForConditionalGeneration.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        device_map="auto",
    ).eval()
    processor = AutoProcessor.from_pretrained(MODEL_ID)

    system_prompt = read_prompt("system_prompt.txt")
    user_prompt = read_prompt("user_prompt.txt")

    image = Image.open(args.image).convert("RGB")
    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": user_prompt},
            ],
        },
    ]
    inputs = processor.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_dict=True,
        return_tensors="pt",
    ).to(model.device)

    with torch.inference_mode():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=16384,
            do_sample=False,
        )
    generated_ids = output_ids[:, inputs.input_ids.shape[1]:]
    output = processor.batch_decode(
        generated_ids,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )[0]

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(output)
    print(output)


if __name__ == "__main__":
    main()
