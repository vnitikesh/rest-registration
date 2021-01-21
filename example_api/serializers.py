from example_api.models import Category, Product, Cart, Checkout
from rest_framework import serializers
import itertools
from shop_api.serializers import ShopSerializer
from shop_api.models import Shop
from rest_framework.fields import CurrentUserDefault


class SlugRelatedModuleField(serializers.SlugRelatedField):
    def get_queryset(self):
        queryset = Shop.objects.all()
        request = self.context.get('request', None)
        queryset = queryset.filter(owner = request.user)
        return queryset



class CategorySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name = 'category-detail', read_only = True)
    shop = SlugRelatedModuleField(slug_field = 'shop_name')
    class Meta:
        model = Category
        fields = ('id', 'url','shop', 'name')

class SlugRelatedProductModuleField(serializers.SlugRelatedField):
    def get_queryset(self):
        shop = Shop.objects.all()
        request = self.context.get('request', None)
        shop = shop.filter(owner = request.user)

        queryset = Category.objects.filter(shop__id__in = shop)
        return queryset

class ProductSerializer(serializers.ModelSerializer):
    shop = SlugRelatedModuleField(slug_field = 'shop_name')
    #category = CategorySerializer(required = True)
    category = SlugRelatedProductModuleField(slug_field = 'name')
    class Meta:
        model = Product
        fields = ('id','shop', 'category', 'name', 'price')

    def create(self, validated_data):

        shop_data = validated_data.pop('shop')
        product_data = validated_data.pop('category')


        #category = CategorySerializer.create(CategorySerializer(), validated_data = product_data)
        shop = Shop.objects.get(shop_name = shop_data)
        category = Category.objects.get(shop = shop, name = product_data)

        product, created = Product.objects.update_or_create(shop = shop, category = category,
                                name = validated_data.pop('name'),
                                price = validated_data.pop('price'))
        return product

class ProductHelperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'price')

class CategoryDetailSerializer(serializers.ModelSerializer):
    #products = ProductSerializer(many = True)
    #products = serializers.StringRelatedField(many = True)
    shop = ShopSerializer()
    products = ProductHelperSerializer(many = True)
    class Meta:
        model = Category
        fields = ('id', 'shop', 'name', 'products')

class CartSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.username')
    subtotal = serializers.DecimalField(max_digits = 50, decimal_places = 2, read_only = True)
    order_items = ProductHelperSerializer
    items_ordered = serializers.CharField(read_only = True)
    shop = ShopSerializer(read_only = True)
    #quantities = serializers.IntegerField(read_only = True)
    class Meta:
        model = Cart
        fields = ['shop', 'user', 'items_ordered', 'subtotal', 'order_items', 'quantities']

    def create(self, validated_data):
        print(validated_data)
        item = validated_data['order_items']
        print(type(item[0]))
        prod = Product.objects.get(name = item[0])
        request = self.context.get('request', None)
        quantities = validated_data.pop('quantities')
        product_total_price = quantities * prod.price
        instance = Cart.objects.create(subtotal = product_total_price, user = request.user, shop = prod.shop, quantities = quantities)
        instance.order_items.set(validated_data.pop('order_items'))
        instance.items_ordered = prod.name

        instance.save()
        return instance

        #return Cart.objects.create(subtotal = prod.price, order_items = validated_data)
class CheckoutHelperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = ['cart']


class CheckoutSerializer(serializers.ModelSerializer):
    #cart = CheckoutHelperSerializer(read_only = True, many = True)
    delivery_address = serializers.ReadOnlyField()
    item_total_cost = serializers.DecimalField(read_only = True, max_digits = 10, decimal_places = 2)
    delivery_charge = serializers.DecimalField(read_only = True, max_digits = 10, decimal_places = 2)
    total = serializers.DecimalField(read_only = True, max_digits = 10, decimal_places = 2)
    class Meta:
        model = Checkout
        fields = ['cart','delivery_address', 'item_total_cost', 'delivery_charge', 'total']

    def create(self, validated_data, user):
        product_dicts = dict(itertools.islice(validated_data.items(), 4))
        print(validated_data)
        for key in product_dicts.keys():
            validated_data.pop(key)
        print(validated_data)
        print(product_dicts)
        checkout = Checkout.objects.create(**product_dicts)

        print(type(checkout))
        checkout.cart = validated_data
        checkout.user = user
        checkout.save()
        return checkout
