from django import forms
from .models import Chat, Book, User


class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ('message',)
        widgets = {
            'message': forms.Textarea(attrs={'placeholder': 'Type your message here...'}),
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'publisher', 'year', 'uploaded_by', 'desc')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
