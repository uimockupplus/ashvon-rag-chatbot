
"""Restricted Playwright crawler for Ashvon Technologies."""

import json
import logging
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

logger = logging.getLogger(__name__)

APPROVED_URLS = [
    "https://ashvontech.com/",
    "https://ashvontech.com/about",
    "https://ashvontech.com/edtech",
    "https://ashvontech.com/it-services",
]

OUTPUT_FILE = Path("data/raw/ashvon_website.json")


def validate_url(url: str) -> bool:
    """Allow only the four explicitly approved URLs."""
    return url.rstrip("/") in {
        approved.rstrip("/") for approved in APPROVED_URLS
    }


def extract_page(page, url: str) -> dict:
    """Render and extract clean text from one approved page."""

    if not validate_url(url):
        raise ValueError(f"URL is not approved: {url}")

    response = page.goto(
        url,
        wait_until="domcontentloaded",
        timeout=60000,
    )

    if response and response.status >= 400:
        raise RuntimeError(
            f"Page returned HTTP {response.status}: {url}"
        )

    try:
        page.wait_for_load_state("networkidle", timeout=15000)
    except PlaywrightTimeoutError:
        logger.warning("Network idle timeout for %s; continuing.", url)

    # Remove elements that do not contain useful page content.
    page.evaluate("""
        () => {
            const selectors = [
                'script', 'style', 'noscript', 'svg',
                'header', 'footer', 'nav',
                'form', 'button', 'input', 'select',
                'textarea', 'iframe',
                '[role="navigation"]',
                '[role="banner"]',
                '[role="contentinfo"]',
                '.cookie-banner',
                '.cookie-consent',
                '.popup',
                '.modal'
            ];

            document.querySelectorAll(selectors.join(','))
                .forEach(element => element.remove());
        }
    """)

    title = page.title().strip()

    content = page.locator("body").inner_text(timeout=15000)

    # Normalize whitespace and remove empty lines.
    lines = [
        re.sub(r"\s+", " ", line).strip()
        for line in content.splitlines()
    ]

    content = "\n".join(line for line in lines if line)
    content = content.strip()

    if not content:
        raise RuntimeError(f"No readable content extracted from {url}")

    return {
        "page_url": url,
        "page_title": title,
        "content": content,
        "crawl_date": datetime.now(timezone.utc).isoformat(),
    }


def crawl_website() -> list[dict]:
    """Crawl only the four approved pages."""

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    results = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)

        context = browser.new_context(
            java_script_enabled=True,
            locale="en-US",
        )

        page = context.new_page()

        for url in APPROVED_URLS:
            try:
                logger.info("Crawling: %s", url)
                result = extract_page(page, url)
                results.append(result)

                logger.info(
                    "Extracted %d characters from %s",
                    len(result["content"]),
                    url,
                )

            except Exception:
                logger.exception("Failed to crawl %s", url)

        browser.close()

    if not results:
        raise RuntimeError(
            "No pages were successfully crawled. "
            "Check website connectivity and logs."
        )

    OUTPUT_FILE.write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    logger.info("Saved %d pages to %s", len(results), OUTPUT_FILE)

    return results
