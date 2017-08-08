from PIL import Image, ImageEnhance, ImageFilter
# from django.core.files.storage import default_storage as storage
import os
from va_blog.settings import MEDIA_ROOT
# from io import BytesIO
# from django.core.files.uploadedfile import InMemoryUploadedFile


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
        image_enhancer = ImageEnhance.Color(image)
        image_enhanced = image_enhancer.enhance(0.5)
        image_enhanced.show()
        return image_enhanced


# class ImageOperations:
#     def process_ratio(self, image, basewidth=None):
#         basewidth = 128 if basewidth is None else basewidth
#         filename_base, filename_ext = os.path.splitext(str(image))
#         thumb_path = "thumbnails/%s.jpg" % filename_base
#         if storage.exists(thumb_path):
#             print(thumb_path, " exists.")
#             return False
#         print("Image thumb path not found: ", thumb_path)
#         print("proceeding to start thumb processing")
#         try:
#             image_file = storage.open(str(image), 'r')
#             img = Image.open(image_file)
#         except OSError:
#             print("Image File does not exist", str(image))
#             return False
#         width, height = img.size

#         if width > height:
#             delta = width - height
#             left = int(delta/2)
#             upper = 0
#             right = height + left
#             lower = height
#         else:
#             delta = height - width
#             left = 0
#             upper = int(delta/2)
#             right = width
#             lower = width + upper

#         img = img.crop((left, upper, right, lower))
#         img = img.resize((128, 100), Image.ANTIALIAS)
#         img_io = BytesIO()
#         img = img.save(img_io, format="JPEG")
#         thumb_file = InMemoryUploadedFile(img_io, None, 'foo.jpg',
#                                           'image/jpeg', None, None)
#         storage.save("thumbnails/"+image.name, thumb_file)
#         return True

