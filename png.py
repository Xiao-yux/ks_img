import base64
from io import BytesIO
from PIL import Image
from pathlib import Path
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.ocr.v20181119 import ocr_client, models

def ocr_recognize(image_path):
    secretId = ""  #your_secret_id
    secretKey = "" #your_secret_key
    
    cred = credential.Credential(secretId, secretKey)
    httpProfile = HttpProfile()
    httpProfile.endpoint = "ocr.tencentcloudapi.com"  

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = ocr_client.OcrClient(cred, "ap-guangzhou", clientProfile)  

    img = Image.open(image_path)
    width, height = img.size

    left = 0
    top = height * 0.90  
    right = width
    bottom = height

    img_cropped = img.crop((left, top, right, bottom))
    buffered = BytesIO()
    img_cropped.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    req = models.GeneralBasicOCRRequest()
    req.ImageBase64 = img_str
    resp = client.GeneralBasicOCR(req)

    result = [item.DetectedText for item in resp.TextDetections]
    return result, img_str


# if __name__ == "__main__":
#     P = Path("./img")
#     for file in P.iterdir():
#         if file.is_file():
#             result, img_str = ocr_recognize(file)
#             print(result)