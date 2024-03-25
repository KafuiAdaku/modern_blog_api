import factory

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from faker import Factory as FakerFactory


faker = FakerFactory.create()
User = get_user_model()

@factory.django.mute_signals(post_save)

class UserFactory(factory.django.DjangoModelFactory):
    """Factory for User model"""
    first_name = factory.LazyAttribute(lambda x: faker.first_name())
    last_name = factory.LazyAttribute(lambda x: faker.last_name())
    username = factory.LazyAttribute(lambda x: faker.first_name().lower())
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.org")
    password = factory.LazyAttribute(lambda x: faker.password())
    is_active = True
    is_staff = False

    class Meta:
        """"Meta class"""
        model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default _create"""
        manager = cls._get_manager(model_class)
        if "is_super_user" in kwargs:
            return manager.create_superuser(*args, **kwargs)

        return manager.create_superuser(*args, **kwargs)