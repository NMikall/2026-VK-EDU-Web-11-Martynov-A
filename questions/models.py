from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q, F
from django.urls import reverse



class DefaultModel(models.Model):
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    class Meta:
        abstract = True


class QuestionManager(models.Manager):
    def new(self):
        return self.filter(is_active=True).order_by('-created_at').select_related('user__profile').prefetch_related('tags_set__tag')

    def best(self):
        return self.filter(is_active=True).order_by('-likes', '-id').select_related('user__profile').prefetch_related('tags_set__tag')

    def by_tag(self, tag_name):
        return self.new().filter(tags__tag__name_tag=tag_name)

    def search(self, query):
        return self.new().filter(Q(title__icontains=query) | Q(text__icontains=query))

class AnswerManager(models.Manager):
    def for_question(self, question_id):
        return self.filter(question_id=question_id, is_active=True).order_by('-likes', '-id').select_related('user__profile')

    def page_of(self, answer, per_page=10):
        answers = self.filter(question_id=answer.question_id, is_active=True)
        before = answers.filter(likes__gt=answer.likes).count() + answers.filter(likes=answer.likes, id__gt=answer.id).count()
        return before // per_page + 1

class Question(DefaultModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    title = models.CharField(max_length=100, verbose_name="Заголовок вопроса")
    text = models.TextField(max_length=2000, verbose_name="Текст вопроса")
    number_of_answers = models.IntegerField(default=0, verbose_name="Число ответов")
    likes = models.IntegerField(default=0, verbose_name="Число лайков")
    objects = QuestionManager()
    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return f"Вопрос #{self.pk}: `{self.title}`"

    def get_absolute_url(self):
        return reverse('question', args=[self.pk])

    def vote(self, user, is_like):
        like = QuestionLike.objects.filter(user=user, question=self).first()
        if like is None:
            QuestionLike.objects.create(user=user, question=self, like_or_dislike=is_like)
            Question.objects.filter(pk=self.pk).update(likes=F('likes') + (1 if is_like else -1))
        elif like.like_or_dislike != is_like:
            like.delete()
            Question.objects.filter(pk=self.pk).update(likes=F('likes') + (1 if is_like else -1))
        self.refresh_from_db(fields=['likes'])
        return self.likes

class Answer(DefaultModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")
    text = models.TextField(max_length=2000, verbose_name="Текст ответа")
    likes = models.IntegerField(default=0, verbose_name="Число лайков")
    best_answer = models.BooleanField(default=False, verbose_name="Лучший ли вопрос")
    objects = AnswerManager()

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return f"Ответ #{self.pk}: `{self.text}`"

    def vote(self, user, is_like):
        like = AnswerLike.objects.filter(user=user, answer=self).first()
        if like is None:
            AnswerLike.objects.create(user=user, answer=self, like_or_dislike=is_like)
            Answer.objects.filter(pk=self.pk).update(likes=F('likes') + (1 if is_like else -1))
        elif like.like_or_dislike != is_like:
            like.delete()
            Answer.objects.filter(pk=self.pk).update(likes=F('likes') + (1 if is_like else -1))
        self.refresh_from_db(fields=['likes'])
        return self.likes

    def answer_best(self, user):
        if self.question.user_id != user.id:
            return False
        new_value = not self.best_answer
        Answer.objects.filter(question_id=self.question_id).update(best_answer=False)
        Answer.objects.filter(pk=self.pk).update(best_answer=new_value)
        return True

class Tag(models.Model):
    name_tag = models.CharField(max_length=100, verbose_name="Имя тега")

    def __str__(self):
        return self.name_tag

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

class Tags(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="Тег")
    class Meta:
        unique_together = ('question', 'tag')
        verbose_name = "Тег вопроса"
        verbose_name_plural = "Теги вопросов"

class QuestionLike(DefaultModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    like_or_dislike = models.BooleanField(default=True, verbose_name="Лайк или дизлайк")
    class Meta:
        unique_together = ('user', 'question')
        verbose_name = "Лайк на вопрос"
        verbose_name_plural = "Лайки на вопросы"

    def __str__(self):
        return f"Лайк #{self.pk} на вопрос `{self.question_id}`"

class AnswerLike(DefaultModel):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name="Ответ")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    like_or_dislike = models.BooleanField(default=True, verbose_name="Лайк или дизлайк")

    class Meta:
        unique_together = ('user', 'answer')
        verbose_name = "Лайк на ответ"
        verbose_name_plural = "Лайки на ответы"

    def __str__(self):
        return f"Лайк #{self.pk} на ответ `{self.answer_id}`"