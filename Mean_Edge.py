# MEAN FILTERING AND EDGE DETECTION FOR VIDEO

# AUTHOR: CHRISTOS KORGIALAS

import numpy as np
import cv2
import skvideo.io

def Videogray(video):
	cap = cv2.VideoCapture(video)  
	total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  
	fps = int(cap.get(cv2.CAP_PROP_FPS))  
	width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  
	height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) 
	codec = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G') 
	output_video = cv2.VideoWriter('video_gray.avi', codec, fps, (width, height), 0)  
	for f in range(0, total_frames):  
		ret, frame = cap.read()  
		if ret == False:
			break
		# Make it Gray
		frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		# Write output video
		output_video.write(frame_gray)

def Pad(A, size):
    padded_A = np.zeros((A.shape[0] + (size - 1), A.shape[1] + (size - 1), A.shape[2] + (size - 1)), np.uint8)
    padded_A[(size // 2):-(size // 2), (size // 2):-(size // 2), (size // 2):-(size // 2)] = A  
    print(padded_A.shape)
    print(padded_A)
    return padded_A

def Mean(video):
    total_frames = 166
    height = 320
    width = 560
    new = np.zeros((total_frames, height, width))
    for i in range(1, total_frames):
        for j in range(1, height):
            for k in range(1, width):
                new[i,j,k] = ((video[i-1:i+1, j-1:j+1, k-1:k+1]).sum())/(3*3*3)
    return new

def MySobel(video):
   Gradient_X = np.array([[1.0, 0.0, -1.0], [2.0, 0.0, -2.0], [1.0, 0.0, -1.0]])
   Gradient_Y = np.array([[1.0, 2.0, 1.0], [0.0, 0.0, 0.0], [-1.0, -2.0, -1.0]])
   [total_frames, height, width] = np.shape(video)
   sobel_video = np.zeros(shape=(total_frames, height, width))
   for i in range(total_frames - 2):
       for j in range(height - 2):
           for k in range(width - 2):
               x = np.sum(np.multiply(Gradient_X, video[i:i + 3, j:j + 3, k:k + 3]))  
               y = np.sum(np.multiply(Gradient_Y, video[i:i + 3, j:j + 3, k:k + 3]))  
               sobel_video[i + 1, j + 1, k + 1] = np.sqrt(x ** 2 + y ** 2) 
   return sobel_video

def main():  
    
    Videogray('video.avi')
    video = skvideo.io.vread('video_gray.avi')
    video = video[:, :, :, 0]
    video = video.reshape((video.shape[0], video.shape[1], video.shape[2]))
    print(video.shape)
    
    #---TASK 1---#

    # Pad the Video
    padded_video = Pad(video, 3)
    print(padded_video.shape)
    # Apply Mean Filter
    output_1 = Mean(padded_video)
    print("The output_1 shape is:", output_1.shape)
    # Save the Video
    skvideo.io.vwrite('output_1.avi', output_1)
    
    #---TASK 2---#
    
    # Apply MySobel Function
    output_2 = MySobel(video)
    print("The output_2 shape is:", output_2.shape)
    # Save the Video
    skvideo.io.vwrite('output_2.avi', output_2)
    
if __name__ == "__main__":
    main()