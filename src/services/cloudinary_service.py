import cloudinary
import cloudinary.uploader
from src.conf.config import settings

cloudinary.config(
    cloud_name=settings.cloudinary_cloud_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret
)

def upload_avatar(image_path: str) -> str:
    try:
        response = cloudinary.uploader.upload(image_path, folder="user_avatars")
        return response['secure_url']
    except Exception as e:
        raise Exception(f"Error uploading avatar: {str(e)}")
