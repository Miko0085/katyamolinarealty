MOLINA Prototype B v9 — Video Library
Open index.html, choose Insights & Media > Video Library or Shorts & Reels.
For embedded playback use a local HTTP server: python -m http.server 8080
Then visit http://localhost:8080/videos.html. Internet and YouTube embedding permission are needed.
Eight watch pages: one existing third-party reference, seven editorial placeholders. No videos are attributed to Katya. Chapter buttons on the reference are technical seek markers, not actual chapters. Transcript content is not available and is not invented. Placeholder chapters show selection only.
All new pages are noindex until real content is supplied. integration/videoobject-template.json is a non-published template; populate only verified metadata, real chapters and canonical URLs in WordPress. Video sitemap and production schema are future CMS tasks.
Optional read-only YouTube metadata import: set YOUTUBE_API_KEY in your environment and run python integration/youtube_sync.py --channel-id YOUR_CHANNEL_ID. This exports draft JSON only, does not update the static catalog or publish. Captions need separate authorization; auto-sync and WordPress rendering are not connected.
