from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from openai import OpenAI
import os
from PIL import Image
import io
import base64

load_dotenv()

app = FastAPI(
    title="Cat Travel API",
    description="API for generating cat travel photos",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client with proper configuration
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.openai.com/v1"
)

@app.get("/")
async def root():
    """Root endpoint that returns API information."""
    return {
        "message": "Welcome to Cat Travel API",
        "version": "1.0.0",
        "endpoints": {
            "/process-image": "POST - Process a cat image and generate a travel photo"
        }
    }

async def analyze_cat_image(image_data):
    """使用GPT-4 Vision分析猫咪图片，识别品种、颜色和身材特征"""
    try:
        # 将图像转换为base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        # 调用OpenAI的vision模型
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Analyze this cat image and describe its features in detail. Include: breed (if recognizable), fur color and pattern, eye color, body type (slim/chubby), face shape, and any distinctive markings. If you're uncertain about any feature, make your best educated guess based on what you can see. Respond in English with a detailed description that could help recreate this cat in an image."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )
        
        # 提取返回的描述
        cat_description = response.choices[0].message.content.strip()
        
        # 检查是否返回有用的描述
        if "sorry" in cat_description.lower() or "can't" in cat_description.lower() or "cannot" in cat_description.lower():
            # 分析图片获取基本信息
            cat_image = Image.open(io.BytesIO(image_data))
            width, height = cat_image.size
            
            # 创建一个基本描述
            fallback_description = "a cat with distinctive features from the uploaded image"
            print(f"Using fallback cat description: {fallback_description}")
            return fallback_description
            
        print(f"Cat analysis result: {cat_description}")
        return cat_description
    
    except Exception as e:
        print(f"Error analyzing cat image: {str(e)}")
        return "a cat with distinctive features from the uploaded image"

@app.post("/process-image")
async def process_image(
    file: UploadFile = File(...),
    location: str = Form(...)
):
    try:
        # 读取上传的猫图片
        contents = await file.read()
        cat_image = Image.open(io.BytesIO(contents))
        
        # 检查文件格式
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ['.jpg', '.jpeg', '.png']:
            raise HTTPException(status_code=400, detail="Only JPG, JPEG, and PNG formats are supported")
        
        # 分析猫咪特征
        cat_features = await analyze_cat_image(contents)
        
        # 构建更详细的prompt，包含猫咪具体特征
        prompt = f"""Create a photorealistic image that looks like a selfie accidentally taken by a real cat at night, using a phone camera. The cat should be physically present in the environment, naturally lit by the surrounding light sources. 
                    The cat has these specific features: {cat_features}. Make sure these exact features are clearly visible in the generated image.
                    The cat should be very close to the lens, slightly off-center, mid-meow or smiling. The framing should be awkward, with subtle motion blur, a bit of grain/noise, and minor wide-angle distortion — all common in low-light mobile phone photography. The background is {location} at night, and the lighting on the cat should match the ambient lighting of the scene. 
                    The image should be look like a real photo, not look like edited or synthetic."""
                            
        try:
            print(f"Generating image with prompt: {prompt[:100]}...")
            
            # 使用text-to-image生成
            response = client.images.generate(
                model="dall-e-3",  # 使用最新的DALL-E 3模型
                prompt=prompt,
                n=1,
                size="1024x1024",
                quality="hd",  # 使用高清质量
                style="natural"  # 使用自然风格
            )
            
            # 返回生成的图片URL
            return {"image_url": response.data[0].url}
        except Exception as e:
            print(f"Error calling OpenAI API: {str(e)}")
            # 打印更多的错误细节
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Error generating image with OpenAI: {str(e)}")
            
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
