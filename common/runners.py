from django.test.runner import DiscoverRunner
from django.test.utils import override_settings


class InMemoryStorageTestRunner(DiscoverRunner):
    def setup_test_environment(self, **kwargs):
        super().setup_test_environment(**kwargs)

        # Override the STORAGES settings to use in-memory storage
        self._override_storage = override_settings(
            STORAGES={
                "default": {
                    "BACKEND": "django.core.files.storage.memory.InMemoryStorage",
                },
                "staticfiles": {
                    "BACKEND": "django.core.files.storage.memory.InMemoryStorage",
                    "OPTIONS": {
                        "location": "static",
                    },
                },
            },
        )
        self._override_storage.enable()

    def teardown_test_environment(self, **kwargs):
        super().teardown_test_environment(**kwargs)

        # Disable the override settings
        self._override_storage.disable()
