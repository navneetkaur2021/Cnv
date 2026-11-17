# Cnv

## Gemini bridge

`gemini.py` lets Claude (or you) ask Google Gemini questions from the terminal. It has no dependencies; it only needs Python 3.

```bash
python3 gemini.py "Explain recursion in one line"
python3 gemini.py --models                      # list models your key can use
python3 gemini.py -m gemini-2.5-pro "..."       # pick a model
cat file.py | python3 gemini.py -s "Review this code" -
```

### API key
Get a free key at https://aistudio.google.com/apikey, then do one of the following:

- **Claude Code cloud:** open Environment settings, then Network secrets. Set host `generativelanguage.googleapis.com` and header `x-goog-api-key`, and use your key as the value.
- **Local / env var:** `export GEMINI_API_KEY=your_key`

You can set `GEMINI_MODEL` to change the default model (`gemini-2.5-flash`).
