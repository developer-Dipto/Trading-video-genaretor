import pandas as pd
import mplfinance as mpf
import cv2
import numpy as np
import os

def create_video():
    print("1. Generating Data...")
    dates = pd.date_range(start='2024-01-01', periods=40, freq='D')
    data = np.random.randn(40, 4).cumsum(axis=0)
    data = (data - data.min()) * 10 + 100
    df = pd.DataFrame(data, columns=['Open', 'High', 'Low', 'Close'], index=dates)

    print("2. Creating Chart Image...")
    # চার্ট স্টাইল
    style = mpf.make_mpf_style(base_mpf_style='yahoo', rc={'font.size': 12})
    chart_filename = 'chart_temp.png'
    
    # --- ERROR FIX ---
    # figsize এখানে বাইরে থাকবে, savefig এর ভেতরে না।
    mpf.plot(df, type='candle', style=style, figsize=(12.8, 7.2), savefig=dict(fname=chart_filename, dpi=100))

    print("3. Processing Video with OpenCV...")
    
    # ইমেজ রিড করা
    if not os.path.exists(chart_filename):
        raise FileNotFoundError("Chart image failed to generate.")

    # ইমেজ লোড করা
    img = cv2.imread(chart_filename)
    
    # সাইজ ফিক্স করা (1280x720) - ভিডিও প্লে হওয়ার জন্য রেজোলিউশন ইভেন নাম্বার হতে হয়
    img = cv2.resize(img, (1280, 720))
    height, width, layers = img.shape

    # টেক্সট বসানো (OpenCV দিয়ে)
    # UP/DOWN Text
    cv2.putText(img, "PREDICT: UP / DOWN", (400, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3, cv2.LINE_AA)
    # Timer Text
    cv2.putText(img, "5 Seconds", (550, 680), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3, cv2.LINE_AA)

    # ভিডিও তৈরি
    video_filename = "trading_quiz.mp4"
    fps = 30
    duration = 5 
    
    # Codec: 'mp4v' লিনাক্স এবং উইন্ডোজ উভয়ের জন্য বেস্ট
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_filename, fourcc, fps, (width, height))

    # ভিডিও রাইট করা
    for _ in range(fps * duration):
        out.write(img)

    out.release()
    print(f"Video generated successfully: {video_filename}")

    # টেম্পোরারি ফাইল ডিলিট
    if os.path.exists(chart_filename):
        os.remove(chart_filename)

if __name__ == "__main__":
    create_video()
