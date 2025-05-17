from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
import json
import subprocess
import psutil

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    with open("config.json", "r", encoding="utf-8") as f:
        rss_feeds = json.load(f).get("rss_feeds", {})
    return templates.TemplateResponse("index.html", {"request": request, "config": config, "rss_feeds": rss_feeds})

@app.post("/save")
async def save_config(
    request: Request,
    hours: int = Form(...),
    rus_limit: int = Form(...),
    per_src_limit: int = Form(...),
    keywords: str = Form(...),
    rss_feeds: str = Form(...)
):
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)

        config["hours"] = hours
        config["rus_limit"] = rus_limit
        config["per_src_limit"] = per_src_limit
        config["keywords"] = [kw.strip() for kw in keywords.split(",") if kw.strip()]
        config["rss_feeds"] = json.loads(rss_feeds)

        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        return HTMLResponse(f"<p>Ошибка сохранения: {e}</p>")

@app.post("/reset_config")
async def reset_config():
    try:
        with open("default_config.json", "r", encoding="utf-8") as default_file:
            default_config = json.load(default_file)
        with open("config.json", "w", encoding="utf-8") as config_file:
            json.dump(default_config, config_file, ensure_ascii=False, indent=2)
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        return HTMLResponse(f"<p>Ошибка сброса: {e}</p>")

@app.get("/download_config")
async def download_config():
    return FileResponse("config.json", filename="config.json", media_type="application/json")

def kill_existing_bot():
    found = False
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['cmdline'] and any("bot.py" in arg for arg in proc.info['cmdline']):
                print(f"[INFO] Завершаю процесс бота (PID: {proc.pid})...")
                proc.kill()
                found = True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    if not found:
        print("[INFO] Бот не был запущен — запускаю новый экземпляр.")

@app.post("/restart_bot")
async def restart_bot():
    try:
        kill_existing_bot()
        print("[INFO] Запускаю bot.py через cmd /k в новой консоли...")
        subprocess.Popen(
            ["cmd", "/k", "python", "bot.py"],
            cwd=r"C:\Bots\news_assistant_ready",
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        print("[SUCCESS] Бот успешно запущен в отдельной консоли.")
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        print(f"[ERROR] Ошибка при перезапуске бота: {e}")
        return HTMLResponse(f"<p>Ошибка при перезапуске бота: {e}</p>")
