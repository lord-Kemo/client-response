# Valor AI Client Response Form

This repository is ready to publish the client confirmation form through GitHub Pages.

## GitHub Pages

The workflow in `.github/workflows/pages.yml` publishes only these public files:

- `index.html`
- `client.html`
- `config.js`

It intentionally does not publish `local_server.py` or `responses/`, because saved client responses should not be public website files.

After pushing to `main`, enable Pages from **Settings > Pages** and select **GitHub Actions** as the source if GitHub asks for a publishing source. The public URL should be:

```text
https://lord-kemo.github.io/client-response/
```

## Saving Responses

GitHub Pages is static hosting. It can serve HTML, CSS, and JavaScript, but it cannot run `local_server.py` or write new JSON files into this repository.

Current behavior:

- Local use with `local_server.py`: submissions are saved in `responses/`.
- GitHub Pages use without a save endpoint: the client gets an automatic JSON download and can send it back to you.
- GitHub Pages use with a hosted save endpoint: set `window.VALOR_SAVE_ENDPOINT` in `config.js`.

Example:

```js
window.VALOR_SAVE_ENDPOINT = 'https://your-form-endpoint.example/submit';
```

Good endpoint choices are Formspree, Basin, Getform, Supabase Edge Functions, Cloudflare Workers, or a small custom API. Do not put GitHub tokens or private API keys in `config.js`, because this file is public.

## Local Testing

```bash
python local_server.py
```

Then open:

```text
http://localhost:8080/client.html
```
