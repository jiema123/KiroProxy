"""Login page for KiroProxy Web UI."""


def get_login_page() -> str:
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>KiroProxy Login</title>
  <link rel="icon" type="image/svg+xml" href="/assets/icon.svg">
  <style>
    :root {
      color-scheme: light dark;
      --bg: #f4f1ea;
      --panel: rgba(255,255,255,0.86);
      --text: #1a1816;
      --muted: #6a625b;
      --border: rgba(54, 43, 32, 0.12);
      --accent: #ef4444;
      --accent-strong: #d92d20;
      --accent-soft: #f97373;
      --error: #b42318;
      --shadow: 0 18px 60px rgba(31, 29, 26, 0.12);
    }
    @media (prefers-color-scheme: dark) {
      :root {
        --bg: #111513;
        --panel: rgba(19, 24, 22, 0.92);
        --text: #f4efe8;
        --muted: #b1a89e;
        --border: rgba(219, 209, 198, 0.12);
        --accent: #ef4444;
        --accent-strong: #fb7185;
        --accent-soft: #fca5a5;
        --error: #ff8a80;
        --shadow: 0 18px 60px rgba(0, 0, 0, 0.35);
      }
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      font-family: "Avenir Next", "PingFang SC", "Segoe UI", sans-serif;
      color: var(--text);
      background:
        radial-gradient(circle at top left, rgba(239,68,68,0.16), transparent 32%),
        radial-gradient(circle at bottom right, rgba(251,113,133,0.18), transparent 28%),
        linear-gradient(135deg, var(--bg), #ece6dc 100%);
      display: grid;
      place-items: center;
      padding: 24px;
    }
    @media (prefers-color-scheme: dark) {
      body {
        background:
          radial-gradient(circle at top left, rgba(239,68,68,0.18), transparent 28%),
          radial-gradient(circle at bottom right, rgba(251,113,133,0.14), transparent 22%),
          linear-gradient(135deg, var(--bg), #1a201d 100%);
      }
    }
    .shell {
      width: min(960px, 100%);
      display: grid;
      grid-template-columns: 1.1fr 0.9fr;
      border: 1px solid var(--border);
      border-radius: 24px;
      overflow: hidden;
      background: var(--panel);
      box-shadow: var(--shadow);
      backdrop-filter: blur(18px);
    }
    .hero {
      padding: 48px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      border-right: 1px solid var(--border);
      background:
        linear-gradient(180deg, rgba(255,255,255,0.12), transparent),
        linear-gradient(135deg, rgba(239,68,68,0.14), transparent 58%);
    }
    .brand {
      display: inline-flex;
      align-items: center;
      gap: 16px;
      margin-top: 20px;
    }
    .brand img {
      width: 54px;
      height: 64px;
      filter: drop-shadow(0 12px 24px rgba(217,45,32,0.18));
    }
    .brand-copy {
      display: grid;
      gap: 4px;
    }
    .brand-name {
      font-size: 0.92rem;
      font-weight: 700;
      letter-spacing: 0.01em;
    }
    .brand-tag {
      font-size: 0.82rem;
      color: var(--muted);
    }
    .hero h1 {
      margin: 18px 0 12px;
      font-size: clamp(2rem, 3.6vw, 3.4rem);
      line-height: 1.02;
      letter-spacing: -0.04em;
    }
    .hero p {
      margin: 0;
      max-width: 28rem;
      color: var(--muted);
      line-height: 1.7;
      font-size: 0.98rem;
    }
    .badge {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      padding: 10px 14px;
      border-radius: 999px;
      border: 1px solid var(--border);
      font-size: 0.82rem;
      color: var(--muted);
      width: fit-content;
    }
    .dot {
      width: 9px;
      height: 9px;
      border-radius: 50%;
      background: linear-gradient(135deg, var(--accent), #d3a96a);
      box-shadow: 0 0 0 6px rgba(31, 111, 95, 0.08);
    }
    .panel {
      padding: 40px 34px;
      display: flex;
      align-items: center;
    }
    .card {
      width: 100%;
    }
    .eyebrow {
      font-size: 0.78rem;
      letter-spacing: 0.16em;
      text-transform: uppercase;
      color: var(--muted);
      margin-bottom: 12px;
    }
    .card h2 {
      margin: 0 0 10px;
      font-size: 1.6rem;
      letter-spacing: -0.03em;
    }
    .card p {
      margin: 0 0 24px;
      color: var(--muted);
      line-height: 1.6;
    }
    form {
      display: grid;
      gap: 14px;
    }
    label {
      display: grid;
      gap: 8px;
      font-size: 0.9rem;
      color: var(--muted);
    }
    input {
      border: 1px solid var(--border);
      border-radius: 14px;
      background: rgba(255,255,255,0.72);
      color: var(--text);
      padding: 14px 16px;
      font: inherit;
      outline: none;
      transition: border-color .2s ease, transform .2s ease;
    }
    @media (prefers-color-scheme: dark) {
      input {
        background: rgba(255,255,255,0.04);
      }
    }
    input:focus {
      border-color: var(--accent);
      transform: translateY(-1px);
      box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.12);
    }
    button {
      margin-top: 10px;
      border: 0;
      border-radius: 14px;
      background: linear-gradient(135deg, var(--accent), var(--accent-soft));
      color: white;
      font: inherit;
      font-weight: 600;
      padding: 14px 18px;
      cursor: pointer;
      transition: transform .2s ease, opacity .2s ease, box-shadow .2s ease;
      box-shadow: 0 14px 28px rgba(217, 45, 32, 0.24);
    }
    button:hover {
      transform: translateY(-1px);
      opacity: 0.96;
      box-shadow: 0 18px 34px rgba(217, 45, 32, 0.28);
    }
    button:disabled {
      opacity: 0.6;
      cursor: wait;
      transform: none;
    }
    .hint {
      margin-top: 16px;
      font-size: 0.84rem;
      color: var(--muted);
    }
    .error {
      min-height: 20px;
      color: var(--error);
      font-size: 0.88rem;
      margin-top: 10px;
    }
    .creds {
      margin-top: 22px;
      padding: 14px 16px;
      border-radius: 14px;
      border: 1px dashed var(--border);
      color: var(--muted);
      font-size: 0.84rem;
      line-height: 1.6;
    }
    @media (max-width: 840px) {
      .shell {
        grid-template-columns: 1fr;
      }
      .hero {
        border-right: 0;
        border-bottom: 1px solid var(--border);
        padding: 32px;
      }
      .panel {
        padding: 28px 22px 30px;
      }
    }
  </style>
</head>
<body>
  <div class="shell">
    <section class="hero">
      <div>
        <div class="badge"><span class="dot"></span>KiroProxy Admin Access</div>
        <div class="brand">
          <img src="/assets/icon.svg" alt="KiroProxy logo">
          <div class="brand-copy">
            <div class="brand-name">KiroProxy</div>
            <div class="brand-tag">Route Kiro. Guard Access.</div>
          </div>
        </div>
        <h1>Kiro API Proxy<br>管理入口</h1>
        <p>这个页面用于保护启动后的管理面板。代理接口保持可用，只有 Web 管理界面和管理 API 需要先登录。</p>
      </div>
      <p>登录后可进行账号管理、流量查看、登录授权、日志检查与设置调整。</p>
    </section>
    <section class="panel">
      <div class="card">
        <div class="eyebrow">Secure Login</div>
        <h2>KiroProxy Login</h2>
        <p>请输入默认管理员账号，登录成功后会自动跳转到控制台。</p>
        <form id="loginForm">
          <label>用户名
            <input id="username" name="username" type="text" value="admin" autocomplete="username" required>
          </label>
          <label>密码
            <input id="password" name="password" type="password" value="kiroproxy" autocomplete="current-password" required>
          </label>
          <button id="submitBtn" type="submit">登录</button>
        </form>
        <div id="errorMsg" class="error"></div>
        <div class="creds">默认账号：<strong>admin</strong><br>默认密码：<strong>kiroproxy</strong></div>
        <div class="hint">如需修改默认账号密码，可设置环境变量 `KIROPROXY_ADMIN_USERNAME` 和 `KIROPROXY_ADMIN_PASSWORD`。</div>
      </div>
    </section>
  </div>
  <script>
    const form = document.getElementById('loginForm');
    const errorMsg = document.getElementById('errorMsg');
    const submitBtn = document.getElementById('submitBtn');

    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      errorMsg.textContent = '';
      submitBtn.disabled = true;

      const payload = {
        username: document.getElementById('username').value.trim(),
        password: document.getElementById('password').value
      };

      try {
        const response = await fetch('/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        if (!response.ok) {
          const data = await response.json().catch(() => ({}));
          errorMsg.textContent = data.detail || '登录失败';
          return;
        }

        window.location.href = '/';
      } catch (error) {
        errorMsg.textContent = '请求失败: ' + error.message;
      } finally {
        submitBtn.disabled = false;
      }
    });
  </script>
</body>
</html>"""
