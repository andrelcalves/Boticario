import factory

from backend.core.models import CreateSeller


class CreateSellerFactory(factory.Factory):
    cpf: str = factory.Faker("cpf", locale="pt_BR")
    name: str = factory.Faker("name")
    email: str = factory.LazyAttribute(
        lambda o: "%s@example.com" % str(o.name).lower().replace(" ", "_").replace(".", "")
    )
    password: str = factory.Faker("pystr")
    confirm_password: str = factory.lazy_attribute(lambda o: o.password)

    class Meta:
        model = CreateSeller
