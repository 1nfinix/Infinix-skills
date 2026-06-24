"""
模型验证脚本 — 覆盖六种任务场景
用法: python3 verify-models.py
"""
import os, json, urllib.request, time

env_path = os.path.expanduser("~/.hermes/.env")
keys = {}
with open(env_path) as f:
    for line in f:
        if "=" in line and not line.startswith("#"):
            k, v = line.strip().split("=", 1)
            v = v.strip().strip('"').strip("'")
            if v and len(v) > 8:
                keys[k] = v

DS = keys.get("DEEPSEEK_API_KEY", "")
OR = keys.get("OPENROUTER_API_KEY", "")


def test(model, base, key, msgs, max_tok=500, timeout=30, extra=None):
    body = {"model": model, "messages": msgs, "max_tokens": max_tok}
    if extra:
        body["extra_body"] = extra
    h = {"Authorization": "Bearer " + key, "Content-Type": "application/json"}
    t0 = time.time()
    req = urllib.request.Request(
        base + "/chat/completions",
        data=json.dumps(body).encode(),
        headers=h,
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        r = json.loads(resp.read())
        return {
            "elapsed": f"{time.time() - t0:.1f}s",
            "content": r["choices"][0]["message"]["content"].strip(),
            "usage": r.get("usage", {}),
            "model": r.get("model", "?"),
        }


if __name__ == "__main__":
    results = []

    # 1: Light QA
    r = test("deepseek-v4-pro", "https://api.deepseek.com", DS,
        [{"role": "user", "content": "用中文回复：早安"}], max_tok=200)
    ok1 = len(r["content"]) > 0
    print(f"1. light QA [{r['elapsed']}] {r['content'][:80]}")
    results.append(("轻量问答", "v4-pro", ok1))

    # 2: Structured JSON
    r = test("deepseek-v4-pro", "https://api.deepseek.com", DS,
        [{"role": "user", "content": '输出纯JSON: {"status":"ok","count":3} 不要其他文字'}], max_tok=150)
    ok2 = "status" in r["content"] and "count" in r["content"]
    print(f"2. structured [{r['elapsed']}] json_valid={ok2}")
    results.append(("结构化JSON", "v4-pro", ok2))

    # 3: Long text summary
    txt = "一所有模型100%正常。二MiMo切换到Bearer认证。三nex-n2-pro已付费不可用。四v2-omni将于6月30日下线。五TTS用chat/completions端点。六FAL FLUX/v2返回404需用flux/dev。七Agnes免费层延迟约11秒。八fallback配置nemotron加v4-flash两层降级。"
    r = test("deepseek-v4-flash", "https://api.deepseek.com", DS,
        [{"role": "user", "content": "用三行总结，保留所有数字：\n" + txt}], max_tok=300,
        extra={"thinking": {"type": "disabled"}})
    ok3 = len(r["content"]) > 50
    print(f"3. summary [{r['elapsed']}] len={len(r['content'])}")
    results.append(("长文本摘要", "v4-flash", ok3))

    # 4: Config debugging
    r = test("deepseek-v4-pro", "https://api.deepseek.com", DS,
        [{"role": "user", "content": "API返回401 Invalid API Key。列出3个可能原因，不要给命令"}], max_tok=200)
    ok4 = "密钥" in r["content"] or "Key" in r["content"] or "key" in r["content"]
    print(f"4. debug [{r['elapsed']}] {r['content'][:80]}")
    results.append(("配置排障", "v4-pro", ok4))

    # 5: Creative writing
    r = test("deepseek-v4-pro", "https://api.deepseek.com", DS,
        [{"role": "user", "content": "用文艺风写一句话介绍科技早报，20字以内"}], max_tok=200)
    ok5 = 5 < len(r["content"]) < 80
    print(f"5. creative [{r['elapsed']}] ({len(r['content'])}字) {r['content'][:80]}")
    results.append(("创作任务", "v4-pro", ok5))

    # 6: Fallback
    r = test("nvidia/nemotron-3-super-120b-a12b:free", "https://openrouter.ai/api/v1", OR,
        [{"role": "user", "content": "say hi"}], max_tok=50)
    ok6 = len(r["content"]) > 0
    print(f"6. fallback [{r['elapsed']}] {r['content'][:60]}")
    results.append(("Fallback", "nemotron-120b", ok6))

    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    for name, model, ok in results:
        icon = "✅" if ok else "❌"
        print(f"  {icon} {name:12s} | {model:18s}")
    passed = sum(1 for _, _, ok in results if ok)
    print(f"\n  {passed}/{len(results)} passed")
