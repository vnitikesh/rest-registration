from example_api.models import Category, Product, Cart, Checkout
from rest_framework import serializers
import itertools


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name = 'category-detail', read_only = True)
    class Meta:
        model = Category
        fields = ('id', 'url', 'name')

class SlugRelatedModuleField(serializers.SlugRelatedField):
    def get_queryset(self):
        queryset = Category.objects.all()
        return queryset

class ProductSerializer(serializers.ModelSerializer):
    #category = CategorySerializer(required = True)
    category = SlugRelatedModuleField(slug_field = 'name')
    class Meta:
        model = Product
        fields = ('id', 'category', 'name', 'price')

    def create(self, validated_data):
        print(validated_data)
        product_data = validated_data.pop('category')
        print(product_data)

        #category = CategorySerializer.create(CategorySerializer(), validated_data = product_data)
        category = Category.objects.get(name = product_data)
        product, created = Product.objects.update_or_create(category = category,
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
    products = ProductHelperSerializer(many = True)
    class Meta:
        model = Category
        fields = ('id', 'name', 'products')

class CartSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(max_digits = 50, decimal_places = 2, read_only = True)
    order_items = ProductHelperSerializer
    items_ordered = serializers.CharField(read_only = True)
    class Meta:
        model = Cart
        fields = ['items_ordered', 'subtotal', 'order_items']

    def create(self, validated_data):
        print(validated_data)
        item = validated_data['order_items']
        print(type(item[0]))
        prod = Product.objects.get(name = item[0])
        instance = Cart.objects.create(subtotal = prod.price)
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
    class Meta:
        model = Checkout
        fields = ['cart', 'delivery_address', 'item_total_cost', 'delivery_charge', 'total']

    def create(self, validated_data):
        product_dicts = dict(itertools.islice(validated_data.items(), 4))
        for key in product_dicts.keys():
            validated_data.pop(key)
        checkout = Checkout.objects.create(**product_dicts)
        checkout.cart = validated_data
        checkout.save()
        return checkout

'''
class CategorySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name = 'category-detail')
    class Meta:
        model = Category
        fields = ('url', 'id', 'name')

'''
'''
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.HyperlinkedIdentityField()
'''

'''
class SlugRelatedModuleField(serializers.SlugRelatedField):

    def get_queryset(self):
        queryset =
'''
'''
class CategoryHelperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategoryRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CategoryDetailSerializer(serializers.ModelSerializer):
    category = CategoryHelperSerializer(read_only = True)
    #category = CategoryRelatedSerializer(read_only = True)
    def create(self,validated_data):
        return Product.objects.create(**validated_data)

    class Meta:
        model = Product
        fields = ('id', 'category', 'name', 'price')
'''
