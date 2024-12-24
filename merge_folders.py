import os
import shutil


def get_max_file_number(folder):
    """
    Belirtilen klasördeki dosya isimlerinden en büyük sayıyı alır.
    """
    max_number = 0
    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        if os.path.isfile(file_path):
            try:
                number = int(os.path.splitext(file_name)[0])
                max_number = max(max_number, number)
            except ValueError:
                pass  # Numara içermeyen dosya isimlerini atla
    return max_number


def copy_and_rename_files(source_folder, destination_folder, start_index=1):
    """
    Belirtilen klasördeki dosyaları başka bir klasöre taşır ve yeni isimlerle yeniden adlandırır.
    """
    os.makedirs(destination_folder, exist_ok=True)
    current_index = start_index

    for file_name in os.listdir(source_folder):
        file_path = os.path.join(source_folder, file_name)
        if os.path.isfile(file_path):
            file_extension = os.path.splitext(file_name)[1]  # Uzantıyı koru
            new_name = f"{current_index}{file_extension}"
            destination_path = os.path.join(destination_folder, new_name)
            shutil.copy(file_path, destination_path)
            current_index += 1

    return current_index  # Son kullanılan numarayı döndür


def merge_folders_continue_numbering(folder1, folder2):
    """
    İki klasörü birleştirir ve ikinci klasörün dosyalarını ilk klasörde numara devam ettirerek ekler.
    """
    max_number = get_max_file_number(folder1)
    copy_and_rename_files(folder2, folder1, start_index=max_number + 1)
    print(f"{folder2} dosyaları {folder1} içerisine birleştirildi.")


def merge_folders_to_new_directory(folder1, folder2, destination_folder):
    """
    İki klasörü yeni bir klasörde birleştirir ve tüm dosyaları sırayla yeniden adlandırır.
    """
    next_index = copy_and_rename_files(folder1, destination_folder, start_index=1)
    copy_and_rename_files(folder2, destination_folder, start_index=next_index)
    print(
        f"{folder1} ve {folder2} klasörleri {destination_folder} içinde birleştirildi."
    )


# Kullanım
if __name__ == "__main__":
    folder1 = r"C:\Users\emrehan.gorgec\Desktop\Projects\computervision\scripts\sepetli_vinc_deneme"
    folder2 = r"C:\Users\emrehan.gorgec\Desktop\Projects\computervision\scripts\bucket_truck_deneme"
    destination_folder = (
        r"C:\Users\emrehan.gorgec\Desktop\Projects\computervision\scripts\merged_files"
    )

    # Birinci ve ikinci klasörü yeni bir klasörde birleştir
    merge_folders_to_new_directory(folder1, folder2, destination_folder)

    # İkinci klasörü birinci klasör içine numaraları devam ettirerek ekle
    # merge_folders_continue_numbering(folder1, folder2)
