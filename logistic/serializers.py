from itertools import product
from pdb import post_mortem
from rest_framework import serializers
from .models import Product, StockProduct, Stock

class ProductSerializer(serializers.ModelSerializer):

    class Meta:

        model = Product
        fields = ['id','title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):

    class Meta:

        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):

    positions = ProductPositionSerializer(many=True)

    class Meta:

        model = Stock
        fields = ['positions', 'address']

    def create(self, validated_data):

        positions = validated_data.pop('positions')
        stock = super().create(validated_data)

        for i in positions:
            StockProduct.objects.create(stock=stock, **i)

        return stock

    def update(self, instance, validated_data):

        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)

        for position in positions:
            stock_product, create_tuple = StockProduct.objects.update_or_create(stock=stock, product=position['product'])
            stock_product.quantity = position['quantity']
            stock_product.price = position['price']
            stock_product.save()

        return stock
