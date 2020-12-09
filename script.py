from datacenter.models import Schoolkid, Mark, Chastisement, Commendation, Lesson
import random
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def get_schoolkid_by_fullname(full_name):
    try:
        schoolkid = Schoolkid.objects.filter(full_name__contains=full_name).get()
    except Schoolkid.DoesNotExist:
        logging.error("Ученик {} не найден".format(full_name))
    except Schoolkid.MultipleObjectsReturned:
        logging.error(
            "Найдено несколько учеников, попробуйте указать более конкретно (Фамилия Имя) или проверьте на ошибки в написании"  # noqa: E501
        )
        return None

    return schoolkid


def fix_marks(full_name):
    schoolkid = get_schoolkid_by_fullname(full_name)

    if schoolkid is None:
        return

    marks = Mark.objects.filter(schoolkid=schoolkid, points__lt=4)
    for mark in marks:
        logging.debug("Исправляем оценку {} на 5".format(mark))
        mark.points = 5
        mark.save()
        logging.debug("Исправлено!")

    logging.info("Исправление оценок завершено")


def remove_chastisements(full_name):
    schoolkid = get_schoolkid_by_fullname(full_name)

    if schoolkid is None:
        return

    all_chastisement = Chastisement.objects.filter(schoolkid=schoolkid)
    all_chastisement.delete()
    logging.info("Замечания удалены")


def create_commendation(full_name, subject):
    commendations_examples = [
        "Молодец!",
        "Отлично!",
        "Хорошо!",
        "Гораздо лучше, чем я ожидал!",
        "Ты меня приятно удивил!",
        "Великолепно!",
        "Прекрасно!",
        "Ты меня очень обрадовал!",
        "Именно этого я давно ждал от тебя!",
        "Сказано здорово – просто и ясно!",
        "Ты, как всегда, точен!",
        "Очень хороший ответ!",
        "Талантливо!",
        "Ты сегодня прыгнул выше головы!",
        "Я поражен!",
        "Уже существенно лучше!",
        "Потрясающе!",
        "Замечательно!",
        "Прекрасное начало!",
        "Так держать!",
        "Ты на верном пути!",
        "Здорово!",
        "Это как раз то, что нужно!",
        "Я тобой горжусь!",
        "С каждым разом у тебя получается всё лучше!",
        "Мы с тобой не зря поработали!",
        "Я вижу, как ты стараешься!",
        "Ты растешь над собой!",
        "Ты многое сделал, я это вижу!",
        "Теперь у тебя точно все получится!",
    ]
    schoolkid = get_schoolkid_by_fullname(full_name)

    if schoolkid is None:
        return

    lesson = (
        Lesson.objects.filter(
            subject__title=subject,
            group_letter=schoolkid.group_letter,
            year_of_study=schoolkid.year_of_study,
        )
        .order_by("-date")
        .first()
    )
    if lesson is None:
        logging.error(
            "Урок {} в классе {} не найден".format(
                subject, f"{schoolkid.year_of_study}{schoolkid.group_letter}"
            )
        )
        return

    Commendation.objects.create(
        subject=lesson.subject,
        teacher=lesson.teacher,
        created=lesson.date,
        schoolkid=schoolkid,
        text=commendations_examples[random.randint(0, len(commendations_examples) - 1)],
    )

    logging.info("Похвала создана!")

    return
