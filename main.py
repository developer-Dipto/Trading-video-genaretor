import pandas as pd
import mplfinance as mpf
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

def create_video():
    print("1. Generating Data...")
    dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
    data = np.random.randn(30, 4).cumsum(axis=0)
    data = (data - data.min()) * 10 + 100
    df = pd.DataFrame(data, columns=['Open', 'High', 'Low', 'Close'], index=dates)

    # চার্ট স্টাইল এবং সেভ
    style = mpf.make_mpf_style(base_mpf_style='nightclouds', rc={'font.size': 10})
    chart_filename = 'chart_temp.png'
    mpf.plot(df, type='candle', style=style, savefig=dict(fname=chart_filename, dpi=100, bbox_inches='tight'))

    print("2. Adding Text using PIL (No ImageMagick)...")
    
    # ১. চার্ট ইমেজ ওপেন করা
    img = Image.open(chart_filename)
    
    # ২. ইমেজের সাইজ অনুযায়ী ব্যাকগ্রাউন্ড বড় করা (যাতে টেক্সট বসানো যায়)
    # আমরা ইমেজের উপরে এবং নিচে একটু জায়গা বাড়াবো
    w, h = img.size
    new_h = h + 150 # টেক্সটের জন্য ১৫০ পিক্সেল জায়গা বাড়ালাম
    background = Image.new('RGB', (w, new_h), (20, 20, 30)) # ডার্ক ব্যাকগ্রাউন্ড
    background.paste(img, (0, 75)) # চার্টটি মাঝখানে বসালাম

    # ৩. টেক্সট ড্র করা
    draw = ImageDraw.Draw(background)
    
    # ফন্ট লোড করা (ডিফল্ট ফন্ট ব্যবহার করছি যাতে এরর না হয়)
    try:
        # লিনাক্সের জন্য ফন্ট পাথ
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
    except:
        # ফন্ট না পেলে ডিফল্ট
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # টেক্সট ১: UP / DOWN
    text_top = "PREDICT: UP / DOWN"
    # টেক্সট মাঝখানে আনার লজিক (সাধারণত pillow তে anchor ব্যবহার করা হয়, এখানে সহজ ভাবে দিচ্ছি)
    draw.text((w/2 - 150, 20), text_top, fill="white", font=font_large)

    # টেক্সট ২: Timer
    text_bottom = "5 Seconds"
    draw.text((w/2 - 80, new_h - 60), text_bottom, fill="yellow", font=font_small)

    # ৪. ফাইনাল ইমেজ সেভ করা
    final_image_path = "final_frame.png"
    background.save(final_image_path)

    print("3. Rendering Video from Image...")
    
    # ৫. ভিডিও তৈরি (শুধুমাত্র ইমেজ থেকে, তাই খুব ফাস্ট হবে)
    clip = ImageClip(final_image_path).set_duration(5)
    
    clip.write_videofile(
        "trading_quiz.mp4", 
        fps=24, 
        codec="libx264", 
        audio=False,     # অডিও অফ (এটি খুব জরুরি)
        preset="medium", # কোয়ালিটি ভালো রাখার জন্য
        threads=4
    )
    print("Video Generated Successfully!")

if __name__ == "__main__":
    create_video()
