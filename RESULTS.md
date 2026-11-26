# Results — Amini Soma-1X Lite hands-on (2026-11-26)

Model: `AminiTech/Soma-1X-lite` (2,213,241,664 params, BF16, Qwen3.5-based, Apache 2.0)
Environment: Google Colab free T4 (Tesla T4, 15,360 MiB), transformers 5.24.1, torch 2.15.0+cu132
Notebook: https://colab.research.google.com/drive/12jD2qGdL9L-khj2oogBj6E_iL-I9E3rD
Drive folder: `soma-1x-lite-hands-on/` (results saved there as they came out)

## Setup

- T4 obtained on attempt 2 (attempt 1: "too many active sessions" + reCAPTCHA).
- Weight size checked first: model.safetensors 4.43 GB. VRAM before load: 0 MiB used, 15.527 GB free.
- Load time: 103.6 s (download 99.4 MB/s, 617/617 weights in 13 s).
- VRAM after load: allocated 4.427 GB, reserved 4.429 GB, free 11.081 GB; during inference allocated 4.436 GB.
- system_prompt.txt (4,895 chars) and user_prompt.txt ("Parse the page into layout blocks with their text.") read from the repo.

## Probe (24.6 s): 4/4

Known text: 領収書 / 株式会社たまご / 金額 1,200円. All 4 strings found.

```
<block label="heading" box="64 146 329 364">領収書</block>
<block label="text" box="64 464 450 594">株式会社たまご</block>
<block label="text" box="64 695 379 856">金額 1,200円</block>
```

## Q1 receipt (88.1 s): text 14/14, amounts digit-exact

たまご商店, 2026-11-20, No. 001234; たまご 300円, 牛乳 250円, 食パン 200円, りんご 250円; 小計 1,000円, 消費税 100円, 合計 1,100円.
Table as HTML: YES — `<table><tr><th>品目</th><th>金額</th></tr>` with all 8 rows. Reading order correct.

## Q2 table + equations (88.6 s): table cells 12/12

月別売上：9月 120,000円 120個, 10月 135,000円 135個, 11月 150,000円 150個. Table as HTML: YES.
Equations as LaTeX: YES.

```
<block label="equation">\[ x = (-b \pm \sqrt{b^2 - 4ac}) / 2a \]</block>
<block label="equation">\[ E = mc^2 \]</block>
```

## Q3 old document, synthetic (84.5 s): columns 8/8, unique chars 33/33

Synthetic aged-paper vertical-text image (explicitly synthetic, not a real scan). Right-to-left reading order correct (box x decreasing 849→216). No missing chars.

## Q3 supplementary, real scan (69.0 s): N/A, no hallucination

File:Genji emaki Yadorigi.JPG from Wikimedia Commons (12th-century Genji monogatari emaki, Tokugawa Art Museum, public domain, 2,000×884). Output exactly `[EMPTY PAGE]` (0 blocks). The section is painting-dominant with no legible text visible, so scoring is N/A.

## Deviations

1. README quickstart `generate(enable_thinking=False)` does NOT run on transformers 5.24.1 (`ValueError: unused model kwargs`; shipped generation_config has no enable_thinking field). All generations used max_new_tokens=16384, do_sample=False, enable_thinking NOT passed.
2. `pip -U torch` upgraded torch to CUDA 13.2 while torchaudio stayed at 13.0, breaking transformers import; fixed with torchaudio 2.11.1+cu132.
3. apt Noto CJK fonts are .ttc collections; test images were generated with NotoSansCJKjp-Regular.otf / NotoSerifCJKjp-Regular.otf downloaded from noto-cjk.
4. Two kernel/session crashes and one backend disconnect; no results lost (each saved to Drive immediately).

## Not verified

- olmOCR-Bench / OmniParse-Bench reproduction (small-scale probes only; cannot confirm or refute vendor scores 84.7 / 84.37).
- GGUF version (`Soma-1X-lite-GGUF`).
- Real historical-scan character accuracy in a scored form (Q3 scored run is synthetic).
