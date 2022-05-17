from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        label = {'text': 'Введите текст',
                 'group': 'Выберите группу',
                 'image': 'Выберите картинку'}
        help_text = {'text': 'Любую абракадабру',
                     'group': 'Из уже существующих',
                     'image': 'Можно фото из паспорта'}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        help_text = {'text': 'Любую абракадабру'}
