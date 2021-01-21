from .models import Shop
from rest_framework import serializers


class SlugRelatedModuleField(serializers.SlugRelatedField):

    # Customized queryset which is sending GET response in the form of shop object filterised by the user in session.
    def get_queryset(self):
        queryset = Shop.objects.all()
        request = self.context.get('request', None)
        queryset = queryset.filter(owner = request.user)
        return queryset


class ShopSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.username')
    categories = serializers.HyperlinkedRelatedField(many = True, view_name = 'category-detail', read_only = True)
    #add_category = serializers.HyperlinkedIdentityField(view_name = 'category-detail', lookup_field = 'pk')

    class Meta:
        model = Shop
        fields = ('url', 'id', 'shop_name', 'owner', 'delivery_time', 'discount_coupon', 'rating', 'categories')
