from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.models import Note
from notes.forms import NoteForm

User = get_user_model()


class TestNotesList(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='author')
        cls.reader = User.objects.create(username='reader')
        cls.author_note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='author',
            author=cls.author
        )
        cls.reader_note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='reader',
            author=cls.reader
        )

    def test_note_in_notes_list(self):
        self.client.force_login(self.author)
        url = reverse('notes:list')
        response = self.client.get(url)
        object_list = response.context['object_list']
        self.assertIn(self.author_note, object_list)
        self.assertNotIn(self.reader_note, object_list)

    def test_edit_note_page_contains_form(self):
        self.client.force_login(self.author)
        pages_with_forms = (
            ('notes:edit', (self.author_note.slug,)),
            ('notes:add', None),
        )
        for name, args in pages_with_forms:
            url = reverse(name, args=args)
            response = self.client.get(url)
            self.assertIn('form', response.context)
            self.assertIsInstance(response.context['form'], NoteForm)
