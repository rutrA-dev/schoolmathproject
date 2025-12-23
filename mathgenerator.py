import random
import re
from sympy import symbols, expand, latex, Eq, Rational, sqrt, simplify, solve, log, Abs as sympy_abs, sin, cos, tan, pi, rad, deg, solve, S
class EquationGenerator:
    def __init__(self):
        self.x = symbols('x', real=True)

    def _format_latex(self, expr_str):
        return rf"$${expr_str}$$"
    def diff(self, d):
        if d == 1: return "легкая"
        elif d == 2: return "средняя"
        elif d == 3: return "сложная"
    def generate_quadratic(self, d):
        x = self.x
        if d == 1: difficulty = random.choice([1,2])
        elif d == 2: difficulty = random.choice([3,4])
        elif d == 3: difficulty = 5

        # Переменные для корней и коэффициентов
        roots = []
        equation_expr = None
        
        # --- УРОВЕНЬ 1: Неполные квадратные уравнения (вида x^2 = a или x^2 - a = 0) ---
        if difficulty == 1:
            # Корни: симметричные целые числа (например, 3 и -3)
            root = random.randint(1, 20)
            roots = [root, -root]
            a = random.randint(1,2)
            # Уравнение: x^2 - root^2 = 0
            equation_expr = a * (x**2 - root**2)

        # --- УРОВЕНЬ 2: Приведенные уравнения (a=1) с малыми целыми корнями ---
        elif difficulty == 2:
            # Корни: целые числа от -10 до 10
            r1 = random.randint(-10, 10)
            r2 = random.randint(-10, 10)
            roots = [r1, r2]
            
            # Уравнение: (x - r1)(x - r2)
            equation_expr = expand((x - r1) * (x - r2))

        # --- УРОВЕНЬ 3: Приведенные (a=1) но с большими числами ИЛИ a=-1 ---
        elif difficulty == 3:
            # Корни: целые числа от -20 до 20, исключая слишком простые
            r1 = random.choice([i for i in range(-20, 21) if abs(i) > 5])
            r2 = random.randint(-10, 10)
            roots = [r1, r2]
            
            # С вероятностью 30% делаем параболу ветвями вниз (умножаем на -1)
            coef = -1 if random.random() < 0.5 else 1
            equation_expr = expand(coef * (x - r1) * (x - r2))

        # --- УРОВЕНЬ 4: Неприведенные (a > 1), но корни всё еще целые ---
        elif difficulty == 4:
            # Корни: целые числа
            r1 = random.randint(-20, 20)
            r2 = random.randint(-20, 20)
            roots = [r1, r2]
            
            # Коэффициент 'a' случайный (2, 3, 4, 5, -2...)
            a = random.choice([6, 2, 3, 4, 5, -2, -3, -4,-5, -6])
            
            # Уравнение: a(x - r1)(x - r2)
            # Пример: 2(x-1)(x-3) -> 2x^2 - 8x + 6 = 0
            equation_expr = expand(a * (x - r1) * (x - r2))

        # --- УРОВЕНЬ 5: Дробные корни (десятичные), высокие коэффициенты ---
        elif difficulty == 5:
            # Чтобы получить "хорошие" десятичные дроби (0.5, 0.25, 0.2),
            # знаменатели должны быть степенями 2 или 5.
            denominators = [1, 2, 4, 5, 8, 10] 
            
            # Генерируем рациональные корни
            # Rational(число, знаменатель) создает точную дробь в SymPy
            d1 = random.choice(denominators)
            n1 = random.randint(-50, 50)
            
            d2 = random.choice(denominators)
            n2 = random.randint(-50, 50)
            
            # Исключаем случай, когда оба корня целые (это уровень 4)
            while d1 == 1 and d2 == 1:
                d2 = random.choice([2, 4, 5])

            r1 = Rational(n1, d1)
            r2 = Rational(n2, d2)
            
            roots = [float(r1), float(r2)] # Конвертируем в float для ответа (например 0.5)

            # ХИТРОСТЬ: Чтобы уравнение выглядело красиво (целые коэффициенты),
            # мы формируем его как (d1*x - n1)(d2*x - n2) = 0
            # Пример: корни 0.5 и 3 -> (2x - 1)(x - 3) -> 2x^2 - 7x + 3 = 0
            term1 = (d1 * x - n1)
            term2 = (d2 * x - n2)
            
            # Иногда добавляем общий множитель для сложности
            multiplier = random.choice([1, -1, 2])
            equation_expr = expand(multiplier * term1 * term2)

        # --- ФИНАЛЬНАЯ СБОРКА ---
        
        # Сортируем ответы для удобства проверки
        roots.sort()
        
        # Формируем LaTeX. Eq(expr, 0) создает запись "= 0"
        latex_problem = latex(equation_expr) + " = 0"
        
        return {
            "type": "quadratic",
            "type_russian": "квадратное уравнение",
            "question_latex": self._format_latex(latex_problem),
            "answers": roots, 
            "complexity": self.diff(d),
            "difficulty": d
        }



    def generate_biquadratic(self, d):
        x = self.x
        if d == 1: difficulty = random.choice([1,2])
        elif d == 2: difficulty = random.choice([3,4])
        elif d == 3: difficulty = 5
        # Мы генерируем корни для t (где t = x^2)
        # Важно: чтобы были вещественные корни x, t должно быть >= 0
        t_roots = []
        
        # --- УРОВЕНЬ 1: Простейшие (x^4 - a = 0) ---
        # Решается как x^2 = sqrt(a)
        if difficulty == 1:
            # Берем t1 как квадрат целого числа (например, 4, 9, 16)
            base = random.randint(1, 10)
            t1 = base**2  # t1 = 4
            # Уравнение (t - t1) = 0 => x^2 - 4 = 0 => x^4 - 8x^2 + 16 = 0 (нет, это сложно)
            # Проще: x^4 - t1^2 = 0 не совсем биквадратное. 
            # Сделаем (x^2 - t1) = 0
            equation_expr = x**4 - t1**2 
            # Корни будут x = sqrt(t1) и x = -sqrt(t1)
            # Но для биквадратного классического вида:
            roots = [float(base), float(-base)]
            equation_expr = x**4 - t1**2 # x^4 - 16 = 0

        # --- УРОВЕНЬ 2: Два целых корня x (один t положительный, другой отрицательный) ---
        # Пример: (t - 4)(t + 5) = 0  => t=4 (x=±2) и t=-5 (корней нет)
        elif difficulty == 2:
            r_base = random.randint(1, 5)
            t1 = r_base**2 # Положительный t
            t2 = -random.randint(1, 5) # Отрицательный t (не даст корней x)
            
            roots = [float(r_base), float(-r_base)]
            # (x^2 - t1)(x^2 - t2)
            equation_expr = expand((x**2 - t1) * (x**2 - t2))

        # --- УРОВЕНЬ 3: Четыре целых корня x ---
        # Пример: (t - 4)(t - 9) = 0 => x = ±2, ±3
        elif difficulty == 3:
            b1 = random.randint(1, 5)
            b2 = random.randint(1, 5)
            while b1 == b2: b2 = random.randint(1, 5)
            a = random.choice([-2, -1, 1, 2])
            t1, t2 = b1**2, b2**2
            roots = [float(b1), float(-b1), float(b2), float(-b2)]
            equation_expr = expand(a * (x**2 - t1) * (x**2 - t2))

        # --- УРОВЕНЬ 4: Неприведенное (a > 1) и/или отсутствие корней ---
        # Тип А: 2x^4 - 10x^2 + 8 = 0
        # Тип B: x^4 + 5x^2 + 4 = 0 (корней нет, так как t1, t2 < 0)
        elif difficulty == 4:
            no_roots = random.random() < 0.1
            if no_roots:
                t1, t2 = -random.randint(1, 10), -random.randint(11, 20)
                roots = []
                equation_expr = expand((x**2 - t1) * (x**2 - t2))
            else:
                a = random.choice([2, 3])
                b1, b2 = random.randint(1, 10), random.randint(1, 11)
                roots = [float(b1), float(-b1), float(b2), float(-b2)]
                equation_expr = expand(a * (x**2 - b1**2) * (x**2 - b2**2))

        # --- УРОВЕНЬ 5: Дробные корни x ---
        # Пример: x^2 = 1/4 и x^2 = 9 => x = ±0.5, ±3
        elif difficulty == 5:
            # t1 = 1/4 (x = ±0.5), t2 = случайное целое
            d1 = random.choice([2, 5, 4, 8, 10]) # Чтобы были красивые десятичные 0.5 или 0.2
            t1 = Rational(1, d1**2)
            t2 = random.randint(1, 4)**2
            
            roots = [float(1/d1), float(-1/d1), float(sqrt(t2)), float(-sqrt(t2))]
            
            # Формируем уравнение с целыми коэффициентами: (d1^2 * x^2 - 1)(x^2 - t2)
            equation_expr = expand((d1**2 * x**2 - 1) * (x**2 - t2))

        # Финализация
        unique_roots = sorted(list(set(roots)))
        latex_problem = latex(equation_expr) + " = 0"
        
        return {
            "type": "biquadratic",
            "type_russian": "биквадратное уравнение",
            "question_latex": self._format_latex(latex_problem),
            "answers": unique_roots,
            "complexity": self.diff(d),
            "difficulty": d
        }



    def generate_cubic(self, d):
        if d == 1: difficulty = random.choice([1,2])
        elif d == 2: difficulty = random.choice([3,4])
        elif d == 3: difficulty = 5
        x = self.x
        
        roots = []
        equation_expr = None
        
        # --- УРОВЕНЬ 1: Вынесение за скобки (Неполные кубические) ---
        # Тип: x(x^2 - a^2) = 0  => x(x-a)(x+a) = 0
        # Решается вынесением x, а потом как квадратное
        if difficulty == 1:
            # Один корень всегда 0
            r_val = random.randint(1, 10)
            roots = [0, r_val, -r_val]
            
            # Уравнение вида x^3 - n*x = 0
            equation_expr = x * (x - r_val) * (x + r_val)
            equation_expr = expand(equation_expr)

        # --- УРОВЕНЬ 2: Метод группировки (легкий) ---
        # Тип: x^2(x - a) - b^2(x - a) = 0
        # Корни: a, b, -b. Коэффициенты небольшие.
        elif difficulty == 2:
            a = random.randint(-5, 5)
            b = random.randint(1, 5)
            # Исключаем совпадения, чтобы не упростилось слишком сильно
            while a == b or a == -b or a == 0:
                a = random.randint(-5, 5)
                
            roots = [a, b, -b]
            
            # Формируем: (x - a)(x^2 - b^2)
            # SymPy сам раскроет это в x^3 - a*x^2 - b^2*x + a*b^2
            equation_expr = expand((x - a) * (x - b) * (x + b))

        # --- УРОВЕНЬ 3: Стандартные целые корни (Подбор корня) ---
        # Тип: (x - r1)(x - r2)(x - r3) = 0
        # Ученику нужно найти один корень подбором (среди делителей свободного члена),
        # а потом поделить столбиком или схемой Горнера.
        elif difficulty == 3:
            # Генерируем 3 случайных целых корня
            r1 = random.randint(-10, 10)
            r2 = random.randint(-10, 10)
            r3 = random.randint(-10, 10)
            a = random.choice([-1,2,3,-2,-3])
            roots = [r1, r2, r3]
            equation_expr = expand(a * (x - r1) * (x - r2) * (x - r3))

        # --- УРОВЕНЬ 4: Кратные корни или коэффициент при старшей степени ---
        # Тип A: (x - a)^2 * (x - b) = 0 (Два корня совпадают, график касается оси X)
        # Тип B: 2x^3 + ... (Коэффициент a != 1)
        elif difficulty == 4:
            is_multiple_root = random.choice([True, False])
            
            if is_multiple_root:
                # Кратные корни
                r1 = random.randint(-20, 20)
                r2 = random.randint(-20, 20)
                while r1 == r2: r2 = random.randint(-20, 20)
                a = random.choice([-3, 2, -1, -2, 3])
                roots = [r1, r1, r2] # r1 встречается дважды
                equation_expr = expand(a * (x - r1)**2 * (x - r2))
            else:
                # Старший коэффициент > 1 (но корни все еще целые)
                coef = random.choice([2, 3, -1])
                r1 = random.randint(-4, 4)
                r2 = random.randint(-4, 4)
                r3 = random.randint(-4, 4)
                
                roots = [r1, r2, r3]
                equation_expr = expand(coef * (x - r1) * (x - r2) * (x - r3))

        # --- УРОВЕНЬ 5: Дробные корни (Метод "переброски" или сложный подбор) ---
        # Хотя бы один корень дробный (0.5, 1.5, 0.2 и т.д.)
        elif difficulty == 5:
            denominators = [2, 4, 5]
            
            # Генерируем 1 сложный дробный корень и 2 простых целых
            # Или 2 дробных. Сделаем микс.
            
            # Корень 1 (Дробь)
            d1 = random.choice(denominators)
            n1 = random.choice([i for i in range(-10, 11) if i % d1 != 0])
            
            # Корень 2 (Целое)
            d2 = 1
            n2 = random.randint(-20, 20)
            
            # Корень 3 (Может быть дробным или целым)
            d3 = random.choice([1, 2, 4, 5, 8, 10])
            n3 = random.randint(-20, 20)
            
            roots = [float(n1/d1), float(n2/d2), float(n3/d3)]
            
            # Собираем скобки: (d*x - n)
            term1 = (d1 * x - n1)
            term2 = (d2 * x - n2)
            term3 = (d3 * x - n3)
            
            equation_expr = expand(term1 * term2 * term3)

        # --- ФИНАЛИЗАЦИЯ ---
        
        # Убираем дубликаты из ответов для проверки (set), затем сортируем
        # Важно: для проверки ответа "множество корней" дубли не нужны,
        # но если ты хочешь проверять кратность, то оставь как есть.
        # Обычно в вебе проверяют уникальные корни.
        unique_roots = sorted(list(set(roots)))
        
        latex_problem = latex(equation_expr) + " = 0"

        return {
            "type": "biquadratic",
            "type_russian": "кубическое уравнение",
            "question_latex": self._format_latex(latex_problem),
            "answers": unique_roots, # Для проверки (например [-2.0, 0.0, 2.0])
            "complexity": self.diff(d),
            "difficulty": d,
            "debug_all_roots": roots # Полный список корней (для отладки)
        }



    def generate_higher_degree(self, d):
        if d == 1: difficulty = random.choice([1,2])
        elif d == 2: difficulty = random.choice([3,4])
        elif d == 3: difficulty = 5
        x = self.x
        roots = []
        equation_expr = None
        degree = 3 # По умолчанию

        # --- УРОВЕНЬ 1: Вынесение x^n за скобки ---
        # Тип: x^3 - a*x^2 = 0 или x^4 + a*x^3 = 0
        if difficulty == 1:
            degree = random.choice([3, 4, 5, 6])
            r1 = random.randint(-20, 20)
            # Уравнение: x^{n-1}(x - r1) = 0
            roots = [0, r1]
            equation_expr = expand(x**(degree-1) * (x - r1))

        # --- УРОВЕНЬ 2: Группировка (4 слагаемых) ---
        # Тип: x^3 + ax^2 + bx + c = 0, где можно сгруппировать попарно
        elif difficulty == 2:
            degree = 3
            # (x - r1)(x^2 - a^2) -> три целых корня
            r1 = random.randint(-5, 5)
            a = random.randint(1, 6)
            roots = [r1, a, -a]
            equation_expr = expand((x - r1) * (x**2 - a**2))

        # --- УРОВЕНЬ 3: Степень 4, сводящаяся к произведению двух квадратов ---
        # Тип: (x^2 - a)(x^2 - b) = 0, где a или b не являются полными квадратами (но корни красивые)
        # Или просто 4 целых корня через разложение
        elif difficulty == 3:
            degree = 4
            r_list = random.sample(range(-5, 6), 3) # 3 разных корня
            r_list.append(random.choice(r_list)) # Один корень сделаем кратным
            roots = list(set(r_list))
            equation_expr = expand((x - r_list[0])*(x - r_list[1])*(x - r_list[2])*(x - r_list[3]))

        # --- УРОВЕНЬ 4: Теорема Безу (Целые корни, большой свободный член) ---
        # Тип: x^3 + ax^2 + bx + c = 0. Ученик должен проверить делители 'c'.
        elif difficulty == 4:
            degree = 3
            # Генерируем корни так, чтобы свободный член был "неудобным" (много делителей)
            roots = [random.randint(-4, 4) for _ in range(3)]
            # Добавляем коэффициент перед x^3
            a = random.choice([1, 2, -1])
            equation_expr = expand(a * (x - roots[0]) * (x - roots[1]) * (x - roots[2]))

        # --- УРОВЕНЬ 5: Высокая степень (n=5 или 6) или дробные корни ---
        elif difficulty == 5:
            degree = random.choice([3, 4, 5, 6, 7])
            # Смесь целых и одного дробного корня (0.5 или -0.5)
            d = 2
            n = random.choice([-3, -1, 1, 3])
            r_frac = n/d
            
            simple_roots = random.sample(range(-3, 4), degree - 1)
            roots = simple_roots + [r_frac]
            a = random.choice([-1,1])
            # Формируем через (2x - n) для красоты коэффициентов
            expr = (a*x - n)
            for r in simple_roots:
                expr *= (x - r)
            equation_expr = expand(expr)

        # Финализация
        unique_roots = sorted(list(set([float(r) for r in roots])))
        latex_problem = latex(equation_expr) + " = 0"
        
        return {
            "type": "higher",
            "type_russian": "уравнение высшей степени",
            "question_latex": self._format_latex(latex_problem),
            "answers": unique_roots,
            "complexity": self.diff(d),
            "difficulty": d
        }


    def generate_rational(self, d):
        if d == 1: difficulty = random.choice([1,2])
        elif d == 2: difficulty = random.choice([3,4])
        elif d == 3: difficulty = random.choice([5,6])
        x = self.x
        
        # Идея: (x - r1)(x - r2) / (x - r_forbidden) = 0
        # Числитель дает корни, знаменатель создает ОДЗ
        
        roots = []
        forbidden_roots = []
        
        # --- УРОВЕНЬ 1: Простейшие (Линейный числитель и знаменатель) ---
        # Тип: (x - a) / (x - b) = 0. Корень один: a.
        if difficulty == 1:
            r1 = random.randint(-30, 30)
            forbidden = random.randint(-30, 30)
            while r1 == forbidden:
                forbidden = random.randint(-30, 30)
                
            numerator = x - r1
            denominator = x - forbidden
            roots = [r1]

        # --- УРОВЕНЬ 2: Квадратный числитель, два целых корня ---
        # Тип: (x^2 + bx + c) / (x - d) = 0
        elif difficulty == 2:
            r1 = random.randint(-10, 10)
            r2 = random.randint(-10, 10)
            forbidden = random.randint(-10, 10)
            # Гарантируем, что ОДЗ не совпадает с корнями
            while forbidden in [r1, r2]:
                forbidden = random.randint(-10, 10)
                
            numerator = expand((x - r1) * (x - r2))
            denominator = x - forbidden
            roots = [r1, r2]

        # --- УРОВЕНЬ 4: Ловушка ОДЗ (один из корней числителя совпадает со знаменателем) ---
        # Тип: (x - a)(x - b) / (x - a) = 0. Ответ только b.
        elif difficulty == 4:
            r1 = random.randint(-20, 20) # Корень, который "вылетит" по ОДЗ
            r2 = random.randint(-20, 20) # Настоящий корень
            while r1 == r2: r2 = random.randint(-20, 20)
            a = random.choice([-1,2,3,-2,-3])
            
            numerator = expand(a * (x - r1) * (x - r2))
            denominator = x - r1
            roots = [r2] 

        # --- УРОВЕНЬ 3: Перенос слагаемого и общий знаменатель ---
        # Тип: a / (x - r1) = b / (x - r2) 
        # Приводится к: a(x - r2) - b(x - r1) = 0
        elif difficulty == 3:
            r1 = random.randint(-30, 30)
            r2 = random.randint(-30, 30)
            while r1 == r2: r2 = random.randint(-30, 30)
            
            target_root = random.randint(-30, 30)
            while target_root in [r1, r2]: target_root = random.randint(-30, 30)
            
            k = random.choice([1, 2, 3, 4, 5])
            a_val = k * (target_root - r1)
            b_val = k * (target_root - r2)
            
            # Вместо f-строк создаем объекты дробей SymPy

            
            left_side = a_val / (x - r1)
            right_side = b_val / (x - r2)
            
            # Генерируем LaTeX отдельно для левой и правой части
            latex_problem = f"{latex(left_side)} = {latex(right_side)}"
            roots = [target_root]

        # --- УРОВЕНЬ 5: Сложное уравнение, сводящееся к квадратному + ОДЗ ---
        # Тип: (x^2 + ax + b) / (x^2 - c^2) = 0
        elif difficulty == 5:
            r1 = random.randint(-20, 20)
            r2 = random.randint(-20, 20)
            forbidden = random.randint(1, 20)
            a = random.choice([-1,2,-2,3,-3])
            # Специально делаем так, чтобы один корень совпал с ОДЗ (x^2 - forbidden^2)
            # r1 будет равен forbidden, значит в ответе останется только r2
            r1 = forbidden 
            while r2 == forbidden or r2 == -forbidden:
                r2 = random.randint(-20, 20)
                
            numerator = expand(a * (x - r1) * (x - r2))
            denominator = x**2 - forbidden**2
            roots = [r2]

            # --- УРОВЕНЬ 6: "ЭКСТРИМ" (Биквадратный числитель + сложный знаменатель) ---
        elif difficulty == 6:
            # Используем random.sample, чтобы получить целые числа
            b1, b2 = random.sample([5, 6, 7, 8, 9, 10], 2)
            t1, t2 = b1**2, b2**2
            
            # Оставляем список потенциальных корней как int для SymPy
            potential_roots = [b1, -b1, b2, -b2]
            
            # Выбираем "запрещенные" корни (тоже int)
            forbidden_ones = random.sample(potential_roots, random.randint(1, 2))
            a = random.choice([2,-2,3,-3,4,-4])
            # Важно: используем только объекты SymPy (x, t1, t2), 
            # которые уже являются целыми, тогда expand() не создаст float
            numerator = expand(a * (x**2 - t1) * (x**2 - t2))
            
            denom_expr = 1
            for f in forbidden_ones:
                denom_expr *= (x - f)
            denominator = expand(denom_expr)
            
            # Корни для ответа (в конце переводим в float для логики бэкенда)
            roots = [r for r in potential_roots if r not in forbidden_ones]

        # --- ФИНАЛИЗАЦИЯ ---
        
        unique_roots = sorted(list(set([float(r) for r in roots])))
        
        # Формируем красивый LaTeX вид: \frac{P}{Q} = 0
        if difficulty !=3:
            latex_problem = r"\frac{" + latex(numerator) + "}{" + latex(denominator) + "} = 0"

        return {
            "type": "rational",
            "type_russian": "дробно-рациональное уравнение",
            "question_latex": self._format_latex(latex_problem),
            "answers": unique_roots,
            "complexity": self.diff(d),
            "difficulty": d
        }



    def generate_irrational(self, d):
        if d == 1: difficulty = 1
        elif d == 2: difficulty = random.choice([3, 4])
        elif d == 3: difficulty = 5
        x = self.x
        roots = []
        latex_problem = ""

        # --- УРОВЕНЬ 1: Простейшие вида sqrt(x + a) = b ---
        # Решается в одно действие: x + a = b^2
        if difficulty == 1:
            r1 = random.randint(-20, 20) # Корень уравнения
            b = random.randint(1, 10)    # Правая часть (всегда положительная)
            a = b**2 - r1
            # Уравнение: sqrt(x + a) = b
            # Чтобы в LaTeX не было "x + -5", используем latex(x + a)
            latex_problem = rf"\sqrt{{{latex(x + a)}}} = {b}"
            roots = [r1]

        # --- УРОВЕНЬ 3: sqrt(ax + b) = cx + d (Линейная правая часть) ---
        # При возведении в квадрат получается квадратное уравнение.
        # Один корень может быть посторонним.
        
        elif difficulty == 3:
            # 1. Генерируем два случайных целых корня для уравнения A - B = 0
            r1, r2 = random.sample(range(-7, 7), 2)
            
            # 2. Создаем случайный множитель 'a' (может быть отрицательным)
            a = random.choice([-3, -2, -1, 1, 2, 3])
            
            # 3. Формируем разность: a*(x - r1)*(x - r2)
            # Это то, что получится после возведения в квадрат и переноса в одну сторону
            difference = expand(a * (x - r1) * (x - r2))
            
            # 4. Чтобы под корнями были положительные числа при x=r1 и x=r2,
            # добавим к обеим частям "сдвиг" (константу или выражение)
            # Сдвиг должен быть таким, чтобы (f1 > 0) и (f2 > 0)
            # Вычисляем минимальное значение разности в корнях (оно 0) и добавим запас
            offset = random.randint(10, 20)
            
            # 5. Генерируем случайную линейную добавку для разнообразия, например (2x + 15)
            linear_shift = random.randint(1, 3) * x + random.randint(5, 15)
            
            # 6. Распределяем: sqrt(f1) = sqrt(f2) => f1 = f2 => f1 - f2 = 0
            # Пусть f1 = linear_shift + offset
            # Тогда f2 = f1 - difference
            f1 = expand(linear_shift + offset)
            f2 = expand(f1 - difference)
            
            # Проверка ОДЗ: подставляем корни в f1
            # Если вдруг < 0 (маловероятно при таких константах), просто берем модуль
            roots = []
            for r in [r1, r2]:
                if f1.subs(x, r) >= 0 and f2.subs(x, r) >= 0:
                    roots.append(float(r))
            
            latex_problem = rf"\sqrt{{{latex(f1)}}} = \sqrt{{{latex(f2)}}}"

        # --- УРОВЕНЬ 3: Сумма двух корней sqrt(A) + sqrt(B) = C ---
        # Требует двойного возведения в квадрат
        # --- УРОВЕНЬ 3: Сумма двух корней sqrt(A) + sqrt(B) = C ---
        elif difficulty == 4:
            # 1. Выбираем целевой корень
            target_x = random.randint(-5, 10)
            
            # 2. Генерируем два "удобных" значения для корней (например, 2 и 3)
            # Это результаты извлечения корня при подстановке target_x
            val1 = random.randint(1, 5)
            val2 = random.randint(1, 5)
            C = val1 + val2 # Правая часть уравнения
            
            # 3. Конструируем подкоренные выражения
            # Чтобы sqrt(k*x + b) = val1 при x = target_x:
            # k*target_x + b = val1^2  =>  b = val1^2 - k*target_x
            k1 = random.randint(1, 3)
            b1 = val1**2 - k1 * target_x
            expr1 = k1 * x + b1
            
            k2 = random.randint(1, 3)
            # Сделаем одно выражение квадратичным для разнообразия
            # Пусть sqrt(x^2 + b) = val2  => b = val2^2 - target_x^2
            if random.choice([True, False]):
                b2 = val2**2 - target_x**2
                expr2 = x**2 + b2
            else:
                b2 = val2**2 - k2 * target_x
                expr2 = k2 * x + b2
                
            # 4. Формируем LaTeX
            latex_problem = rf"\sqrt{{{latex(expr1)}}} + \sqrt{{{latex(expr2)}}} = {C}"
            
            # 5. Проверка на посторонние корни
            # При возведении в квадрат могут появиться другие корни.
            # Используем solve, чтобы найти ВСЕ корни и отфильтровать их.
            all_potential_roots = solve(sqrt(expr1) + sqrt(expr2) - C, x)
            
            roots = []
            for r in all_potential_roots:
                # Оставляем только вещественные и "красивые" числа
                try:
                    val = float(r)
                    if val.is_integer(): # Ограничимся целыми для этого уровня
                        roots.append(val)
                except:
                    continue

        # --- УРОВЕНЬ 4: Иррациональное + Замена переменной ---
        # x^2 + x + sqrt(x^2 + x + 2) = 10
        # Замена t = sqrt(x^2 + x + 2)
        elif difficulty == 5:
            # 1. Генерируем два целых корня для x (чтобы ответы были красивыми)
            r1, r2 = random.sample(range(-5, 10), 2)
            
            # 2. Формируем основу: x^2 + bx + constant
            # (x - r1)(x - r2) = x^2 - (r1+r2)x + r1*r2
            b_coeff = -(r1 + r2)
            target_const = r1 * r2
            base_expr = x**2 + b_coeff * x
            
            # 3. Выбираем параметры замены t = sqrt(base_expr + c)
            # Нам нужно, чтобы при наших r1, r2 под корнем было t_target^2
            # base_expr + c = t_target^2  => r1*r2 + c = t_target^2
            t_target = random.randint(5, 10)
            c = t_target**2 - target_const
            
            # 4. Чтобы уравнение было решаемым через t, выберем t_bad (отрицательный)
            t_bad = -random.randint(1, 10)
            
            # Коэффициенты для t^2 + mt + n = 0
            m = -(t_target + t_bad)
            n = t_target * t_bad
            
            # Гарантируем, что m != 0, чтобы корень не исчез
            if m == 0: m = 1 
            
            # Уравнение: (base_expr + c) + m*sqrt(base_expr + c) + n = 0
            # Преобразуем к виду для ученика: base_expr + m*sqrt(base_expr + c) = -n - c
            left_side = base_expr + m * sqrt(base_expr + c)
            right_side = -n - c
            
            # Красивый рендеринг коэффициента m
            m_str = f"{m}" if abs(m) != 1 else ("-" if m == -1 else "")
            
            latex_problem = fr"{latex(base_expr)} {'' if m < 0 else '+'}{m_str}\sqrt{{{latex(base_expr + c)}}} = {right_side}"
            
            roots = [float(r1), float(r2)]

        unique_roots = sorted(list(set([float(r) for r in roots])))

        return {
            "type": "irrational",
            "type_russian": "иррациональное уравнение",
            "question_latex": self._format_latex(latex_problem),
            "answers": unique_roots,
            "complexity": self.diff(d),
            "difficulty": d
        }



    def generate_logarithmic(self, d):
        if d == 1: difficulty = random.choice([1,2])
        elif d == 2: difficulty = random.choice([3,4])
        elif d == 3: difficulty = 5
        x = self.x
        roots = []
        latex_problem = ""

        # --- УРОВЕНЬ 1: log_a(x + b) = c ---
        # Решение: x + b = a^c
        if difficulty == 1:
            base = random.randint(2,10)
            ans_power = random.randint(0, 3) # Значение логарифма (c)
            r1 = random.randint(-30, 30)      # Корень (x)
            
            # Находим b: x + b = base**ans_power => b = base**ans_power - x
            b = base**ans_power - r1
            
            # log_{base}(x + b) = c
            latex_problem = rf"\log_{{{base}}}({latex(x + b)}) = {ans_power}"
            roots = [float(r1)]

        # --- УРОВЕНЬ 2: log_a(f(x)) = log_a(g(x)) ---
        # Линейные выражения с обеих сторон
        elif difficulty == 2:
            r1 = random.randint(-20, 20)
            base = random.randint(2, 10)
            
            # 1. Генерируем коэффициенты наклона
            k1 = random.randint(1, 10)
            k2 = k1 + random.randint(1, 10)
            
            # 2. Ключевой момент: подбираем b1 так, чтобы f(r1) > 0
            # f(r1) = k1*r1 + b1. Значит b1 должно быть > -k1*r1
            # Добавим случайный запас от 1 до 20, чтобы внутри логарифма не был ноль
            b1 = (-k1 * r1) + random.randint(1, 20)
            
            # 3. Вычисляем b2, чтобы обеспечить равенство f(r1) = g(r1)
            # k1*r1 + b1 = k2*r1 + b2  =>  b2 = k1*r1 + b1 - k2*r1
            b2 = k1*r1 + b1 - k2*r1
            
            f_x = k1*x + b1
            g_x = k2*x + b2

            # Теперь f(r1) гарантированно положительно, 
            # а так как g(r1) = f(r1), то и g(r1) > 0. Корень r1 всегда валиден.
            latex_problem = rf"\log_{{{base}}}({latex(f_x)}) = \log_{{{base}}}({latex(g_x)})"
            roots = [float(r1)]

        # --- УРОВЕНЬ 3: Свойство суммы log_a(f) + log_a(g) = log_a(f*g) ---
        # Появляется посторонний корень из-за ОДЗ аргумента
        
        elif difficulty == 3:
            # 1. Выбираем основание
            base = random.choice([2, 3, 5])
            
            # 2. Генерируем корни квадратного уравнения (x-r1)(x-r2) = 0
            # r_good должен быть больше смещений, чтобы аргументы были > 0
            # r_bad должен делать хотя бы один аргумент отрицательным
            r_good = random.randint(8, 15)
            r_bad = random.randint(-5, 0)
            
            # 3. Подбираем смещения b и c для (x + b) и (x + c)
            # Чтобы r_bad был плохим, нужно чтобы (r_bad + b) < 0 или (r_bad + c) < 0
            # Пусть b = - (r_bad - 1), тогда r_bad + b = 1 (хорошо), 
            # значит сделаем b и c такими, чтобы r_bad давал минус.
            
            # Простая схема: log(x - a1) + log(x - a2) = C
            a1 = random.randint(1, 4)
            a2 = a1 + random.randint(1, 3)
            # Тогда x^2 - (a1+a2)x + a1*a2 = base^power
            # Пусть x = r_good — корень. Тогда base^power = (r_good - a1)*(r_good - a2)
            
            val_at_good = (r_good - a1) * (r_good - a2)
            
            # Ищем такую степень, чтобы val_at_good был степенью основания
            # Если не получается красиво, просто подставим число в правую часть
            # log(f) + log(g) = log(val)
            
            expr1 = x - a1
            expr2 = x - a2
            
            latex_problem = rf"\log_{{{base}}}({latex(expr1)}) + \log_{{{base}}}({latex(expr2)}) = \log_{{{base}}}({val_at_good})"
            
            # Проверка корней через ОДЗ (x > a1 и x > a2)
            potential_roots = solve(expand(expr1 * expr2) - val_at_good, x)
            roots = []
            for r in potential_roots:
                r_val = float(r)
                if r_val > a1 and r_val > a2: # Условие ОДЗ
                    roots.append(r_val)

        # --- УРОВЕНЬ 4: Метод замены (log_a x)^2 + ... ---
        elif difficulty == 4:
            # t^2 - 3t + 2 = 0 => t=1, t=2
            base = random.choice([2, 3, 4, 5])
            t1 = random.randint(-2,3)
            t2 = random.randint(-2,3)
            #while t2 == t1: t2 = random.randint(1,5)
            r1, r2 = base**t1, base**t2
            
            # (log x)^2 - (t1+t2)log x + t1*t2 = 0
            m = -(t1 + t2)
            n = t1 * t2
            
            latex_problem = rf"(\log_{{{base}}} x)^2 {m}\log_{{{base}}} x + {n} = 0"
            if r1!=r2: roots = [float(r1), float(r2)]
            else: roots = [float(r1)]

        # --- УРОВЕНЬ 5:
        elif difficulty == 5:
            # Вариант А: Разные основания (log_a x + log_{a^2} x = b)
            # Вариант Б: Вложенные логарифмы (log_a(log_b(x)) = c)
            
            scenario = random.choice(['different_bases', 'nested'])
            
            if scenario == 'different_bases':
                # log_2(x) + log_4(x) + log_16(x) = 7
                # t + 0.5t + 0.25t = 7
                base = random.choice([2, 3])
                t_root = random.randint(2, 4) # log_base(x)
                
                # (1 + 1/2 + 1/4) * t = sum_val
                sum_val = Rational(7, 4) * t_root
                latex_problem = rf"\log_{{{base}}}(x) + \log_{{{base**2}}}(x) + \log_{{{base**4}}}(x) = {latex(sum_val)}"
                roots = [float(base**t_root)]

            elif scenario == 'nested':
                # log_a(log_b(x)) = c
                base1 = random.randint(2, 3)
                base2 = random.randint(2, 4)
                c = random.randint(0, 2)
                
                # Решение: log_b(x) = base1^c => x = base2^(base1^c)
                latex_problem = rf"\log_{{{base1}}}(\log_{{{base2}}}(x)) = {c}"
                roots = [float(base2**(base1**c))]


        return {
            "type": "logarithmic",
            "type_russian": "логарифмическое уравнение",
            "question_latex": self._format_latex(latex_problem),
            "answers": sorted(roots),
            "complexity": self.diff(d),
            "difficulty": d
        }



    def generate_modulus(self, d):
            if d == 1: difficulty = random.choice([1,2])
            elif d == 2: difficulty = random.choice([3,4])
            elif d == 3: difficulty = 5
            x = self.x
            latex_problem = ""
            roots = []

            # --- УРОВЕНЬ 1: |x + a| = b ---
            if difficulty == 1:
                # |x + 5| = 3 => x+5=3 или x+5=-3
                a = random.randint(-10, 10)
                b = random.randint(1, 15)
                latex_problem = rf"|{latex(x + a)}| = {b}"
                roots = [b - a, -b - a]

            # --- УРОВЕНЬ 2: |ax + b| = cx + d (Линейная правая часть) ---
            elif difficulty == 2:
                        # Уравнение |x - a| = kx + b
                # Чтобы избежать интервалов, k не должно быть равно 1 или -1
                k = random.choice([2, 3, 4, 5]) 
                x1 = random.randint(-10, 10) # Наш будущий целый корень
                a = random.randint(-20, 20)
                
                # Вычисляем b так, чтобы x1 был корнем: |x1 - a| = k*x1 + b
                b = abs(x1 - a) - k * x1
                
                right_side = k * x + b
                latex_problem = rf"|{latex(x - a)}| = {latex(right_side)}"
                
                # Решаем. Теперь здесь точно не будет интервала, так как k != 1
                sol = solve(sympy_abs(x - a) - right_side, x)
                roots = [float(r) for r in sol]

            # --- УРОВЕНЬ 3: |f(x)| = |g(x)| ---
            # Решается методом (f-g)(f+g) = 0 или f = g, f = -g

            # --- УРОВЕНЬ 4: Метод промежутков (Сумма двух модулей) ---
            # |x - a| + |x - b| = c
            elif difficulty == 3:
                # Подберем числа так, чтобы корни были "красивыми"
                # |x - 1| + |x - 3| = 4
                a, b = sorted(random.sample(range(-10, 10), 2))
                c = (b - a) + random.randint(2, 6)
                latex_problem = rf"|{latex(x - a)}| + |{latex(x - b)}| = {c}"
                roots = [float(r) for r in solve(abs(x - a) + abs(x - b) - c, x)]

            # --- УРОВЕНЬ 5: Модуль в модуле (Вложенность) ---
            # ||x + a| + b| = c
            elif difficulty == 4:
                a = random.randint(-10, 10)
                b = random.randint(-10, -1) # b должен быть отрицательным для интереса
                c = random.randint(1, 5)
                latex_problem = rf"||{latex(x + a)}| {b}| = {c}"
                roots = [float(r) for r in solve(abs(abs(x + a) + b) - c, x)]

            # --- УРОВЕНЬ 6: Квадратное уравнение с модулем (Замена) ---
            # x^2 - a|x| + b = 0  => (|x|)^2 - a|x| + b = 0
            elif difficulty == 5:
                # Пусть корни для t = |x| будут t1=2, t2=5
                t1, t2 = random.sample([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 2)
                # t^2 - (t1+t2)t + t1*t2 = 0
                b_coeff = -(t1 + t2)
                c_coeff = t1 * t2
                # Уравнение x^2 + b|x| + c = 0
                latex_problem = rf"x^2 {b_coeff}|x| + {c_coeff} = 0"
                roots = [float(t1), float(-t1), float(t2), float(-t2)]

            return {
                "type": "modulus",
                "type_russian": "модульное уравнение",
                "question_latex": self._format_latex(latex_problem),
                "answers": sorted(list(set([round(float(r), 2) for r in roots]))),
                "complexity": self.diff(d),
                "difficulty": d
            }
    
def normalize(s: str) -> str:
    s = str(s).lower()
    s = re.sub(r"\s+", "", s)   # все пробелы
    return (
        s.replace(",", ".")
         .replace("−", "-")
         .replace("x=", "")
    )


def normalize_str(s: str) -> str:
    s = str(s).lower()
    s = re.sub(r"\s+", "", s)
    return (
        s.replace("−", "-")
         .replace("x=", "")
    )

def to_number(s: str):
    try:
        return float(s)
    except ValueError:
        return None
    
def parse_user_answers(user_input: str) -> set[float]:
    norm = normalize_str(user_input)

    # запятая и точка с запятой — ТОЛЬКО разделители
    parts = re.split(r"[;,]", norm)

    numbers = set()
    for p in parts:
        if not p:
            continue
        try:
            numbers.add(float(p))
        except ValueError:
            pass

    return numbers

def parse_correct_answers(answers: list) -> set[float]:
    nums = set()
    for a in answers:
        n = to_number(normalize_str(a))
        if n is not None:
            nums.add(n)
    return nums

gen = EquationGenerator()


def eq_generator(type, diff):
    if diff == "random": diff = random.randint(1,3)
    if type == "quadratic": return gen.generate_quadratic(diff)
    elif type == "biquadratic": return gen.generate_biquadratic(diff)
    elif type == "cubic": return gen.generate_cubic(diff)
    elif type == "higher": return gen.generate_higher_degree(diff)
    elif type == "rational": return gen.generate_rational(diff)
    elif type == "irrational": return gen.generate_irrational(diff)
    elif type == "logarithmic": return gen.generate_logarithmic(diff)
    elif type == "modulus": return gen.generate_modulus(diff)
    elif type == "random": return random.choice([gen.generate_quadratic(diff),
                                                 gen.generate_biquadratic(diff),
                                                 gen.generate_cubic(diff),
                                                 gen.generate_higher_degree(diff),
                                                 gen.generate_rational(diff),
                                                 gen.generate_irrational(diff),
                                                 gen.generate_logarithmic(diff),
                                                 gen.generate_modulus(diff)
                                                 ])

