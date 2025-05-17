import os
import json
import socket
import pandas as pd
import feedparser
from datetime import datetime, timedelta
from typing import List, Dict

DEFAULT_HOURS = 24
SENT_FILE = "sent_links.json"
socket.setdefaulttimeout(5)

# Жёсткий путь к config.json в папке панели
CONFIG_PATH = r"C:\Bots\bot_config_panel\config.json"

def fetch_rss_raw(hours: int = DEFAULT_HOURS) -> List[Dict[str, str]]:
    results = []
    now = datetime.utcnow()
    cutoff = now - timedelta(hours=hours)

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
    rss_feeds = config.get("rss_feeds", {})

    for name, url in rss_feeds.items():
        try:
            d = feedparser.parse(url)
            for entry in d.entries:
                if hasattr(entry, "published_parsed"):
                    published = datetime(*entry.published_parsed[:6])
                    if published >= cutoff:
                        results.append({
                            "источник": name,
                            "заголовок": entry.title,
                            "ссылка": entry.link
                        })
        except Exception as e:
            print(f"Ошибка при обработке {name}: {e}")
            continue
    return results

def load_sent_links() -> set:
    if os.path.exists(SENT_FILE):
        with open(SENT_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()

def save_sent_links(links: set):
    with open(SENT_FILE, "w", encoding="utf-8") as f:
        json.dump(list(links), f, ensure_ascii=False, indent=2)

def filter_new_items(items: List[Dict[str, str]]) -> List[Dict[str, str]]:
    sent_links = load_sent_links()
    new_items = [i for i in items if i["ссылка"] not in sent_links]
    save_sent_links(sent_links.union(i["ссылка"] for i in new_items))
    return new_items

def limit_news(items: List[Dict[str, str]], rus_limit=10, per_src_limit=2) -> List[Dict[str, str]]:
    limited = []
    sources = {}
    for item in items:
        src = item["источник"]
        if sources.get(src, 0) < per_src_limit:
            limited.append(item)
            sources[src] = sources.get(src, 0) + 1
        if len(limited) >= rus_limit:
            break
    return limited

def get_known_tickers() -> List[str]:
    try:
        df = pd.read_csv("ticker_map.csv")
        return df["company"].str.lower().tolist()
    except Exception:
        return []

def filter_by_keywords(items: List[Dict[str, str]]) -> List[Dict[str, str]]:
    keywords = ["дивиденды", "отчёт", "прибыль", "рост", "падение", "фьючерсы", "банкротство"]
    return [i for i in items if any(k in i["заголовок"].lower() for k in keywords)]

def filter_by_tickers(items: List[Dict[str, str]]) -> List[Dict[str, str]]:
    tickers = get_known_tickers()
    return [i for i in items if any(t in i["заголовок"].lower() for t in tickers)]

def assess_importance(item: Dict[str, str]) -> int:
    title = item["заголовок"].lower()
    score = 0
    keywords = ["дивиденды", "прибыль", "убыток", "отчёт", "фьючерсы", "банкротство"]
    emotional = ["обвал", "скачок", "рекорд", "срочно", "резко"]
    if any(k in title for k in keywords):
        score += 2
    if any(e in title for e in emotional):
        score += 1
    if any(t in title for t in get_known_tickers()):
        score += 2
    if item["источник"] in {"RBK", "Kommersant", "Finam"}:
        score += 1
    return score

def sort_by_importance(items: List[Dict[str, str]]) -> List[Dict[str, str]]:
    return sorted(items, key=assess_importance, reverse=True)

def fetch_menu_all_news(hours: int = DEFAULT_HOURS) -> List[Dict[str, str]]:
    raw = fetch_rss_raw(hours)
    limited = limit_news(raw, rus_limit=10, per_src_limit=2)
    limited = filter_new_items(limited)
    if not limited:
        return [{"источник": "-", "заголовок": "Новостей пока нет", "ссылка": ""}]
    return [{"источник": i["источник"], "заголовок": i["заголовок"], "ссылка": i["ссылка"]} for i in limited]

def fetch_menu_company_news(hours: int = DEFAULT_HOURS) -> List[Dict[str, str]]:
    raw = fetch_rss_raw(hours)
    filtered = filter_by_tickers(raw)
    limited = limit_news(filtered, rus_limit=10, per_src_limit=2)
    limited = filter_new_items(limited)
    if not limited:
        return [{"источник": "-", "заголовок": "Новостей пока нет", "ссылка": ""}]
    return [{"источник": i["источник"], "заголовок": i["заголовок"], "ссылка": i["ссылка"]} for i in limited]

def fetch_menu_digests(hours: int = DEFAULT_HOURS) -> List[Dict[str, str]]:
    raw = fetch_rss_raw(hours)
    filtered = filter_by_keywords(raw)
    sorted_items = sort_by_importance(filtered)
    limited = limit_news(sorted_items, rus_limit=10, per_src_limit=2)
    limited = filter_new_items(limited)
    if not limited:
        return [{"источник": "-", "заголовок": "Новостей пока нет", "ссылка": ""}]
    return [{"источник": i["источник"], "заголовок": i["заголовок"], "ссылка": i["ссылка"]} for i in limited]
