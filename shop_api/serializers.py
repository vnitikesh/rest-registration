from .models import Shop, Category, Product
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


class CategoryListSerializer(serializers.ModelSerializer):
    shop = SlugRelatedModuleField(slug_field = 'shop_name')
    #shop = ShopSerializer(read_only = True)

    class Meta:
        model = Category
        fields = ('id', 'shop', 'name')
'''
class CategoryRelatedModuleField(serializers.SlugRelatedField):
    def get_queryset(self):
        queryset = Category.objects.all(shop = )
'''

class ProductSerializer(serializers.ModelSerializer):
    shop = SlugRelatedModuleField(slug_field = 'shop_name')
    class Meta:
        model = Product
        fields = ('shop', 'id', 'name', 'price', 'available', )

class CategoryDetailSerializer(serializers.HyperlinkedModelSerializer):
    shop = ShopSerializer(read_only = True)
    product = ProductSerializer(read_only = True)

    class Meta:
        model = Category
        fields = ('id', 'shop', 'name', 'product')
