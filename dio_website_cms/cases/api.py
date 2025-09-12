from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet
from wagtail.images.api.v2.views import ImagesAPIViewSet

from .models import CasePage


class CasePageAPIViewSet(PagesAPIViewSet):
    def get_queryset(self) -> None:
        queryset = super().get_queryset()
        return queryset.type(CasePage)


router = WagtailAPIRouter("wagtailapi")

router.register_endpoint("pages", PagesAPIViewSet)
router.register_endpoint("case_pages", CasePageAPIViewSet)
router.register_endpoint("images", ImagesAPIViewSet)
router.register_endpoint("documents", DocumentsAPIViewSet)
