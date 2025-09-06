from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import cv2
import json
import os

processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
model = VisionEncoderDecoderModel.from_pretrained("./checkpoint-4350")    
    
def extract_text(image_uploaded, batch_dir):
    details=[]
    
    y_positions, segment_image = crop_image(image_uploaded)
    print(len(segment_image))
    recognized_text_list = []
    os.makedirs(batch_dir, exist_ok=True) 
    
    image_name = os.path.basename(image_uploaded)  
    image_base = os.path.splitext(image_name)[0]   

    subfolder = os.path.join(batch_dir, image_base)
    os.makedirs(subfolder, exist_ok=True)
    
    for idx, image in enumerate(segment_image):
        pixel_values = processor(images=image, return_tensors="pt").pixel_values
        generated_ids = model.generate(pixel_values)
        recognized_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        print(recognized_text)
        if recognized_text:
            recognized_text_list.append(recognized_text)
            cropped_filename = f"crop_{idx}.png"
            cv2.imwrite(os.path.join(subfolder, cropped_filename), image)
            result = {
                "cropped_image": f"{os.path.basename(batch_dir)}/{os.path.splitext(image_uploaded)[0]}/{cropped_filename}", 
                "generated_text": recognized_text
            }
            details.append(result)
            print(result)
    response = ""
    if recognized_text_list:
        response ="\n".join(recognized_text_list)
    return details , response
    
def crop_image(image_uploaded, min_height=40, horizontal_width=70):
    # 1. Load and preprocess
    img = cv2.imread(image_uploaded)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )
    
    # 2. Kernel tuned to detect very long horizontal lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_width, 1))
    detected_lines = cv2.morphologyEx(
        binary, cv2.MORPH_OPEN, horizontal_kernel, iterations=2
    )

    # 3. Find contours of detected lines
    contours, _ = cv2.findContours(
        detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # 4. Collect Y positions of horizontal lines
    y_positions = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w >= horizontal_width and h < 10:  # only wide & thin
            y_positions.append(y)

    # 5. Sort and deduplicate Y positions
    y_positions = sorted(list(set(y_positions)))

    # 6. Crop strips between consecutive lines if tall enough
    crops = []
    for i in range(len(y_positions) - 1):
        y_top = y_positions[i]
        y_bottom = y_positions[i + 1]
        region_height = y_bottom - y_top
        if region_height >= min_height:  # filter out tiny strips
            crop = img[y_top:y_bottom, :]
            crops.append(crop)
    return y_positions, crops