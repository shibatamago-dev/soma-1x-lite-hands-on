# soma-1x-lite-hands-on

Amini Soma-1X Lite (`AminiTech/Soma-1X-lite`) を Google Colab 無料 T4 で動かし、日本語の領収書・表＋数式・古文書風画像の構造化精度を確かめた再現リポジトリです。

## 検証結果（2026-11-26、Colab 無料 T4）

- プローブ（日本語の短いテキスト）：4/4 一致
- Q1 日本語の領収書：テキスト 14/14、金額は全て桁まで一致、表は HTML の `<table>`（8行）
- Q2 表＋数式：表セル 12/12、表は HTML、数式は LaTeX（二次方程式の解の公式と E=mc²）
- Q3 古文書風の縦書き（合成画像）：8列全一致、ユニーク文字 recall 33/33、右→左の読む順序も正しい
- Q3 補足・実スキャン（源氏物語絵巻、パブリックドメイン）：`[EMPTY PAGE]`、幻覚なし
- 重み 4.43GB、ロード 103.6秒、VRAM 約 4.43GB（T4 15,360MiB）

詳細は [RESULTS.md](RESULTS.md) を参照してください。

## 使い方

```bash
pip install -U torch torchvision transformers accelerate pillow pymupdf huggingface_hub
python run_soma_1x_lite.py --image document.png --output output.txt
```

モデルは `AminiTech/Soma-1X-lite`（2B、Qwen3.5ベース、Apache 2.0）です。

## 注意点

- README のクイックスタートにある `generate(enable_thinking=False)` は transformers 5.24.1 では動きません（`ValueError: unused model kwargs`）。このスクリプトでは `enable_thinking` を渡していません。
- olmOCR-Bench 84.7 / OmniParse-Bench 84.37 は自社計測で、この小規模プローブでは確認も反証もできません。
- Q3 の採点対象は合成画像です。実スキャンでの文字認識精度は採点できる形では試していません。
- GGUF 版は未確認です。今回は Transformers 版のみです。

## リンク

- モデルカード：https://huggingface.co/AminiTech/Soma-1X-lite
- Colab ノートブック：https://colab.research.google.com/drive/12jD2qGdL9L-khj2oogBj6E_iL-I9E3rD
- Zenn 記事：公開後にリンクを追加します（公開枠は調整中、11/27 候補）

## License

MIT
