import os
import shutil


def merge_folders_continue_numbering(folder1, folder2):
    existing_files = [
        file
        for file in os.listdir(folder1)
        if os.path.isfile(os.path.join(folder1, file))
    ]
    max_number = 0
    for file in existing_files:
        try:
            number = int(os.path.splitext(file)[0])  # Dosya adından numarayı al
            max_number = max(max_number, number)
        except ValueError:
            pass  # Numara olmayan dosya adlarını atla

    # Klasör2'deki dosyaları Klasör1'e ekle ve yeniden adlandır
    for index, file_name in enumerate(os.listdir(folder2), start=max_number + 1):
        file_path = os.path.join(folder2, file_name)
        if os.path.isfile(file_path):  # Sadece dosyaları işle
            file_extension = os.path.splitext(file_name)[1]  # Dosya uzantısını koru
            new_name = f"{index}{file_extension}"
            destination_path = os.path.join(folder1, new_name)
            shutil.copy(file_path, destination_path)

    print(
        f"Klasör2'den {len(os.listdir(folder2))} dosya Klasör1'e {max_number + 1} ile başlayarak taşındı."
    )


def merge_folders_to_new_directory(folder1, folder2, destination_folder):
    # Yeni klasörü oluştur
    os.makedirs(destination_folder, exist_ok=True)

    # Mevcut dosyaları sırayla ekle
    current_index = 1  # Numara 1'den başlayacak
    for folder in [folder1, folder2]:
        for file_name in os.listdir(folder):
            file_path = os.path.join(folder, file_name)
            if os.path.isfile(file_path):  # Sadece dosyaları işle
                file_extension = os.path.splitext(file_name)[1]  # Dosya uzantısını koru
                new_name = f"{current_index}{file_extension}"
                destination_path = os.path.join(destination_folder, new_name)
                shutil.copy(file_path, destination_path)
                current_index += 1

    print(f"Tüm dosyalar {destination_folder} içinde birleştirildi ve sıralandı.")


folder1 = r"C:\Users\emrehan.gorgec\Desktop\Projects\computervision\scripts\sepetli_vinc_deneme"
folder2 = r"C:\Users\emrehan.gorgec\Desktop\Projects\computervision\scripts\bucket_truck_deneme"
destination_folder = (
    r"C:\Users\emrehan.gorgec\Desktop\Projects\computervision\scripts\merged_files"
)


# merge_folders_continue_numbering(folder1, folder2)
merge_folders_to_new_directory(folder1, folder2, destination_folder)
