import sys
import ctypes
import os

def main():
    if len(sys.argv) != 5:
        print("Usage: test_caesar.py <lib_path> <key> <input_file> <output_file>")
        sys.exit(1)

    lib_path   = sys.argv[1]  # путь к .so файлу
    key        = int(sys.argv[2])  # ключ (число или ASCII-код символа)
    input_file = sys.argv[3]
    output_file= sys.argv[4]

    # Динамическая загрузка библиотеки (не статическая линковка!)
    lib = ctypes.CDLL(os.path.abspath(lib_path))

    # Настройка сигнатур функций
    lib.set_key.argtypes = [ctypes.c_char]
    lib.set_key.restype  = None
    lib.caesar.argtypes  = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int]
    lib.caesar.restype   = None

    # Установка ключа
    lib.set_key(ctypes.c_char(key % 256))

    # Чтение входного файла
    with open(input_file, 'rb') as f:
        data = bytearray(f.read())

    length = len(data)
    src_buf = (ctypes.c_ubyte * length)(*data)
    dst_buf = (ctypes.c_ubyte * length)()

    # Шифрование
    lib.caesar(src_buf, dst_buf, length)

    # Запись результата
    with open(output_file, 'wb') as f:
        f.write(bytes(dst_buf))

    print(f"[OK] Зашифровано {length} байт -> {output_file}")

    # Проверка симметричности: XOR XOR = исходные данные
    dst2_buf = (ctypes.c_ubyte * length)()
    lib.caesar(dst_buf, dst2_buf, length)
    assert bytes(dst2_buf) == bytes(data), "ОШИБКА: двойное XOR не вернуло исходные данные!"
    print("[OK] Проверка двойного XOR пройдена успешно")

if __name__ == "__main__":
    main()
