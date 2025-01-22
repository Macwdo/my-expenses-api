from rest_framework.routers import SimpleRouter

from api.views.expenses import TransactionModelViewSet

router = SimpleRouter()
router.register('transactions', TransactionModelViewSet)


urlpatterns = [
]
urlpatterns += router.urls
