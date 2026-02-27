import pandas as pd
import mplfinance as mpf
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

def create_video():
    print("1. Generating Data...")
    # ডামি ডেটা তৈরি
    dates = pd.date_range(start='2024-01-01', periods=40, freq='D')
    data = np.random.randn(40, 4).cumsum(axis=0)
    data = (data - data.min()) * 10 + 100
    df = pd.DataFrame(data, columns=['Open', 'High', 'Low', 'Close'], index=dates)

    print("2. Creating Chart Image...")
    # চার্ট ইমেজ তৈরি (ফিক্সড সাইজ)
    style = mpf.make_mpf_style(base_mpf_style='yahoo', rc={'font.size': 12})
    chart_filename = 'chart_temp.png'
    # dpi এবং সাইজ ফিক্সড রাখা জরুরি ভিডিওর জন্য
    mpf.plot(df, type='candle', style=style, savefig=dict(fname=chart_filename, dpi=100, figsize=(10, 8)))

    print("3. Processing Image with Pillow...")
    # পিলো দিয়ে টেক্সট বসানো
    if not os.path.exists(chart_filename):
        raise FileNotFoundError("Chart image failed to generate.")

    img_pil = Image.open(chart_filename).convert('RGB')
    width, height = img_pil.size

    # ইমেজের ওপর ড্র করা
    draw = ImageDraw.Draw(img_pil)
    
    # ফন্ট লোড করার চেষ্টা (না পেলে ডিফল্ট)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
    except:
        font = ImageFont.load_default()

    # টেক্সট ১: টাইটেল
    text_top = "PREDICT: UP / DOWN"
    # টেক্সট সেন্টারে বসানোর লজিক
    bbox = draw.textbbox((0, 0), text_top, font=font)
    text_w = bbox[2] - bbox[0]
    draw.text(((width - text_w) / 2, 20), text_top, fill=(0, 0, 0), font=font) # কালো টেক্সট

    # টেক্সট ২: টাইমার
    text_bottom = "5 Seconds"
    bbox2 = draw.textbbox((0, 0), text_bottom, font=font)
    text_w2 = bbox2[2] - bbox2[0]
    draw.text(((width - text_w2) / 2, height - 60), text_bottom, fill=(255, 0, 0), font=font) # লাল টেক্সট

    print("4. Writing Video using OpenCV...")
    
    # PIL ইমেজকে OpenCV ফরম্যাটে কনভার্ট করা (RGB -> BGR)
    frame = np.array(img_pil)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # ভিডিও রাইটার সেটআপ
    video_filename = "trading_quiz.mp4"
    fps = 30
    duration = 5 # সেকেন্ড
    
    # Codec: 'mp4v' হলো সবচেয়ে নিরাপদ অপশন MP4 এর জন্য
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_filename, fourcc, fps, (width, height))

    # ৫ সেকেন্ডের জন্য একই ফ্রেম বারবার রাইট করা
    for _ in range(fps * duration):
        out.write(frame)

    out.release() # ফাইল সেভ করার জন্য এটি মাস্ট
    print(f"Video generated successfully: {video_filename}")

    # ক্লিনআপ
    if os.path.exists(chart_filename):
        os.remove(chart_filename)

if __name__ == "__main__":
    create_video()
