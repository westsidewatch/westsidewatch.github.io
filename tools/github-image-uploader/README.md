# Westside Watch GitHub Image Uploader

A deliberately small upload service for ONE Studio artwork.

## What it does

`POST multipart/form-data` with an image and it commits the binary file directly to:

`static/one/studio/<filename>`

The repository, branch and destination prefix are fixed by `wrangler.toml`.

## Security boundaries

- Accepts only PNG, JPEG and WebP.
- Maximum file size defaults to 10 MB.
- Rejects paths and unsafe filenames; callers cannot write outside `static/one/studio/`.
- `GITHUB_TOKEN` and `UPLOAD_SECRET` are Worker secrets and must never be committed.
- Use a fine-grained GitHub token restricted to `westsidewatch/westsidewatch.github.io` with **Contents: Read and write** only.

## Deploy

```bash
cd tools/github-image-uploader
npm install
npx wrangler login
npx wrangler secret put GITHUB_TOKEN
npx wrangler secret put UPLOAD_SECRET
npm run deploy
```

After deployment, Wrangler prints the HTTPS Worker URL.

## Test

```bash
curl -X POST "https://YOUR-WORKER.workers.dev" \
  -H "Authorization: Bearer $UPLOAD_SECRET" \
  -F "file=@/path/to/philemon-01-dore.png" \
  -F "filename=philemon-01-dore.png" \
  -F "message=Add Doré illustration: Philemon 1"
```

A successful response contains the GitHub commit SHA, repository path, raw URL and final GitHub Pages URL.

## API

### `GET /`
Health check. No secret required.

### `POST /`
Headers:

`Authorization: Bearer <UPLOAD_SECRET>`

Multipart fields:

- `file` — required image binary
- `filename` — optional; defaults to uploaded filename
- `message` — optional commit message

The service checks whether the target already exists. If it does, it supplies the current blob SHA and replaces it; otherwise it creates it.
