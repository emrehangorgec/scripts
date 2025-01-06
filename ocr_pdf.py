from pdf2image import convert_from_path
import pytesseract
import os

pdf_path = input("PDF dosyasının tam yolunu girin: ")

output_dir = "extracted_images"
os.makedirs(output_dir, exist_ok=True)

try:
  
    pages = convert_from_path(pdf_path, dpi=300)

    full_text = ""

    
    for i, page in enumerate(pages):
      
        output_filename = os.path.join(output_dir, f'page_{i + 1}.png')
        page.save(output_filename, 'PNG')
        print(f'{output_filename} kaydedildi.')

        text = pytesseract.image_to_string(page, lang="eng")  
        full_text += f"Sayfa {i + 1}:\n{text}\n\n"

    with open("extracted_text.txt", "w", encoding="utf-8") as text_file:
        text_file.write(full_text)

    print("Metin başarıyla çıkarıldı ve 'extracted_text.txt' dosyasına kaydedildi.")

except Exception as e:
    print(f"Hata oluştu: {e}")
