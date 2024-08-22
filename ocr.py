import time
import mss
import io
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from paddleocr import PaddleOCR, draw_ocr

# Initialize PaddleOCR
# ocr = PaddleOCR(use_angle_cls=True, lang='en')
ocr = PaddleOCR(
    use_angle_cls=True, # Whether to load classification model
    ocr_version="PP-OCRv3", #OCR Model version number, PP-OCRv3 is the latest but generally does not seem to impact performance or accuracy
    # some tutorials claim you can or need to specify the language when giving specific models, I always run into errors when I do this
    # lang='en',
    # sometimes for speicifc recognition models you need to specify the corresponding deteciton model directory but generally don't change this 
    # unless you know what you're doing the default detection model generally gives great accuracy and performance tradeoffs from my experimentations
    det_model_dir="PaddleOCR_pub/inference/en_PP-OCRv3_det_infer/",
    rec_model_dir="PaddleOCR_pub/inference/en_PP-OCRv4_rec_infer/",
    max_text_length=1000, # max number of characters in a single line,
    drop_score=0, # drop text boxes with scores lower than this value
    use_space_char=True)
# ="PaddleOCR_pub/inference/ch_ppocr_server_v2.0_rec_infer/" terrible

SHOW_OCR_RESULTS = False
VISUALIZE_OCR_RESULTS = True

def take_screenshot():
    with mss.mss() as sct:
        # Capture the entire screen
        monitor = sct.monitors[1]  # Use the primary monitor (change index if needed)
        screenshot = sct.grab(monitor)
        return screenshot

def benchmark_ocr_and_screenshot(iterations):
    ocr_times = []
    screenshot_times = []

    for i in range(iterations):
        # Time screenshot
        start_screenshot_time = time.time()
        screenshot = take_screenshot()
        end_screenshot_time = time.time()
        
        screenshot_time = end_screenshot_time - start_screenshot_time
        screenshot_times.append(screenshot_time)
        
        # Time OCR
        start_ocr_time = time.time()
        results = ocr.ocr(np.array(screenshot), cls=False)
        end_ocr_time = time.time()

        if SHOW_OCR_RESULTS:
            for idx in range(len(results)):
                res = results[idx]
                for line in res:
                    print(line)
        
        if VISUALIZE_OCR_RESULTS:
            # Draw OCR results on the screenshot
            image = Image.fromarray(np.array(screenshot)).convert("RGB") # Convert to RGB mode from screenshot
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype("./doc/fonts/simfang.ttf", size=20)  # Adjust size as needed

            # Process and draw results
            for res in results:
                for line in res:
                    box = [tuple(point) for point in line[0]]
                    # Finding the bounding box
                    box = [(min(point[0] for point in box), min(point[1] for point in box)),
                        (max(point[0] for point in box), max(point[1] for point in box))]
                    txt = line[1][0]
                    draw.rectangle(box, outline="red", width=2)  # Draw rectangle
                    draw.text((box[0][0], box[0][1] - 25), txt, fill="blue", font=font)  # Draw text above the box
            image.save("result.jpg")

        ocr_time = end_ocr_time - start_ocr_time
        ocr_times.append(ocr_time)

        print(f"Iteration {i + 1}: Screenshot time: {screenshot_time:.4f} seconds, OCR time: {ocr_time:.4f} seconds")
    
    # Print average times
    average_screenshot_time = sum(screenshot_times) / len(screenshot_times)
    average_ocr_time = sum(ocr_times) / len(ocr_times)
    print(f"Average screenshot time: {average_screenshot_time:.4f} seconds")
    print(f"Average OCR time: {average_ocr_time:.4f} seconds")

# Example usage
iterations = 10  # Number of iterations to run
benchmark_ocr_and_screenshot(iterations)
