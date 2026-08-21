# Westside Watch GitHub Image Uploader

A deliberately small upload service for ONE Studio artwork.

## What it does

`POST multipart/form-data` with an image and it commits the binary file directly to:

`static/one/studio/<filename>`

The service then reads the file back from GitHub and compares the returned blob SHA. It reports success only when the write is verified.

## Security boundaries

- Accepts only PNG, JPEG and WebP.
- Maximum file size defaults to 10 MB.
- Rejects paths and unsafe filenames; callers cannot write outside `static/one/studio/`.
- `GITHUB_TOKEN` and `UPLOAD_SECRET` are Worker secrets and must never be committed.
- Use a fine-grained GitHub token restricted to `westsidewatch/westsidewatch.github.io` with **Contents: Read and write** only.

## Deployed endpoint

Current ONE Studio endpoint:

`https://one-studio-upload.westsidewatchca.workers.dev`

Runtime variables:

- `GITHUB_OWNER=westsidewatch`
- `GITHUB_REPO=westsidewatch.github.io`
- `GITHUB_BRANCH=main`
- `DESTINATION_PREFIX=static/one/studio/`
- `MAX_BYTES=10485760`

Secrets:

- `GITHUB_TOKEN`
- `UPLOAD_SECRET`

## Upload from the repository helper

The normal client entry point is:

```bash
read -s UPLOAD_SECRET
export UPLOAD_SECRET
scripts/one-studio-upload.sh /path/to/image.png target-name.png
```

The helper refuses to treat the request as successful unless the Worker returns all of:

- `ok: true`
- `verified: true`
- a GitHub `commit` SHA

## Direct API test

```bash
curl -X POST "https://one-studio-upload.westsidewatchca.workers.dev" \
  -H "Authorization: Bearer $UPLOAD_SECRET" \
  -F "file=@/path/to/philemon-01-dore.png" \
  -F "filename=philemon-01-dore.png" \
  -F "message=Add Doré illustration: Philemon 1"
```

A verified successful response contains the repository path, blob SHA, commit SHA, raw URL and GitHub Pages URL.

## API

### `GET /`

Health check. No secret required.

### `POST /`

Header:

`Authorization: Bearer <UPLOAD_SECRET>`

Multipart fields:

- `file` — required image binary
- `filename` — optional; defaults to uploaded filename
- `message` — optional commit message

The service checks whether the target already exists. If it does, it supplies the current blob SHA and replaces it; otherwise it creates it. After the PUT, it immediately performs a GitHub GET and verifies the returned SHA before returning `ok: true`.
