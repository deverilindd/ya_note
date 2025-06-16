from http import HTTPStatus
from unittest import skip
# Импортируем функцию для определения модели пользователя.
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

# Импортируем класс комментария.
from notes.models import Note

# Получаем модель пользователя.
User = get_user_model()


# Главная страница доступна анонимному пользователю.
# Страницы регистрации пользователей, входа в учётную
# запись и выхода из неё доступны всем пользователям.
class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='author')
        cls.reader = User.objects.create(username='reader')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author
        )

    def test_pages_availability(self):
        urls = (
            ('notes:home', None),
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    # Аутентифицированному пользователю доступна страница со списком заметок
    # notes/, страница успешного добавления заметки done/, страница добавления
    # новой заметки add/.
    def test_availability_for_note_add_and_done(self):
        urls = (
            'notes:list',
            'notes:success',
            'notes:add',
        )
        self.client.force_login(self.author)
        for name in urls:
            with self.subTest(name=name):
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    # Страницы отдельной заметки, удаления и редактирования заметки доступны
    # только автору заметки. Если на эти страницы попытается зайти другой
    # пользователь — вернётся ошибка 404.
    def test_availability_for_note_edit_and_delete(self):
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for name in ('news:edit', 'news:delete'):
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.comment.id,))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    @skip(reason='потом')
    def test_redirect_for_anonymous_client(self):
        login_url = reverse('users:login')
        for name in ('news:edit', 'news:delete'):
            with self.subTest(name=name):
                url = reverse(name, args=(self.comment.id,))
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)




# При попытке перейти на страницу списка заметок, страницу успешного
# добавления записи, страницу добавления заметки, отдельной заметки,
# редактирования или удаления заметки анонимный пользователь перенаправляется
# на страницу логина.
