import itertools
import time

def main():
    coder = Coder()
    text = 'всім привіт '
    # text = 'тест'
    # encrypted_text = coder.encrypt('в', 'п', filepath='data.txt')
    # encrypted_text = coder.encrypt('ав', 'га', text=text)
    # coder.decrypt('тестове', 'слово', text=encrypted_text)
    # coder.brute_force(encrypted_text, text)
    # coder.test_encryption_decryption(100000)
    coder.test_brute_force(100000)

class Coder:
    """Клас для роботи з шифром Уітстона"""
    LETTERS = 'абв.гґдеє жзиіїйклм?ноп:рсту№фхцчш*щьюя0123456789'
    LENGTH = 7
    HEIGHT = 7

    def encrypt(self, keyword1: str, keyword2: str, text: str = None, filepath: str = None, toprint=True):
        """Функція проводить кодування заданого тексту шифром Уітстона з двома вхідними кодовими словами """
        if text is None and filepath is None:
            raise AttributeError('Помилка! Введіть значення тексту або шляху до файлу!')
        if text is None:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
        text = text.lower().replace('!', '.')
        if len(text) % 2:
            text += ' '

        first_square = self._form_square(keyword1)
        second_square = self._form_square(keyword2)
        if toprint:
            self._display_square(first_square, 'Перший квадрат (кодування)')
            self._display_square(second_square, 'Другий квадрат (кодування)')

        encrypted_text = ''
        for i in range(0, len(text), 2):
            first_letter, second_letter = text[i], text[i + 1]
            first_letter = first_letter if first_letter in self.LETTERS else '*'
            second_letter = second_letter if second_letter in self.LETTERS else '*'

            first_i, first_j = self._find_position(first_square, first_letter)
            second_i, second_j = self._find_position(second_square, second_letter)

            encrypted_text += second_square[first_i][second_j] + first_square[second_i][first_j]
        if toprint:
            print('\nЗакодований текст:')
            print(encrypted_text, "\n")
        return encrypted_text

    def decrypt(self, keyword1: str, keyword2: str, text: str = None, filepath: str = None, toprint=True):
        """Функція проводить декодування заданого тексту шифром Уітстона з двома вхідними кодовими словами """
        if text is None and filepath is None:
            raise AttributeError('Помилка! Введіть значення тексту або шляху до файлу!')
        if text is None:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
        if len(text) % 2:
            raise ValueError('Помилка! Некоректна довжина тексту для декодування!')

        text = text.lower()
        first_square = self._form_square(keyword1)
        second_square = self._form_square(keyword2)

        if toprint:
            self._display_square(first_square, 'Перший квадрат (декодування)')
            self._display_square(second_square, 'Другий квадрат (декодування)')

        decrypted_text = ''
        for i in range(0, len(text), 2):
            first_letter, second_letter = text[i], text[i + 1]
            first_letter = first_letter if first_letter in self.LETTERS else '*'
            second_letter = second_letter if second_letter in self.LETTERS else '*'

            first_i, first_j = self._find_position(second_square, first_letter)
            second_i, second_j = self._find_position(first_square, second_letter)

            decrypted_text += first_square[first_i][second_j] + second_square[second_i][first_j]

        if toprint:
            print('\nРозкодований текст:')
            print(decrypted_text, "\n")
        return decrypted_text

    def brute_force(self, encrypted_text: str, original_text: str, max_length: int = 10):
        """Функція атаки "грубою силою" для пошуку пари ключових слів для декодування заданого тексту"""
        fixed_original_text = original_text.replace('!', '.').lower()
        for i, char in enumerate(fixed_original_text):
            if char not in self.LETTERS:
                fixed_original_text = fixed_original_text[:i] + '*' + fixed_original_text[i+1:]
        for length in range(1, max_length + 1):
            for iteration, (kw1, kw2) in enumerate(itertools.product((''.join(p) for p in itertools.permutations(self.LETTERS, length)), repeat=2)):
                if iteration % 10000 == 0:
                    print(f'Ітерація: {iteration}, ключові слова: "{kw1}" - "{kw2}"')
                try:
                    decrypted_text = self.decrypt(kw1, kw2, text=encrypted_text, toprint=False)
                    if fixed_original_text in decrypted_text:
                        print(f'Знайдені ключові слова: {kw1}, {kw2}')
                        self._display_square(self._form_square(kw1), 'Лівий квадрат')
                        self._display_square(self._form_square(kw2), 'Правий квадрат')
                        return kw1, kw2
                except ValueError:
                    continue

        print('Не вийшло зламати')
        return None

    def test_encryption_decryption(self, max_text_size: int, max_kw_size: int = 49):
        """Функція для тестування часу кодування та декодування повідомлень в залежності від розміру тексту та розміру ключових слів"""
        text_result = ''
        text = 'Приклад тексту для перевірки шифру. Він містить лише українські літери, цифри 0123456789 та пробіли.'
        for i in range(100, max_text_size // len(text) + 1, 100):
            current_text = text * i
            tmp_encryption_result = []
            tmp_decryption_result = []
            text_result += str(len(current_text)) + ":\n"
            for j in range(1, max_kw_size + 1):
                kw1, kw2 = self.LETTERS[-j:], self.LETTERS[-j:][::-1]
                start_encrypt_time = time.time_ns()
                self.encrypt(kw1, kw2, text=current_text, toprint=False)
                start_decrypt_time = time.time_ns()
                self.decrypt(kw1, kw2, text=current_text, toprint=False)
                end_time = time.time_ns()
                tmp_encryption_result.append(str(start_decrypt_time - start_encrypt_time))
                tmp_decryption_result.append(str(end_time - start_decrypt_time))
            text_result += 'enc,' + ','.join(tmp_encryption_result) + '\n'
            text_result += 'dec,' + ','.join(tmp_decryption_result) + '\n'
            print(f'{len(current_text)}:')
            print(f'enc: {tmp_encryption_result}')
            print(f'dec: {tmp_decryption_result}')
        with open('results.txt', 'a') as f:
            f.write(text_result)

    def test_brute_force(self, max_text_size: int, max_kw_size: int = 3):
        """Функція для тестування часу атаки "грубою силою" в залежності від розмірів ключових слів"""
        text_result = ''
        text = 'приклад тексту для перевірки шифру. він містить лише українські літери  цифри 0123456789 та пробіли.'
        # text = 'абвггвб99523466754673452353452234проешащвмдльтіпоаа'
        for i in range(100, max_text_size // len(text) + 1, 100):
            current_text = text * i
            text_result += str(len(current_text)) + ":\n"
            for j in range(1, max_kw_size + 1):
                kw1 = self.LETTERS[-j:]
                for k in range(1, max_kw_size + 1):
                    kw2 = self.LETTERS[-k*2:-k:][::-1]
                    print(f'Задані ключові слова: {kw1}, {kw2}')
                    current_encrypted_text = self.encrypt(kw1, kw2, text=current_text, toprint=False)
                    start_bruteforce_time = time.time_ns()
                    kw1_found, kw2_found = self.brute_force(current_encrypted_text, current_text, max_length=3)
                    end_time = time.time_ns()
                    print(f'Знайдено: {kw1_found}, {kw2_found}, час: {str(end_time - start_bruteforce_time)}')
                    text_result += kw1 + '-' + kw2 + ' - ' + str(end_time - start_bruteforce_time) + '\n'
            text_result += '\n'
            print(f'{len(current_text)} зроблено')
        with open('results_brutforce.txt', 'a') as f:
            f.write(text_result)

    def _form_square(self, keyword: str):
        """Функція генерує квадрат за алгоритмом шифру Уітстона за заданим словом-клдючем"""
        letters_buf = self.LETTERS
        square = [[] for _ in range(self.HEIGHT)]

        for i in range(self.HEIGHT):
            for j in range(self.LENGTH):
                if keyword:
                    current_letter = keyword[0]
                    keyword = keyword.replace(current_letter, '')
                    if current_letter not in self.LETTERS:
                        continue
                    letters_buf = letters_buf.replace(current_letter, '')
                else:
                    current_letter = letters_buf[0]
                    letters_buf = letters_buf.replace(current_letter, '')

                square[i].append(current_letter)
        return square

    @staticmethod
    def _display_square(square, title: str):
        """Функція виводить квадрат за алгоритмом шифру Уітстона"""
        print(f'{title}:')
        for line in square:
            print(' '.join(line))

    @staticmethod
    def _find_position(square, letter):
        """Функція знаходить позицію по рядку та стовпцю букви у квадраті за алгоритмом шифру Уітстона"""
        for i, line in enumerate(square):
            if letter in line:
                return i, line.index(letter)
        return 0, 0


if __name__ == '__main__':
    main()

