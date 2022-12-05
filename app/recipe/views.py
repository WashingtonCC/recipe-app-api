"""
Views for the recipe APIs.
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
from rest_framework import (
    viewsets,
    mixins, # mixins that you can add to a view to add functionality
    status,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag, Ingredient
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    # the way you tell the Model View Set which model you'll use
    # is by specifying the queryset.
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # In order to use any of the endpoints provided by this viewset,
    # you need to use Token Authentication and be authenticated

    def _params_to_ints(self, qs):
        """Convert a list of strings to integers."""
        # /?tags=1,2,3 -> "1,2,3" -> [1, 2, 3]
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self, params):
        """Retrive recipes for authenticated user ONLY."""
        #return self.queryset.filter(user=self.request.user).order_by('-id')
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset #The correct way is this, but for some reason doesn't work
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        return queryset.filter(
            user=self.request.user
        ).order_by('-id').distinct()
        # distinct eliminates duplicate db rows. it uses SELECT DISTINCT
        # duplicates may appear when filtering in 48 and 51

    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == 'list':
            return serializers.RecipeSerializer
        elif self.action == 'upload_image': # custom action. Read viewset docs
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe."""
        # serializer is already validated by the viewset
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to recipe"""
        # detail because you upload to a specific recipeff
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BaseRecipeAttrViewSet(mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    """Base viewset for recipe attributes."""
    # This code was duplicated in tag and ingredient viewsets
    # so we just refactored it into a base class.
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database."""
    # Must inherit GenericViewSet after mixins
    # The mixins handle their responsibilities themselves, without having to configure anything.
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in db"""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
