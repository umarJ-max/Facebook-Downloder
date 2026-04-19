export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") return res.status(200).end();
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed" });

  const { url } = req.body;
  if (!url || !url.includes("facebook.com") && !url.includes("fb.watch") && !url.includes("fb.com")) {
    return res.status(400).json({ error: "Please provide a valid Facebook video URL." });
  }

  try {
    const apiUrl = `https://www.y2mate.com/mates/analyzeV2/ajax`;
    const formData = new URLSearchParams({
      k_query: url,
      k_page: "Facebook",
      hl: "en",
      q_auto: 0,
    });

    const analyzeRes = await fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        Referer: "https://www.y2mate.com/",
      },
      body: formData.toString(),
    });

    const data = await analyzeRes.json();

    if (!data || data.status !== "ok") {
      return res.status(500).json({ error: "Could not extract video. The video may be private or unavailable." });
    }

    const links = data.links?.mp4 || data.links?.video || {};
    const qualities = Object.entries(links).map(([key, val]) => ({
      quality: val.q || key,
      size: val.size || "Unknown",
      k: val.k,
    }));

    if (!qualities.length) {
      return res.status(404).json({ error: "No downloadable formats found. The video may be private." });
    }

    return res.status(200).json({
      title: data.title || "Facebook Video",
      thumbnail: data.thumbnail || null,
      qualities,
    });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: "Something went wrong. Please try again." });
  }
}
