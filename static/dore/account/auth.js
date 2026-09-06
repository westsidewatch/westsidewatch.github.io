/* DORÉ Auth adapter — Supabase configuration is injected at runtime. */
(function () {
  const config = window.DORE_AUTH_CONFIG || {};
  const status = document.getElementById('status');
  const form = document.getElementById('email-form');
  const email = document.getElementById('email');
  const providers = [...document.querySelectorAll('[data-provider]')];

  const providerMap = { google: 'google', apple: 'apple', microsoft: 'azure', github: 'github' };

  function message(text) {
    if (status) status.textContent = text;
  }

  async function loadClient() {
    if (!config.url || !config.publishableKey) return null;
    if (!window.supabase) {
      await new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2';
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
      });
    }
    return window.supabase.createClient(config.url, config.publishableKey);
  }

  async function signIn(provider) {
    try {
      const client = await loadClient();
      if (!client) {
        message('身份服務尚未配置。');
        return;
      }
      const { error } = await client.auth.signInWithOAuth({
        provider,
        options: { redirectTo: window.location.origin + '/dore/account/' }
      });
      if (error) message(error.message);
    } catch (error) {
      message('身份服務載入失敗，請稍後再試。');
    }
  }

  providers.forEach((button) => {
    button.removeAttribute('aria-disabled');
    button.addEventListener('click', () => signIn(providerMap[button.dataset.provider]));
  });

  if (form) {
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      if (!email || !email.checkValidity()) {
        email?.reportValidity();
        return;
      }
      try {
        const client = await loadClient();
        if (!client) {
          message('身份服務尚未配置。');
          return;
        }
        const { error } = await client.auth.signInWithOtp({
          email: email.value.trim(),
          options: { emailRedirectTo: window.location.origin + '/dore/account/' }
        });
        message(error ? error.message : '驗證連結已發送，請檢查你的電子郵箱。');
      } catch (error) {
        message('身份服務載入失敗，請稍後再試。');
      }
    });
  }
})();
