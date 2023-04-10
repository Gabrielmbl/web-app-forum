from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from my_app.views import home_page
from my_app.models import Message, Thread

# Create your tests here.

# Check that we can create database entries directly.
class DirectDatabaseTest(TestCase):
    
    def test_can_create_threads_and_posts(self):
        thread_ = Thread()
        thread_.save()

        # Saving step
        first_message = Message()
        first_message.alias = 'Gabriel'
        first_message.text = 'First message'
        first_message.thread = thread_
        first_message.save()

        second_message = Message()
        second_message.alias = 'Lucas'
        second_message.text = 'Second message'
        second_message.thread = thread_
        second_message.save()

        saved_thread = Thread.objects.first()
        self.assertEqual(saved_thread, thread_)

        # Retrieving Step
        saved_messages = Message.objects.all()
        self.assertEqual(saved_messages.count(), 2)

        first_saved_message = saved_messages[0]
        second_saved_message = saved_messages[1]
        self.assertEqual(first_saved_message.text, 'First message')
        self.assertEqual(first_saved_message.thread, thread_)
        self.assertEqual(second_saved_message.text, 'Second message')
        self.assertEqual(second_saved_message.thread, thread_)


# We test if we can use view functions to store data to database.
class PostToDatabaseTests(TestCase):

    def test_can_create_a_thread_and_post_through_POST(self):
        user_response = self.client.post(f'/my_app/new', data={'alias_thread': 'A random user', 'subject_thread': 'A new thread', 'message_text': 'A new message'})
        new_thread = Thread.objects.first()
        new_message = Message.objects.first()
        self.assertEqual(new_thread.alias, 'A random user')
        self.assertEqual(new_thread.subject, 'A new thread')
        self.assertEqual(new_message.text, 'A new message')
    
    def test_can_add_to_thread_through_POST(self):
        other_thread = Thread.objects.create()
        correct_thread = Thread.objects.create()

        self.client.post(
            f'/my_app/{correct_thread.id}/add_message',
            data={'alias_text': 'Another random user', 'message_text': 'Some random message'}
        )

        self.assertEqual(Message.objects.count(),1)
        new_message = Message.objects.first()
        self.assertEqual(new_message.text, 'Some random message')
        self.assertEqual(new_message.thread, correct_thread)


# Test that correct redirects and renders occur
class RenderAndRedirectTests(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'creativename.html')

    def test_view_thread_returns_correct_html(self):
        other_thread = Thread.objects.create()
        correct_thread = Thread.objects.create()
        response = self.client.get(f'/my_app/{correct_thread.id}/')
        self.assertEqual(response.context['thread'], correct_thread)

    def test_add_new_thread_through_POST_redirects(self):
        response = self.client.post(f'/my_app/new', 
                                    data={'alias_thread': 'A random user', 
                                            'subject_thread': 'A new thread', 
                                            'message_text': 'A new message'})
        new_thread = Thread.objects.first()
        self.assertRedirects(response, f'/my_app/{new_thread.id}/')


    def test_add_post_through_POST_redirects(self):
        other_thread = Thread.objects.create()
        correct_thread = Thread.objects.create()

        response = self.client.post(f'/my_app/{correct_thread.id}/add_message', 
                                    data={'alias_text': 'Another random user', 
                                    'message_text': 'Some random message'})

        self.assertRedirects(response, f'/my_app/{correct_thread.id}/')
