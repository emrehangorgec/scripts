from pdf2image import convert_from_path
import os

pdf_path = input("PDF dosyasının tam yolunu girin: ")

output_dir = "output_images"
os.makedirs(output_dir, exist_ok=True)  

try:
    
    pages = convert_from_path(pdf_path, dpi=300)

    # Her bir sayfayı kaydet
    for i, page in enumerate(pages):
        output_filename = os.path.join(output_dir, f'page_{i + 1}.png')
        page.save(output_filename, 'PNG')
        print(f'{output_filename} kaydedildi.')

    print(f"Tüm görüntüler {output_dir} klasörüne başarıyla kaydedildi.")
except Exception as e:
    print(f"Hata oluştu: {e}")
