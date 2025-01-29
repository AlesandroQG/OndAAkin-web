# mi_app/segment.py
import os
import numpy as np
import torch
import matplotlib.pyplot as plt
from PIL import Image
from sam2.utils.misc import variant_to_config_mapping
from sam2.build_sam import build_sam2
from sam2.automatic_mask_generator import SAM2AutomaticMaskGenerator

import io
import base64
from io import BytesIO
from django.http import HttpResponse
from django.http import JsonResponse

# Configuración del dispositivo para PyTorch
device = torch.device("cpu")
print(f"using device: {device}")
np.random.seed(3)

def show_anns(anns, borders=True):
    if len(anns) == 0:
        return
    sorted_anns = sorted(anns, key=(lambda x: x['area']), reverse=True)
    ax = plt.gca()
    ax.set_autoscale_on(False)

    img = np.ones((sorted_anns[0]['segmentation'].shape[0], sorted_anns[0]['segmentation'].shape[1], 4))
    img[:, :, 3] = 0
    for ann in sorted_anns:
        m = ann['segmentation']
        color_mask = np.concatenate([np.random.random(3), [0.5]])
        img[m] = color_mask
        if borders:
            import cv2
            contours, _ = cv2.findContours(m.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            contours = [cv2.approxPolyDP(contour, epsilon=0.01, closed=True) for contour in contours]
            cv2.drawContours(img, contours, -1, (0, 0, 1, 0.4), thickness=1)

    ax.imshow(img)
    

def segment_image(images):
#def segment_image():
    # Cargar la imagen
    #image = Image.open("C:/Users/maider/DesktopCiudad_jardin\ADAT\UD 7\OndAAkin\Image-Segmentation-API")
    #print(images)
    imagef = Image.open(io.BytesIO(images))
    image = np.array(imagef.convert("RGB"))
    
    # Generar las máscaras
    sam2_checkpoint = "/Users/alesandroquirosgobbato/segmentations/sam2_hiera_large.pt"
    model_cfg = "sam2.1_hiera_l.yaml"

    sam2 = build_sam2(
        variant_to_config_mapping["large"],
        sam2_checkpoint,
    )

    mask_generator = SAM2AutomaticMaskGenerator(sam2, pred_iou_thresh=0.7, stability_score_thresh=0.7, stability_score_offset=0.7)
    masks = mask_generator.generate(image)

    # Mostrar la segmentación
    plt.figure(figsize=(20, 20))
    plt.imshow(image)
    show_anns(masks)
    # Guardar el gráfico en un objeto de bytes
    buffer = BytesIO()
    plt.savefig(buffer, format="png")  # Guardar como imagen PNG
    buffer.seek(0)  # Volver al inicio del buffer

    # Obtener los bytes de la imagen
    image_bytes = buffer.getvalue()

    # Cerrar el buffer
    buffer.close()
    base64_string = base64.b64encode(image_bytes).decode("utf-8")
    return base64_string
    

    