import factory
from django.db.models.signals import post_save
from faker import Factory as FakerFactory

from core_apps.profiles.models import Profile
from core_apps.users.tests.factories import UserFactory

faker = FakerFactory.create()


@factory.django.mute_signals(post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    """Factory for Profile model"""
    user = factory.SubFactory(UserFactory)
    phone_number = factory.LazyAttribute(lambda x: faker.phone_number())
    about_me = factory.LazyAttribute(lambda x: faker.sentence(nb_words=5))
    gender = factory.LazyAttribute(lambda x: faker.random_element(elements=('M', 'F', 'O')))
    country = factory.LazyAttribute(lambda x: faker.country_code())
    city = factory.LazyAttribute(lambda x: faker.city())
    profile_photo = factory.LazyAttribute(lambda x: faker.file_extension(category="image"))
    twitter_handle = factory.LazyAttribute(lambda x: faker.user_name())

    class Meta:
        """Meta class"""
        model = Profile

    @factory.post_generation
    def follows(self, create, extracted, **kwargs):
        """Post generation method"""
        if not create:
            return

        if extracted:
            for follow in extracted:
                self.follows.add(follow)