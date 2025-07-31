
import praw
import requests
import random
import os

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
REDDIT_USER_AGENT = "kgbtr-ai-bot by /u/yarrak-zeka"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = "mistralai/mixtral-8x7b-instruct"

def get_ai_reply(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://www.reddit.com/u/yarrak-zeka",
        "X-Title": "yarrak-zeka reddit bot"
    }
    data = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": "Sen Reddit'te KGBTR kültürüne göre konuşan bir AI'sın. Mizah, küfür ve absürt flood tarzı yorumlar yaparsın."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    if response.ok:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "G*tüm gibi hissettim, bi' hata olmuş olabilir knk."

def main():
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        username=REDDIT_USERNAME,
        password=REDDIT_PASSWORD,
        user_agent=REDDIT_USER_AGENT
    )

    for mention in reddit.inbox.mentions(limit=10):
        if mention.new:
            try:
                parent_comment = mention.parent()
                post = mention.submission

                prompt = f"""Post başlığı: {post.title}
Post içeriği: {post.selftext}

Üst yorum: {parent_comment.body}

Yukarıdaki içeriğe KGBTR flood havasında, bol küfürlü ama zekice bir cevap ver."""

                reply = get_ai_reply(prompt)
                mention.reply(reply)
                mention.mark_read()
                print("Cevap atıldı:", reply[:100])
            except Exception as e:
                print("Hata:", e)

if __name__ == "__main__":
    main()
