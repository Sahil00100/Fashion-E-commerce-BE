# your_app/management/commands/reduce_image_quality.py

from django.core.management.base import BaseCommand
from PIL import Image
from api.models  import ProductImages  # Import your actual model

class Command(BaseCommand):
    help = 'Reduce image quality for all existing images'

    def handle(self, *args, **options):
        # Fetch all existing images
        images = ProductImages.objects.all()

        for image in images:
            try:
                # Open the original image
                original_image = Image.open(image.image.path)

                # Set the quality (adjust as needed)
                quality = 80

                # Save the image with adjusted quality
                original_image.save(image.image.path, quality=quality)

                self.stdout.write(self.style.SUCCESS(f'Successfully processed image: {image.image.name}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing image {image.image.name}: {str(e)}'))
