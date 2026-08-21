const ALLOWED_TYPES = new Set(["image/png", "image/jpeg", "image/webp"]);
const SAFE_NAME = /^[a-z0-9][a-z0-9._-]*\.(png|jpe?g|webp)$/i;

function json(data, status = 200) {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: { "content-type": "application/json; charset=utf-8" },
  });
}

function bytesToBase64(bytes) {
  let binary = "";
  const chunk = 0x8000;
  for (let i = 0; i < bytes.length; i += chunk) {
    binary += String.fromCharCode(...bytes.subarray(i, i + chunk));
  }
  return btoa(binary);
}

async function github(env, path, init = {}) {
  const response = await fetch(`https://api.github.com${path}`, {
    ...init,
    headers: {
      accept: "application/vnd.github+json",
      authorization: `Bearer ${env.GITHUB_TOKEN}`,
      "x-github-api-version": "2022-11-28",
      "user-agent": "westsidewatch-image-uploader",
      ...(init.headers || {}),
    },
  });
  const text = await response.text();
  let body = null;
  try { body = text ? JSON.parse(text) : null; } catch { body = { message: text }; }
  if (!response.ok) throw new Error(`GitHub ${response.status}: ${body?.message || text}`);
  return body;
}

export default {
  async fetch(request, env) {
    if (request.method === "GET") {
      return json({ ok: true, service: "westsidewatch-image-uploader", destination: env.DESTINATION_PREFIX });
    }
    if (request.method !== "POST") return json({ error: "Method not allowed" }, 405);

    const auth = request.headers.get("authorization") || "";
    if (!env.UPLOAD_SECRET || auth !== `Bearer ${env.UPLOAD_SECRET}`) {
      return json({ error: "Unauthorized" }, 401);
    }
    if (!env.GITHUB_TOKEN) return json({ error: "GITHUB_TOKEN is not configured" }, 500);

    let form;
    try { form = await request.formData(); }
    catch { return json({ error: "Expected multipart/form-data" }, 400); }

    const file = form.get("file");
    const requestedName = String(form.get("filename") || file?.name || "").trim();
    const message = String(form.get("message") || `Add ONE Studio image: ${requestedName}`).slice(0, 200);

    if (!(file instanceof File)) return json({ error: "Missing file field" }, 400);
    if (!ALLOWED_TYPES.has(file.type)) return json({ error: "Only PNG, JPEG and WebP are allowed" }, 415);
    if (!SAFE_NAME.test(requestedName) || requestedName.includes("..") || requestedName.includes("/")) {
      return json({ error: "Unsafe filename" }, 400);
    }

    const maxBytes = Number(env.MAX_BYTES || 10485760);
    if (file.size < 1 || file.size > maxBytes) return json({ error: `File must be 1-${maxBytes} bytes` }, 413);

    const destination = `${env.DESTINATION_PREFIX}${requestedName}`;
    const encodedPath = destination.split("/").map(encodeURIComponent).join("/");
    const owner = encodeURIComponent(env.GITHUB_OWNER);
    const repo = encodeURIComponent(env.GITHUB_REPO);
    const branch = env.GITHUB_BRANCH || "main";

    let sha;
    try {
      const current = await github(env, `/repos/${owner}/${repo}/contents/${encodedPath}?ref=${encodeURIComponent(branch)}`);
      sha = current?.sha;
    } catch (error) {
      if (!String(error.message).startsWith("GitHub 404:")) return json({ error: error.message }, 502);
    }

    const bytes = new Uint8Array(await file.arrayBuffer());
    const payload = { message, content: bytesToBase64(bytes), branch };
    if (sha) payload.sha = sha;

    try {
      const result = await github(env, `/repos/${owner}/${repo}/contents/${encodedPath}`, {
        method: "PUT",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(payload),
      });
      return json({
        ok: true,
        path: destination,
        bytes: file.size,
        sha: result?.content?.sha,
        commit: result?.commit?.sha,
        raw_url: `https://raw.githubusercontent.com/${env.GITHUB_OWNER}/${env.GITHUB_REPO}/${branch}/${destination}`,
        site_url: `https://${env.GITHUB_OWNER}.github.io/${destination.replace(/^static\//, "")}`,
      }, sha ? 200 : 201);
    } catch (error) {
      return json({ error: error.message }, 502);
    }
  },
};
