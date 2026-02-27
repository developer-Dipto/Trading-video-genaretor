import pandas as pd
import mplfinance as mpf
from moviepy.editor import *
# MoviePy Config (Linux Server Fix)
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/convert"})

import numpy as np
import os

def create_video():
    print("1. Generating Data...")
    dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
    data = np.random.randn(30, 4).cumsum(axis=0)
    data = (data - data.min()) * 10 + 100
    df = pd.DataFrame(data, columns=['Open', 'High', 'Low', 'Close'], index=dates)

    print("2. Creating Chart Image...")
    # savefig এ tight_layout ব্যবহার করলে ইমেজ সাইজ ঠিক থাকে
    style = mpf.make_mpf_style(base_mpf_style='nightclouds', rc={'font.size': 12})
    mpf.plot(df, type='candle', style=style, savefig=dict(fname='chart.png', dpi=100, bbox_inches='tight'))

    print("3. Processing Video...")
    
    # ইমেজ ক্লিপ লোড করা
    if not os.path.exists("chart.png"):
        raise Exception("Chart image was not generated!")
        
    chart_clip = ImageClip("chart.png").set_duration(5)
    
    # টেক্সট ক্লিপ (ফন্ট ও সাইজ এডজাস্ট করা হয়েছে)
    # লিনাক্স সার্ভারে অনেক সময় ফন্ট মিসিং থাকে, তাই ডিফল্ট বা common ফন্ট ব্যবহার নিরাপদ
    txt_clip = TextClip("PREDICT: UP / DOWN", fontsize=50, color='white', font='DejaVu-Sans-Bold')
    txt_clip = txt_clip.set_position(('center', 'top')).set_duration(5)
    
    timer_clip = TextClip("5 Seconds", fontsize=40, color='yellow', font='DejaVu-Sans-Bold')
    timer_clip = timer_clip.set_position(('center', 'bottom')).set_duration(5)

    video = CompositeVideoClip([chart_clip, txt_clip, timer_clip])
    
    print("4. Writing Video File...")
    # ফিক্সড কোডেক সেটিংস
    video.write_videofile(
        "trading_quiz.mp4", 
        fps=24, 
        codec="libx264", 
        audio=False, 
        preset="ultrafast",
        logger=None # লগ আউটপুট ক্লিন রাখার জন্য
    )
    print("Video Generated Successfully!")

if __name__ == "__main__":
    create_video()
