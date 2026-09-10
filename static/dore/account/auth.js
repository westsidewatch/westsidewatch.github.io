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
  let busy = true;
  let ready = false;
  let cooldownUntil = 0;
  let settings = null;
  const submit = form?.querySelector('[type="submit"]');
  const providerGroup = document.querySelector('.providers');
  const divider = document.querySelector('.divider');
  const continueLink = document.getElementById('continue');
  if (continueLink) continueLink.href = '/multiwrite/#library';

  function updateControls() {
    providers.forEach(button => {
      const enabled = settings?.external?.[providerMap[button.dataset.provider]] === true;
      button.hidden = !enabled || !sessionPanel?.hidden;
      button.disabled = busy || !ready || !enabled;
    });
    const anyProvider = providers.some(button => !button.hidden);
    if (providerGroup) providerGroup.hidden = !anyProvider;
    if (divider) divider.hidden = !anyProvider;
    const seconds = Math.max(0, Math.ceil((cooldownUntil - Date.now()) / 1000));
    if (submit) {
      submit.disabled = busy || !ready || seconds > 0 || settings?.external?.email !== true;
      submit.textContent = seconds ? `請於 ${seconds} 秒後重寄` : '發送驗證連結';
    }
    if (email) email.disabled = busy || !ready;
    if (logout) logout.disabled = busy || !ready;
    form?.setAttribute('aria-busy', String(busy));
  }

  async function getSettings() {
    const response = await fetch(config.url + '/auth/v1/settings', {
      headers: { apikey: config.publishableKey },
      signal: AbortSignal.timeout(10000)
    });
    if (!response.ok) throw new Error('無法讀取登入方式，請重新整理後再試。');
    settings = await response.json();
  }

  function explain(error) {
    if (error?.status === 429 || /rate.limit/i.test(error?.message || ''))
      return '操作過於頻繁，請稍後再試。';
    if (/fetch|network/i.test(error?.message || '')) return '網路連線失敗，請檢查連線後重試。';
    return error?.message || '請稍後重試。';
  }

  function message(text) {
    if (status) status.textContent = text;
  }

  function setAuthenticated(user) {
    const signedIn = Boolean(user);
    document.querySelectorAll('.account-link').forEach(link => {
      link.textContent = signedIn ? '我的帳號' : '註冊／登入';
    });
    if (sessionPanel) sessionPanel.hidden = !signedIn;
    if (sessionEmail) sessionEmail.textContent = signedIn ? (user.email || '已登入') : '';
    providers.forEach((button) => { button.hidden = signedIn; });
    if (form) form.hidden = signedIn;
    updateControls();
  }

  function showAuthErrorFromRedirect() {
    const hash = window.location.hash.startsWith('#') ? window.location.hash.slice(1) : '';
    const params = new URLSearchParams(hash || window.location.search.slice(1));
    const error = params.get('error_description') || params.get('error');
    if (!error) return false;
    message('登入未完成：' + error.replace(/\+/g, ' '));
    window.history.replaceState({}, document.title, window.location.pathname);
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
    if (busy || !ready || settings?.external?.[provider] !== true) return;
    busy = true; updateControls();
    message('正在連接登入服務……');
    try {
      const auth = await loadClient();
      if (!auth) {
        message('身份服務尚未配置。');
        return;
      }
      const { error } = await auth.auth.signInWithOAuth({
        provider,
        options: { redirectTo: ACCOUNT_URL, ...(provider === 'azure' ? { scopes: 'email' } : {}) }
      });
      if (error) message('登入服務錯誤：' + error.message);
    } catch (error) {
      message('登入服務錯誤：' + explain(error));
    } finally { busy = false; updateControls(); }
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
      if (busy || !ready || Date.now() < cooldownUntil || settings?.external?.email !== true) return;
      if (email) email.value = email.value.trim();
      if (!email || !email.checkValidity()) {
        email?.reportValidity();
        return;
      }
      busy = true; updateControls();
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
            shouldCreateUser: settings.disable_signup !== true
          }
        });
        if (error) throw error;
        cooldownUntil = Date.now() + 60000;
        const timer = setInterval(() => {
          updateControls();
          if (Date.now() >= cooldownUntil) clearInterval(timer);
        }, 1000);
        message('驗證連結已發送。請檢查收件匣及垃圾郵件；點開最新一封信中的連結，即可完成註冊／登入。');
      } catch (error) {
        message('郵箱登入錯誤：' + explain(error));
      } finally { busy = false; updateControls(); }
    });
  }

  if (logout) {
    logout.addEventListener('click', async () => {
      if (busy || !ready) return;
      busy = true; updateControls();
      try {
        const auth = await loadClient();
        if (!auth) return;
        const { error } = await auth.auth.signOut();
        if (error) throw error;
        setAuthenticated(null);
        message('已登出。');
      } catch (error) {
        message('登出錯誤：' + explain(error));
      } finally { busy = false; updateControls(); }
    });
  }

  (async function init() {
    updateControls();
    const redirectError = showAuthErrorFromRedirect();
    try {
      const auth = await loadClient();
      if (!auth) {
        setAuthenticated(null);
        if (!redirectError) message('身份服務尚未配置。');
        return;
      }
      if (form) await getSettings();
      ready = true;
      auth.auth.onAuthStateChange((event, session) => {
        setAuthenticated(session?.user || null);
        if (event === 'SIGNED_IN') message('已登入 DORÉ。');
        if (event === 'SIGNED_OUT') message('已登出。');
      });
      await refreshSession();
      if (redirectError) message('登入未完成，請重新選擇登入方式。');
    } catch (error) {
      setAuthenticated(null);
      message('身份服務載入失敗：' + explain(error));
    } finally { busy = false; updateControls(); }
  })();
})();
