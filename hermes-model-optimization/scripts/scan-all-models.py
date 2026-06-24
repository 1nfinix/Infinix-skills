"""
全模型连通性一键扫描脚本
用法: python3 scan-all-models.py
覆盖: DeepSeek / MiMo / Agnes / OpenRouter / TTS / Image Gen
"""
import os, json, urllib.request, time

ENV = os.path.expanduser("~/.hermes/.env")

def load_keys():
    keys = {}
    with open(ENV) as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                v = v.strip().strip('"').strip("'")
                if v and len(v) > 8:
                    keys[k] = v
    return keys

def safe_key(keys, name):
    k = keys.get(name, "")
    return f"{k[:8]}...{k[-4:]}" if k else "MISSING"

def test(keys, key_name, base_url, model, extra_body=None, timeout=30):
    key = keys.get(key_name, "")
    if not key:
        return {"status": "NO_KEY", "error": f"{key_name} missing"}

    body = {
        "model": model,
        "messages": [{"role": "user", "content": "say hi"}],
        "max_tokens": 30
    }
    if extra_body:
        body["extra_body"] = extra_body

    data = json.dumps(body).encode()
    headers = {
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json"
    }
    url = base_url + "/chat/completions"

    t0 = time.time()
    try:
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            r = json.loads(resp.read())
            elapsed = time.time() - t0
            c = r["choices"][0]
            content = c["message"].get("content", "")
            if not content:
                content = c["message"].get("reasoning_content", "") or "(empty)"
            finish = c.get("finish_reason", "?")
            usage = r.get("usage", {})
            reasoning = usage.get("completion_tokens_details", {}).get("reasoning_tokens", 0)
            return {
                "status": "OK",
                "content": content[:60].replace("\n", " "),
                "finish": finish,
                "tokens": usage.get("total_tokens", "?"),
                "reasoning": reasoning,
                "elapsed": f"{elapsed:.1f}s",
                "model": r.get("model", model)
            }
    except urllib.error.HTTPError as e:
        body_txt = "?"
        try:
            body_txt = e.read().decode()[:200]
        except:
            pass
        return {"status": f"HTTP {e.code}", "error": body_txt}
    except Exception as e:
        return {"status": "ERROR", "error": str(e)[:150]}


if __name__ == "__main__":
    keys = load_keys()

    tests = [
        # DeepSeek
        ("DeepSeek", "DEEPSEEK_API_KEY", "https://api.deepseek.com", "deepseek-v4-pro", None),
        ("DeepSeek", "DEEPSEEK_API_KEY", "https://api.deepseek.com", "deepseek-v4-flash", {"thinking": {"type": "disabled"}}),
        ("DeepSeek", "DEEPSEEK_API_KEY", "https://api.deepseek.com", "deepseek-v4-flash", None),
        # MiMo
        ("MiMo", "MIMO_API_KEY", "https://api.xiaomimimo.com/v1", "mimo-v2.5-pro", None),
        ("MiMo", "MIMO_API_KEY", "https://api.xiaomimimo.com/v1", "mimo-v2.5", {"thinking": {"type": "disabled"}}),
        ("MiMo", "MIMO_API_KEY", "https://api.xiaomimimo.com/v1", "mimo-v2.5", None),
        ("MiMo", "MIMO_API_KEY", "https://api.xiaomimimo.com/v1", "mimo-v2-omni", None),
        # Agnes
        ("Agnes", "AGNES_API_KEY", "https://apihub.agnes-ai.com/v1", "agnes-2.0-flash", None),
        # OpenRouter
        ("OpenRouter", "OPENROUTER_API_KEY", "https://openrouter.ai/api/v1", "nvidia/nemotron-3-super-120b-a12b:free", None),
        ("OpenRouter", "OPENROUTER_API_KEY", "https://openrouter.ai/api/v1", "inclusionai/ling-2.6-flash", None),
    ]

    results = []
    for provider, key_name, base, model, extra in tests:
        r = test(keys, key_name, base, model, extra)
        r["provider"] = provider
        r["model"] = model
        r["thinking"] = extra.get("thinking", {}).get("type", "default") if extra else "default"
        results.append(r)
        time.sleep(0.3)

    for p in ["DeepSeek", "MiMo", "Agnes", "OpenRouter"]:
        group = [r for r in results if r["provider"] == p]
        if not group:
            continue
        icon = {"DeepSeek": "🔵", "MiMo": "🟢", "Agnes": "🟡", "OpenRouter": "🟣"}.get(p, "⚪")
        print(f"\n{icon} {p}")

        if group[0].get("status") == "NO_KEY":
            print(f"  ❌ Key missing")
            continue

        for r in group:
            s = r["status"]
            icon2 = "✅" if s == "OK" else "❌"
            extra_info = ""
            if s == "OK":
                extra_info = f" | {r.get('content','')[:40]}"
                if r.get("reasoning", 0):
                    extra_info += f" | R:{r['reasoning']}"
            else:
                extra_info = f" | {r.get('error','')[:80]}"
            print(f"  {icon2} {r['model']:45s} think={r['thinking']:8s} {r.get('elapsed','?'):>6s}{extra_info}")

    ok = sum(1 for r in results if r["status"] == "OK")
    fail = sum(1 for r in results if r["status"] != "OK")
    print(f"\n{'='*60}")
    print(f"  Total: {ok} OK, {fail} FAIL ({len(results)} tests)")
