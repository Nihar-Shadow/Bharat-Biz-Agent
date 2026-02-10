# ⚡ OCR Setup - Quick Start

## 🎯 Install Tesseract OCR

### **Windows (Recommended)**

#### **Option 1: Download Installer**
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run installer: `tesseract-ocr-w64-setup-5.3.3.exe`
3. Install to: `C:\Program Files\Tesseract-OCR`
4. ✅ Add to PATH during installation

#### **Option 2: Using Chocolatey**
```powershell
choco install tesseract
```

### **Verify Installation**
```powershell
tesseract --version
```

**Expected output:**
```
tesseract 5.3.3
```

---

## 🔧 Configure Python Path (If Needed)

If you get "tesseract not found" error:

1. Open: `c:\Nurothon\app\services\ocr_service.py`
2. Uncomment line 11:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

---

## 🚀 Test OCR

### **1. Start Backend**
```powershell
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### **2. Open Upload Page**
```
http://localhost:3000/bill-upload.html
```

### **3. Upload Test Image**
- Take photo of any bill/receipt
- Upload and click "Extract Products"
- See results!

---

## 📝 Create Test Bill

If you don't have a bill, create a simple text image:

```
RESTAURANT BILL
---------------
Burger    2x  ₹150
Pizza     1x  ₹450
Coke      3x  ₹50
---------------
Total:    ₹900
```

Save as image and upload!

---

## ✅ Quick Check

### **Backend Running?**
```
http://localhost:8000/docs
```
Look for `/ocr/upload-bill` endpoint

### **Frontend Running?**
```
http://localhost:3000/bill-upload.html
```
Should see upload interface

---

## 🚨 Troubleshooting

### **"Tesseract not found"**
```powershell
# Check if installed
tesseract --version

# If not found, add to PATH:
# 1. Search "Environment Variables"
# 2. Edit System PATH
# 3. Add: C:\Program Files\Tesseract-OCR
# 4. Restart terminal
```

### **"Failed to process image"**
- ✅ Check image is clear
- ✅ Try different image format
- ✅ Check file size < 10MB

### **"No items extracted"**
- ✅ Use clearer image
- ✅ Check bill has visible text
- ✅ Try printed receipt (not handwritten)

---

## 🎉 You're Ready!

Once Tesseract is installed:
1. ✅ Backend will auto-detect it
2. ✅ Upload any bill image
3. ✅ Get structured product data
4. ✅ Create orders instantly!

**Try it now:** `http://localhost:3000/bill-upload.html`
