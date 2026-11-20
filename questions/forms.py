from django import forms
from django.contrib.auth.models import User
from django.db.models import F

from questions.models import Answer, Question, Tag, Tags


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text',)
    text = forms.CharField(max_length=2000)

    def save(self, user, question):
        answer = super().save(commit=False)
        answer.user = user
        answer.question = question
        answer.save()
        Question.objects.filter(pk=question.pk).update(number_of_answers=(F('number_of_answers') + 1))
        return answer

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text']

    text = forms.CharField(max_length=2000)
    tags = forms.CharField(max_length=100)
    title = forms.CharField(max_length=100)

    def clean_tags(self):
        tags = {t.strip() for t in self.cleaned_data['tags'].split(',') if t.strip()}
        if not tags:
            raise forms.ValidationError('Tags cannot be an empty string')
        if len(tags) > 3:
            raise forms.ValidationError('Tags cannot be more than 3 tag')
        return list(tags)


    def save(self, user):
        question = super().save(commit=False)
        question.user = user
        question.save()
        for name in self.cleaned_data['tags']:
            tag, _ = Tag.objects.get_or_create(name_tag=name)
            Tags.objects.create(question=question, tag=tag)
        return question
