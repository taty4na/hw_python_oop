class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type : str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Сообщение."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}')


class Training: 
    """Базовый класс тренировки."""
    
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance_km = self.action * self.LEN_STEP / self.M_IN_KM
        return distance_km

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(training_type= self.__class__.__name__,
                           duration= self.duration,
                           distance= self.get_distance(),
                           speed= self.get_mean_speed(),
                           calories= self.get_spent_calories()
                           )
        return (info.get_message())


class Running(Training):
    """Тренировка: бег."""

    COEF_CAL_1: int = 18
    COEF_CAL_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        calories_calc = self.COEF_CAL_1 * self.get_mean_speed() - self.COEF_CAL_2
        calories_result = calories_calc * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_HOUR
        return calories_result


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEF_CAL_3: float = 0.035
    COEF_CAL_4: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при ходьбе."""
        calories_calc = (self.get_mean_speed() ** 2 // self.height) * self.COEF_CAL_4 * self.weight
        calories_result = self.COEF_CAL_3 * self.weight + calories_calc * self.MIN_IN_HOUR
        return calories_result


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    COEF_CAL_5: float = 1.1
    COEF_CAL_6: int = 2
    
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,                 
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        
    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий в бассейне."""
        calories_result = (self.get_mean_speed() + self.COEF_CAL_5) * self.COEF_CAL_6 * self.weight
        return calories_result


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    training = {'RUN':Running, 'WLK':SportsWalking, 'SWM':Swimming}
    try:
        return training[workout_type](*data)
    except:
        print ('ошибка')


def main(training: Training) -> None:
    """Главная функция."""
    
    print (training.show_training_info())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

