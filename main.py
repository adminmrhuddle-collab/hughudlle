from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from huggingface_hub import HfApi
import os
import shutil
from pathlib import Path

app = FastAPI()

# السماح لتطبيق Flutter بالتواصل مع الخدمة
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # في الإنتاج، حدد domain تطبيقك
    allow_methods=["*"],
    allow_headers=["*"],
)

# التوكن يجب أن يكون في متغير بيئة (آمن)
HF_TOKEN = os.getenv("HF_TOKEN")
REPO_ID = "mrhudlle/mr-huddle-images"  # تأكد من صحة الاسم

api = HfApi()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    temp_path = None
    try:
        # حفظ الملف مؤقتاً على الخادم
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # رفع الملف عبر المكتبة الرسمية
        api.upload_file(
            path_or_fileobj=temp_path,
            path_in_repo=file.filename,
            repo_id=REPO_ID,
            repo_type="dataset",
            token=HF_TOKEN
        )
        
        return {"success": True, "message": f"تم رفع {file.filename}"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # حذف الملف المؤقت بعد الرفع
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)