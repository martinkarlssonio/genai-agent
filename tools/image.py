"""
This tool uses the Hugging Face Blip Image Captioning model to generate a description of an image.
"""

def analyzeImage(img_url: str) -> dict:
    try:
        import torch
        from transformers import BlipProcessor, BlipForConditionalGeneration


        # specify model to be used
        hf_model = "Salesforce/blip-image-captioning-large"
        # use GPU if it's available
        device = 'cuda' if torch.cuda.is_available() else 'cpu'

        # preprocessor will prepare images for the model
        processor = BlipProcessor.from_pretrained(hf_model)
        # then we initialize the model itself
        model = BlipForConditionalGeneration.from_pretrained(hf_model).to(device)
                                                                        
        import requests
        from PIL import Image

        image = Image.open(requests.get(img_url, stream=True).raw).convert('RGB')
        image

        # unconditional image captioning
        inputs = processor(image, return_tensors="pt").to(device)

        out = model.generate(**inputs, max_new_tokens=20)
        image_description = processor.decode(out[0], skip_special_tokens=True)
        print("analyzeImage - Image Description: ", image_description)
        return {"image_description":image_description}
    except Exception as e:
        return str(e)