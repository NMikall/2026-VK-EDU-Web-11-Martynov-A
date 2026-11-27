import random

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db import transaction
from django.db.models import Case, Count, IntegerField, OuterRef, Subquery, Sum, When
from django.db.models.functions import Coalesce
from faker import Faker

from core.models import Profile
from questions.models import Question, Answer, Tag, Tags, QuestionLike, AnswerLike


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("ratio", type=int)

    def handle(self, *args, **options):
        ratio = options["ratio"]
        batch_size = 50000
        fake = Faker()

        users_to_create = []
        for i in range(ratio):
            user = User(username=f'user_{i}', email=fake.email(), password="password123")
            users_to_create.append(user)
            if i != 0 and i % batch_size == 0:
                User.objects.bulk_create(users_to_create, batch_size=1_000)
                users_to_create.clear()
        if len(users_to_create) != 0:
            User.objects.bulk_create(users_to_create, batch_size=1_000)
        user_ids = list(User.objects.values_list('id', flat=True))

        users_without_profile = list(
            User.objects.filter(profile__isnull=True).values_list('id', flat=True)
        )
        profiles_to_create = []
        for i, user_id in enumerate(users_without_profile):
            profile = Profile(user_id=user_id, nickname=f'nick_{user_id}')
            profiles_to_create.append(profile)
            if i != 0 and i % batch_size == 0:
                Profile.objects.bulk_create(profiles_to_create, batch_size=1_000)
                profiles_to_create.clear()
        if len(profiles_to_create) != 0:
            Profile.objects.bulk_create(profiles_to_create, batch_size=1_000)

        tags_to_create = []
        for i in range(ratio):
            tag = Tag(name_tag=f'{fake.word()}_{i}')
            tags_to_create.append(tag)
            if i != 0 and i % batch_size == 0:
                Tag.objects.bulk_create(tags_to_create, batch_size=1_000)
                tags_to_create.clear()
        if len(tags_to_create) != 0:
            Tag.objects.bulk_create(tags_to_create, batch_size=1_000)
        tag_ids = list(Tag.objects.values_list('id', flat=True))

        questions_to_create = []
        for i in range(ratio * 10):
            question = Question(
                user_id=random.choice(user_ids),
                title=fake.sentence(nb_words=6),
                text=fake.text(max_nb_chars=500),
            )
            questions_to_create.append(question)
            if i != 0 and i % batch_size == 0:
                Question.objects.bulk_create(questions_to_create, batch_size=1_000)
                questions_to_create.clear()
        if len(questions_to_create) != 0:
            Question.objects.bulk_create(questions_to_create, batch_size=1_000)
        question_ids = list(Question.objects.values_list('id', flat=True))

        question_tags_to_create = []
        for i, question_id in enumerate(question_ids):
            for tag_id in random.sample(tag_ids, k=min(3, len(tag_ids))):
                question_tags_to_create.append(Tags(question_id=question_id, tag_id=tag_id))
            if i != 0 and i % batch_size == 0:
                Tags.objects.bulk_create(question_tags_to_create, batch_size=1_000)
                question_tags_to_create.clear()
        if len(question_tags_to_create) != 0:
            Tags.objects.bulk_create(question_tags_to_create, batch_size=1_000)

        answers_to_create = []
        for i in range(ratio * 100):
            answer = Answer(
                user_id=random.choice(user_ids),
                question_id=random.choice(question_ids),
                text=fake.text(max_nb_chars=300),
            )
            answers_to_create.append(answer)
            if i != 0 and i % batch_size == 0:
                Answer.objects.bulk_create(answers_to_create, batch_size=1_000)
                answers_to_create.clear()
        if len(answers_to_create) != 0:
            Answer.objects.bulk_create(answers_to_create, batch_size=1_000)
        answer_ids = list(Answer.objects.values_list('id', flat=True))

        pairs = random.sample(
            range(len(user_ids) * len(question_ids)),
            min(ratio * 100, len(user_ids) * len(question_ids)),
        )
        question_likes_to_create = []
        for i, n in enumerate(pairs):
            like = QuestionLike(
                user_id=user_ids[n // len(question_ids)],
                question_id=question_ids[n % len(question_ids)],
                like_or_dislike=random.random() < 0.8,
            )
            question_likes_to_create.append(like)
            if i != 0 and i % batch_size == 0:
                QuestionLike.objects.bulk_create(question_likes_to_create, batch_size=1_000)
                question_likes_to_create.clear()
        if len(question_likes_to_create) != 0:
            QuestionLike.objects.bulk_create(question_likes_to_create, batch_size=1_000)

        pairs = random.sample(
            range(len(user_ids) * len(answer_ids)),
            min(ratio * 100, len(user_ids) * len(answer_ids)),
        )
        answer_likes_to_create = []
        for i, n in enumerate(pairs):
            like = AnswerLike(
                user_id=user_ids[n // len(answer_ids)],
                answer_id=answer_ids[n % len(answer_ids)],
                like_or_dislike=random.random() < 0.8,
            )
            answer_likes_to_create.append(like)
            if i != 0 and i % batch_size == 0:
                AnswerLike.objects.bulk_create(answer_likes_to_create, batch_size=1_000)
                answer_likes_to_create.clear()
        if len(answer_likes_to_create) != 0:
            AnswerLike.objects.bulk_create(answer_likes_to_create, batch_size=1_000)

        score = Case(When(like_or_dislike=True, then=1), default=-1, output_field=IntegerField())
        with transaction.atomic():
            answers_count = (Answer.objects.filter(question=OuterRef('pk'))
                             .order_by().values('question').annotate(total=Count('pk')).values('total'))
            question_likes_sum = (QuestionLike.objects.filter(question=OuterRef('pk'))
                                  .order_by().values('question').annotate(total=Sum(score)).values('total'))
            answer_likes_sum = (AnswerLike.objects.filter(answer=OuterRef('pk'))
                                .order_by().values('answer').annotate(total=Sum(score)).values('total'))
            Question.objects.update(
                number_of_answers=Coalesce(Subquery(answers_count), 0),
                likes=Coalesce(Subquery(question_likes_sum), 0),
            )
            Answer.objects.update(likes=Coalesce(Subquery(answer_likes_sum), 0))
        self.stdout.write(self.style.SUCCESS('База заполнена'))