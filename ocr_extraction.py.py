from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from doctr.utils.visualization import visualize_page
import os

# Load the PDF file
pdf_path = r'C:\fission_labs\project_assigned\Life Insurances-20240813T190456Z-001\sample\1\01 - Aditya Birla Sun Life.pdf'
document = DocumentFile.from_pdf(pdf_path)

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Initialize the OCR model
model = ocr_predictor(pretrained=True)

# Process the first page (you can loop through all pages if needed)
result = model(document[0])

# Export the OCR results with layout information
page_data = result.export()

# Separate text inside and outside tables
inside_table_text = []
outside_table_text = []

# A simple heuristic for distinguishing text inside and outside tables:
# Here, we'll assume text inside tables has smaller, closely packed bounding boxes
# This is just an example; you might need a more sophisticated approach

# Define a threshold for bounding box size or spacing
table_bbox_threshold = 0.05  # Adjust based on your document

# Iterate through the detected text blocks
for block in page_data['pages'][0]['blocks']:
    for line in block['lines']:
        for word in line['words']:
            text = word['value']
            bbox = word['geometry']  # Normalized [x_min, y_min, x_max, y_max]

            # Calculate the width and height of the bounding box
            bbox_width = bbox[2] - bbox[0]
            bbox_height = bbox[3] - bbox[1]

            # Simple heuristic: if the bounding box is small, assume it's inside a table
            if bbox_width < table_bbox_threshold and bbox_height < table_bbox_threshold:
                inside_table_text.append(text)
            else:
                outside_table_text.append(text)

# Output the results
print("Text Inside Tables:")
print("\n".join(inside_table_text))

print("\nText Outside Tables:")
print("\n".join(outside_table_text))

# Optional: Visualize the page with detected bounding boxes
visualize_page(result.pages[0])
