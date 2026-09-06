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

  const SUPABASE_JS_FALLBACK = 'https://unpkg.com/@supabase/supabase-js@2.115.0';
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
        script.src = SUPABASE_JS_FALLBACK;
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
      });
    }
    if (!window.supabase?.createClient) throw new Error('Supabase JavaScript client 未載入');
    if (!client) client = window.supabase.createClient(config.url, config.publishableKey);
    return client;
  }

  async function refreshSession() {
    try {
      const auth = await loadClient();
      if (!auth) {
        setAuthenticated(null);
        message('身份服務尚未配置。');
        return;
      }
      const { data, error } = await auth.auth.getSession();
      if (error) throw error;
      setAuthenticated(data.session?.user || null);
      if (data.session?.user) message('已登入 DORÉ。');
      else message('請選擇登入方式。');
    } catch (error) {
      setAuthenticated(null);
      message('身份服務載入失敗：' + (error?.message || '未知錯誤'));
    }
  }

  async function signIn(provider) {
    message('正在連接登入服務……');
    try {
      const auth = await loadClient();
      if (!auth) {
        message('身份服務尚未配置。');
        return;
      }
      const { error } = await auth.auth.signInWithOAuth({
        provider,
        options: { redirectTo: ACCOUNT_URL }
      });
      if (error) message('登入服務錯誤：' + error.message);
    } catch (error) {
      message('登入服務錯誤：' + (error?.message || '未知錯誤'));
    }
  }

  providers.forEach((button) => {
    button.addEventListener('click', (event) => {
      event.preventDefault();
      signIn(providerMap[button.dataset.provider]);
    });
  });

  if (form) {
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      if (!email || !email.checkValidity()) {
        email?.reportValidity();
        return;
      }
      message('正在發送驗證連結……');
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
        message(error ? '郵箱登入錯誤：' + error.message : '驗證連結已發送，請檢查你的電子郵箱。');
      } catch (error) {
        message('郵箱登入錯誤：' + (error?.message || '未知錯誤'));
      }
    });
  }

  if (logout) {
    logout.addEventListener('click', async () => {
      try {
        const auth = await loadClient();
        if (!auth) return;
        const { error } = await auth.auth.signOut();
        if (error) throw error;
        setAuthenticated(null);
        message('已登出。');
      } catch (error) {
        message('登出錯誤：' + (error?.message || '未知錯誤'));
      }
    });
  }

  (async function init() {
    const redirectError = showAuthErrorFromRedirect();
    try {
      const auth = await loadClient();
      if (!auth) {
        setAuthenticated(null);
        if (!redirectError) message('身份服務尚未配置。');
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
      message('身份服務載入失敗：' + (error?.message || '未知錯誤'));
    }
  })();
})();
