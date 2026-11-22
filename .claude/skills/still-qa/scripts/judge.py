#!/usr/bin/env python3
"""Score a still (or a video frame) against its shot prompt with an OPEN-WEIGHTS
vision-language model served behind an OpenAI-compatible endpoint (for example
vLLM, llama.cpp server, Ollama or LM Studio serving Qwen2.5-VL / Qwen3-VL).
Stdlib only. Prints JSON: scores 1-5, verdict, fix.

  python judge.py --endpoint http://127.0.0.1:8000/v1 --model qwen2.5-vl-7b \
      --image shot01.png --prompt "..." [--bible bible.md] [--ref prev_shot.png]
"""
import argparse, base64, json, mimetypes, os, re, urllib.request

RUBRIC = """You are a strict film still reviewer. Score each criterion 1-5:
prompt_match (subject, action, setting, framing as asked), identity (cast and
props match the bible and reference image), anatomy_artifacts (hands, faces,
text, warping; 5 = none), composition (readable, intentional framing),
style (matches the bible's look). Then give verdict "pass" if every score >= 3
and the mean >= 3.5, otherwise "retry", and ONE concrete fix: a prompt edit,
a seed change, or an edit-workflow to apply. Reply with JSON only:
{"scores":{...},"mean":x,"verdict":"pass|retry","issues":[...],"fix":"..."}"""


def img_part(path):
    mt = mimetypes.guess_type(path)[0] or "image/png"
    return {"type": "image_url", "image_url": {"url": f"data:{mt};base64," + base64.b64encode(open(path, "rb").read()).decode()}}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--endpoint", default=os.environ.get("VLM_ENDPOINT", "http://127.0.0.1:8000/v1"))
    p.add_argument("--model", default=os.environ.get("VLM_MODEL", "qwen2.5-vl-7b-instruct"))
    p.add_argument("--image", required=True); p.add_argument("--prompt", required=True)
    p.add_argument("--bible"); p.add_argument("--ref")
    a = p.parse_args()
    text = f"Shot prompt:\n{a.prompt}\n"
    if a.bible:
        text += "\nStory bible excerpt:\n" + open(a.bible).read()[:6000]
    content = [{"type": "text", "text": text}, img_part(a.image)]
    if a.ref:
        content += [{"type": "text", "text": "Reference (previous shot / character sheet):"}, img_part(a.ref)]
    body = {"model": a.model, "temperature": 0, "messages": [{"role": "system", "content": RUBRIC}, {"role": "user", "content": content}]}
    h = {"Content-Type": "application/json"}
    if os.environ.get("VLM_API_KEY"):
        h["Authorization"] = "Bearer " + os.environ["VLM_API_KEY"]
    req = urllib.request.Request(a.endpoint.rstrip("/") + "/chat/completions", json.dumps(body).encode(), h)
    out = json.loads(urllib.request.urlopen(req, timeout=300).read())["choices"][0]["message"]["content"]
    m = re.search(r"\{.*\}", out, re.S)
    try:
        print(json.dumps(json.loads(m.group(0)), indent=1))
    except Exception:
        print(json.dumps({"verdict": "unparsed", "raw": out}))


if __name__ == "__main__":
    main()
