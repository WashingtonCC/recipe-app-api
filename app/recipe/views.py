"""
Views for the recipe APIs.
"""
from rest_framework import viewsets, mixins # mixins that you can add to a view to add functionality
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag
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

    def get_queryset(self):
        """Retrive recipes for authenticated user ONLY."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == 'list':
            return serializers.RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe."""
        # serializer is already validated by the viewset
        serializer.save(user=self.request.user)


class TagViewSet(mixins.UpdateModelMixin,
                 mixins.ListModelMixin,
                 mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):
    """Manage tags in the database."""
    # Must inherit GenericViewSet after mixins
    # The mixins handle their responsibilities themselves, without having to configure anything.
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')
