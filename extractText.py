from paddleocr import PaddleOCR

# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `fr`, `german`, `korean`, `japan`
# to switch the language model in order.
ocr = PaddleOCR(use_angle_cls=True, rec_algorithm='SVTR_LCNet') # need to run only once to download and load model into memory
img_path = 'test_image1.png'
result = ocr.ocr(img_path, cls=True)
# for line in result:
#   print(line)
print(result[0][0][1][0])