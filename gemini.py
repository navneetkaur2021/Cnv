#!/usr/bin/env python3
"""Minimal Gemini bridge (no dependencies).

Usage:
  python3 gemini.py "your question"          # ask Gemini
  echo "long prompt" | python3 gemini.py -   # prompt from stdin
  python3 gemini.py --models                 # list available models
  python3 gemini.py -m gemini-2.5-pro "..."  # choose a model

Auth: GEMINI_API_KEY env var. In a Claude Code cloud session the network
proxy injects the key, so a placeholder value is fine there.
"""
import argparse, json, os, sys, urllib.request, urllib.error

BASE = "https://generativelanguage.googleapis.com/v1beta"
DEFAULT_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")


def call(method, path, body=None):
    key = os.environ.get("GEMINI_API_KEY", "proxy-injected")
    req = urllib.request.Request(
        f"{BASE}/{path}",
        data=json.dumps(body).encode() if body is not None else None,
        method=method,
        headers={"Content-Type": "application/json", "x-goog-api-key": key},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"Gemini API error {e.code}: {e.read().decode(errors='replace')}")


def ask(prompt, model, system=None):
    body = {"contents": [{"role": "user", "parts": [{"text": prompt}]}]}
    if system:
        body["systemInstruction"] = {"parts": [{"text": system}]}
    data = call("POST", f"models/{model}:generateContent", body)
    cands = data.get("candidates") or []
    if not cands:
        sys.exit(f"No answer: {json.dumps(data.get('promptFeedback', data))}")
    return "".join(p.get("text", "") for p in cands[0].get("content", {}).get("parts", []))


def main():
    ap = argparse.ArgumentParser(description="Ask Google Gemini")
    ap.add_argument("prompt", nargs="?", help="prompt text, or - for stdin")
    ap.add_argument("-m", "--model", default=DEFAULT_MODEL)
    ap.add_argument("-s", "--system", help="system instruction")
    ap.add_argument("--models", action="store_true", help="list models")
    a = ap.parse_args()
    if a.models:
        for m in call("GET", "models?pageSize=200").get("models", []):
            if "generateContent" in m.get("supportedGenerationMethods", []):
                print(m["name"].removeprefix("models/"))
        return
    if not a.prompt:
        ap.error("prompt required")
    prompt = sys.stdin.read() if a.prompt == "-" else a.prompt
    print(ask(prompt, a.model, a.system))


if __name__ == "__main__":
    main()
