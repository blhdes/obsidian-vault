#!/usr/bin/env python3
"""tunebat_fetch.py — Fetch a song's musical attributes from tunebat.com.

Tunebat is gated behind a Cloudflare "managed challenge" that requires real
JavaScript execution. We use headless Chromium (Playwright) to load the page
like a real browser, then parse the rendered HTML with BeautifulSoup.

Usage:
    tunebat_fetch.py <tunebat_url_or_search_query...>

Examples:
    tunebat_fetch.py "blinding lights weeknd"
    tunebat_fetch.py "https://tunebat.com/Info/Blinding-Lights-The-Weeknd/0VjIjW4..."

Output: JSON to stdout with keys
    artist, title, key, camelot, bpm, popularity,
    energy, danceability, happiness, url
Errors: JSON {"error": "..."} to stderr, exit code 1.
"""
import json
import sys
from urllib.parse import quote

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout


UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"
)
LAUNCH_ARGS = ["--disable-blink-features=AutomationControlled"]
NAV_TIMEOUT_MS = 45_000
WAIT_TIMEOUT_MS = 45_000
CF_CLEAR_TIMEOUT_MS = 45_000


def is_tunebat_url(s: str) -> bool:
    return s.lower().startswith(("https://tunebat.com/", "http://tunebat.com/"))


def _strip_cf_params(url: str) -> str:
    """Remove Cloudflare challenge tokens from the URL we report back."""
    from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

    parts = urlsplit(url)
    clean_q = [(k, v) for k, v in parse_qsl(parts.query) if not k.startswith("__cf_chl")]
    return urlunsplit(parts._replace(query=urlencode(clean_q)))


def _wait_past_cloudflare(page) -> None:
    """Cloudflare's managed challenge has two phases:
    1. URL contains __cf_chl_* tokens during the JS challenge.
    2. After tokens clear, an interstitial 'Verification successful, waiting...'
       page may render briefly before the real page loads.
    Wait for both: clean URL, then a non-challenge title."""
    try:
        page.wait_for_url(lambda u: "__cf_chl" not in u, timeout=CF_CLEAR_TIMEOUT_MS)
    except PWTimeout:
        pass
    try:
        page.wait_for_function(
            "() => document.title && !document.title.toLowerCase().includes('just a moment')",
            timeout=CF_CLEAR_TIMEOUT_MS,
        )
    except PWTimeout:
        pass


def fetch_song_page(query: str) -> tuple[str, str]:
    """Returns (final_url, html). Searches if query isn't already a tunebat URL."""
    with sync_playwright() as p:
        # channel="chrome" uses the user's installed Chrome (less detectable than
        # Playwright's bundled headless-shell). Falls back to bundled chromium.
        try:
            browser = p.chromium.launch(channel="chrome", headless=True, args=LAUNCH_ARGS)
        except Exception:
            browser = p.chromium.launch(headless=True, args=LAUNCH_ARGS)
        ctx = browser.new_context(user_agent=UA, viewport={"width": 1280, "height": 800})
        ctx.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        page = ctx.new_page()
        try:
            if is_tunebat_url(query):
                page.goto(query, wait_until="domcontentloaded", timeout=NAV_TIMEOUT_MS)
            else:
                search_url = f"https://tunebat.com/Search?q={quote(query)}"
                page.goto(search_url, wait_until="domcontentloaded", timeout=NAV_TIMEOUT_MS)
                page.wait_for_selector("a[href*='/Info/']", timeout=WAIT_TIMEOUT_MS)
                first = page.query_selector("a[href*='/Info/']")
                if first is None:
                    raise RuntimeError(f"No tunebat results for: {query}")
                href = first.get_attribute("href") or ""
                full = href if href.startswith("http") else f"https://tunebat.com{href}"
                page.goto(full, wait_until="domcontentloaded", timeout=NAV_TIMEOUT_MS)

            _wait_past_cloudflare(page)
            page.wait_for_selector("div.NYZ7Y", timeout=WAIT_TIMEOUT_MS)
            final_url = _strip_cf_params(page.url)
            return final_url, page.content()
        finally:
            browser.close()


def parse_song(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("div", class_="NYZ7Y")
    if main is None:
        raise RuntimeError("Stat block not found (page layout may have changed)")

    out = {
        "artist": None, "title": None,
        "key": None, "bpm": None, "camelot": None,
        "popularity": None, "energy": None, "danceability": None, "happiness": None,
    }

    children = main.find_all(recursive=False)
    if not children:
        raise RuntimeError("Stat block has no children")

    # Cell 0: artist (first typography div), title (second).
    typography = children[0].find_all("div", class_="ant-typography")
    if len(typography) >= 2:
        out["artist"] = typography[0].get_text(strip=True)
        out["title"] = typography[1].get_text(strip=True)
    else:
        texts = [t for t in children[0].stripped_strings]
        if len(texts) >= 2:
            out["artist"], out["title"] = texts[0], texts[1]

    # Cells 1-4 are labeled: each contains "<value>" and "<label>" as text.
    label_to_key = {
        "Key": "key", "BPM": "bpm",
        "Camelot": "camelot", "Popularity": "popularity",
    }
    for child in children[1:]:
        texts = [t for t in child.stripped_strings]
        # Find a known label among texts; the value is the other text.
        label = next((t for t in texts if t in label_to_key), None)
        if label:
            value = next((t for t in texts if t != label), None)
            if value is not None:
                out[label_to_key[label]] = value

    # Unlabeled cells: GFAiD class, in visual order Energy, Danceability, Happiness.
    meters = main.find_all("div", class_="GFAiD", recursive=False)
    if len(meters) >= 3:
        out["energy"] = meters[0].get_text(strip=True)
        out["danceability"] = meters[1].get_text(strip=True)
        out["happiness"] = meters[2].get_text(strip=True)

    # Coerce numeric strings to ints where they parse cleanly.
    for k in ("bpm", "popularity", "energy", "danceability", "happiness"):
        v = out.get(k)
        if v is not None:
            try:
                out[k] = int(v)
            except ValueError:
                pass

    return out


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: tunebat_fetch.py <tunebat_url_or_search_query>", file=sys.stderr)
        sys.exit(2)
    query = " ".join(sys.argv[1:]).strip()
    if not query:
        print(json.dumps({"error": "empty query"}), file=sys.stderr)
        sys.exit(2)

    try:
        url, html = fetch_song_page(query)
        data = parse_song(html)
        data["url"] = url
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except PWTimeout as e:
        print(json.dumps({"error": f"timeout: {e}"}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
