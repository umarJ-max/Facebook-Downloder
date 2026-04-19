# FBSave — Facebook Video Downloader

A fast, clean Facebook video downloader built with Vanilla JS frontend and Node.js serverless API. Deployable on Vercel in one click.

## Features
- Download Facebook videos in HD & SD
- Thumbnail preview + video title
- No login, no watermark, no limits
- Mobile-responsive Facebook-themed UI
- Serverless API — zero server management

## Tech Stack
- **Frontend**: Vanilla HTML/CSS/JS (single file in `/public`)
- **Backend**: Node.js Vercel Serverless Function (`/api/download.js`)
- **Hosting**: Vercel (auto-deploy from GitHub)

## Deploy to Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new)

1. Push this repo to GitHub
2. Go to [vercel.com](https://vercel.com) → New Project → Import your repo
3. No environment variables needed
4. Click Deploy — done!

## Local Development

```bash
npm i -g vercel
vercel dev
```

Then open `http://localhost:3000`

## Project Structure

```
fb-downloader/
├── api/
│   └── download.js       # Serverless API endpoint
├── public/
│   └── index.html        # Frontend UI
├── vercel.json           # Routing config
└── package.json
```

## Notes
- Only works on public Facebook videos (not private/friends-only)
- For personal & educational use only
- Respect copyright — only download videos you own or have permission to save

---
Made by Umar J
