import cv2  
import numpy as np  
  
# 打开输入视频文件  
input_video = cv2.VideoCapture('video/video8.mp4')  
  
# 获取输入视频的帧率、宽度和高度  
fps = input_video.get(cv2.CAP_PROP_FPS)  
width = int(input_video.get(cv2.CAP_PROP_FRAME_WIDTH))  
height = int(input_video.get(cv2.CAP_PROP_FRAME_HEIGHT))  
  
# 创建输出视频文件  
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 根据你的需求，这里使用了H.264编码  
output_video = cv2.VideoWriter('video/output_video8.mp4', fourcc, fps, (width, height), isColor=True)  
  
# 逐帧读取输入视频并转换为灰度图像，然后写入输出视频  
frame_count = 0  
while True:  
    ret, frame = input_video.read()  
    if not ret:  
        break  
  
    frame_count += 1  
    if frame_count == 1:  # 第一帧不进行任何处理，直接写入输出视频  
        # 将当前帧的B通道和G通道设为灰度图像，R通道设为0  
        b_channel = frame[:, :, 0]  
        g_channel = frame[:, :, 1]  
        r_channel = np.zeros_like(b_channel)  
        bgr_frame = cv2.merge([b_channel, g_channel, r_channel])  
        output_video.write(bgr_frame)  
    else:  # 从第二帧开始处理  
        # 转换为灰度图像  
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
          
        # 计算当前帧的G通道数据为灰度图像与前一帧的加权平均  
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)  
        g_channel = cv2.addWeighted(gray_frame, 0.5, prev_gray, 0.5, 0)  
          
        # R通道的数据全是0  
        r_channel = np.zeros_like(gray_frame)  
          
        # 合并三个通道的数据  
        bgr_frame = cv2.merge([gray_frame, g_channel, r_channel])  
          
        # 将结果写入输出视频文件  
        output_video.write(bgr_frame)  
          
    # 将当前帧设置为前一帧，用于下一次循环的计算  
    prev_frame = frame.copy()  
  
# 释放视频文件资源  
input_video.release()  
output_video.release()
