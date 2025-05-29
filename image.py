import io
from PIL import Image


def compress_image(img_data, max_px_size, quality, encoding_type, algorithm, blur_radius):
    image = Image.open(io.BytesIO(img_data))
    w = float(image.size[0])
    h = float(image.size[1])
    if w < h:
        if w > max_px_size:
            new_w = max_px_size
            scale = max_px_size / w
            new_h = h * scale
        else:
            new_h = h
            new_w = w
    else:
        if h > max_px_size:
            new_h = max_px_size
            scale = max_px_size / h
            new_w = w * scale
        else:
            new_h = h
            new_w = w

    if blur_radius == 0:
        blurred_image = image
    else:
        blurred_image = image.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        
    if algorithm == 'BOX':
        re_image = blurred_image.resize((int(new_w), int(new_h)), Image.Resampling.BOX)
    else if algorithm == 'BILINEAR':
        re_image = blurred_image.resize((int(new_w), int(new_h)), Image.Resampling.BILINEAR)
    else if algorithm == 'BICUBIC':
        re_image = blurred_image.resize((int(new_w), int(new_h)), Image.Resampling.BICUBIC)
    else if algorithm == 'HAMMING':
        re_image = blurred_image.resize((int(new_w), int(new_h)), Image.Resampling.HAMMING)
    else if algorithm == 'NEAREST':
        re_image = blurred_image.resize((int(new_w), int(new_h)), Image.Resampling.NEAREST)
    else if algorithm == 'LANCZOS':
        re_image = blurred_image.resize((int(new_w), int(new_h)), Image.Resampling.LANCZOS)
    else:
        re_image = blurred_image.resize((int(new_w), int(new_h)), Image.Resampling.BILINEAR)

    buf = io.BytesIO()

    if encoding_type == 'WebP':
        re_image.save(buf, format='webp', quality=quality)
    elif encoding_type == 'JPEG':
        re_image.convert('RGB').save(buf, format='jpeg', quality=quality)
    elif encoding_type == 'PNG':
        re_image.save(buf, format='PNG', quality=quality)
    else:
        re_image.save(buf, format=image.format, quality=quality)

    return buf.getvalue()
