# main.py
import pandas as pd
import mplfinance as mpf
from moviepy.editor import *
from moviepy.config import change_settings
import numpy as np

# Linux/Server এ ImageMagick কনফিগারেশন (MoviePy এর জন্য জরুরি)
change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/convert"})

def create_video():
    print("Generating Data...")
    # ১. ডামি ট্রেডিং ডেটা তৈরি
    dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
    data = np.random.randn(30, 4).cumsum(axis=0)
    data = (data - data.min()) * 10 + 100  # পজিটিভ ভ্যালু
    df = pd.DataFrame(data, columns=['Open', 'High', 'Low', 'Close'], index=dates)

    # ২. চার্ট ইমেজ তৈরি
    print("Creating Chart...")
    style = mpf.make_mpf_style(base_mpf_style='nightclouds', rc={'font.size': 12})
    mpf.plot(df, type='candle', style=style, savefig='chart.png')

    # ৩. ভিডিও এডিটিং
    print("Rendering Video...")
    
    # চার্ট ক্লিপ
    chart_clip = ImageClip("chart.png").set_duration(5)
    
    # টেক্সট ওভারলে (UP/DOWN)
    txt_clip = TextClip("PREDICT: UP / DOWN", fontsize=50, color='white', font='Liberation-Sans-Bold')
    txt_clip = txt_clip.set_position(('center', 'top')).set_duration(5)
    
    # কাউন্টডাউন টেক্সট
    timer_clip = TextClip("5 Seconds", fontsize=40, color='yellow', font='Liberation-Sans-Bold')
    timer_clip = timer_clip.set_position(('center', 'bottom')).set_duration(5)

    # ফাইনাল ভিডিও
    video = CompositeVideoClip([chart_clip, txt_clip, timer_clip])
    video.write_videofile("trading_quiz.mp4", fps=24)
    print("Video Generated Successfully!")

if __name__ == "__main__":
    create_video()
