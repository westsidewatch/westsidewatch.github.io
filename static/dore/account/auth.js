/* DORÉ Auth adapter — Supabase configuration is injected at runtime. */
(function () {
  const config = window.DORE_AUTH_CONFIG || {};
  const status = document.getElementById('status');
  const form = document.getElementById('email-form');
  const email = document.getElementById('email');
  const providers = [...document.querySelectorAll('[data-provider]')];
  const sessionPanel = document.getElementById('session-panel');
  const sessionEmail = document.getElementById('session-email');
  const logout = document.getElementById('logout');

  const providerMap = {
    google: 'google',
    apple: 'apple',
    microsoft: 'azure',
    github: 'github'
  };

  const SUPABASE_JS_URL = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.116.0';
  const ACCOUNT_URL = window.location.origin + '/dore/account/';
  let client = null;

  function message(text) {
    if (status) status.textContent = text;
  }

  function setAuthenticated(user) {
    const signedIn = Boolean(user);
    if (sessionPanel) sessionPanel.hidden = !signedIn;
    if (sessionEmail) sessionEmail.textContent = signedIn ? (user.email || '已登入') : '';
    providers.forEach((button) => { button.hidden = signedIn; });
    if (form) form.hidden = signedIn;
  }

  function showAuthErrorFromRedirect() {
    const hash = window.location.hash.startsWith('#') ? window.location.hash.slice(1) : '';
    if (!hash) return false;
    const params = new URLSearchParams(hash);
    const error = params.get('error_description') || params.get('error');
    if (!error) return false;
    message('登入未完成：' + error.replace(/\+/g, ' '));
    window.history.replaceState({}, document.title, window.location.pathname + window.location.search);
    return true;
  }

  async function loadClient() {
    if (!config.url || !config.publishableKey) return null;
    if (!window.supabase) {
      await new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = SUPABASE_JS_URL;
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
      });
    }
    if (!client) client = window.supabase.createClient(config.url, config.publishableKey);
    return client;
  }

  async function refreshSession() {
    const auth = await loadClient();
    if (!auth) {
      setAuthenticated(null);
      message('身份服務尚未配置；完成 Supabase 公開設定與登入提供者設定後，登入按鈕即可啟用。');
      return;
    }
    const { data, error } = await auth.auth.getSession();
    if (error) {
      setAuthenticated(null);
      message(error.message);
      return;
    }
    setAuthenticated(data.session?.user || null);
    if (data.session?.user) message('已登入 DORÉ。');
  }

  async function signIn(provider) {
    try {
      const auth = await loadClient();
      if (!auth) {
        message('身份服務尚未配置。');
        return;
      }
      message('正在前往登入服務……');
      const { error } = await auth.auth.signInWithOAuth({
        provider,
        options: { redirectTo: ACCOUNT_URL }
      });
      if (error) message(error.message);
    } catch (error) {
      message('身份服務載入失敗，請稍後再試。');
    }
  }

  providers.forEach((button) => {
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
        const auth = await loadClient();
        if (!auth) {
          message('身份服務尚未配置。');
          return;
        }
        const { error } = await auth.auth.signInWithOtp({
          email: email.value.trim(),
          options: {
            emailRedirectTo: ACCOUNT_URL,
            shouldCreateUser: true
          }
        });
        message(error ? error.message : '驗證連結已發送，請檢查你的電子郵箱。');
      } catch (error) {
        message('身份服務載入失敗，請稍後再試。');
      }
    });
  }

  if (logout) {
    logout.addEventListener('click', async () => {
      const auth = await loadClient();
      if (!auth) return;
      const { error } = await auth.auth.signOut();
      if (error) {
        message(error.message);
        return;
      }
      setAuthenticated(null);
      message('已登出。');
    });
  }

  (async function init() {
    try {
      const redirectError = showAuthErrorFromRedirect();
      const auth = await loadClient();
      if (!auth) {
        setAuthenticated(null);
        if (!redirectError) message('身份服務尚未配置；完成 Supabase 公開設定與登入提供者設定後，登入按鈕即可啟用。');
        return;
      }
      auth.auth.onAuthStateChange((event, session) => {
        setAuthenticated(session?.user || null);
        if (event === 'SIGNED_IN') message('已登入 DORÉ。');
        if (event === 'SIGNED_OUT') message('已登出。');
      });
      await refreshSession();
      if (redirectError) message('登入未完成，請重新選擇登入方式。');
    } catch (error) {
      setAuthenticated(null);
      message('身份服務載入失敗，請稍後再試。');
    }
  })();
})();
