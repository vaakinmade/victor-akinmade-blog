from PIL import Image, ImageEnhance, ImageFilter
from va_blog.settings import MEDIA_ROOT
import os


class PageTitleMixin:
    page_title = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

class ImageOperationMixin:
    
    def get_image(self, img):
        image_path = os.path.join(MEDIA_ROOT, img)
        try:
            image = Image.open(image_path)
        except OSError:
            return None
        return image

    def enhance(self, img):
        image = self.get_image(img)
        if image is None:
            return img
        image_enhancer = ImageEnhance.Contrast(image)
        image_enhanced = image_enhancer.enhance(1.3)
        #image_enhanced.show("30% More Contrast")
        image_enhanced.save(MEDIA_ROOT+'/'+img)
        return image_enhanced