# from rest_framework import serializers
# from .models import Product, Brand

# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = '__all__'




# class BrandSerializer(serializers.ModelSerializer):
#     products = ProductSerializer(source='product_set', many=True)

#     class Meta:
#         model = Brand
#         fields = ['id', 'name', 'slug', 'products']


from rest_framework import serializers
from .models import Product, Brand


# class ProductSerializer(serializers.ModelSerializer):

#     pdf = serializers.SerializerMethodField()

#     class Meta:
#         model = Product
#         fields = '__all__'

#     def get_pdf(self, obj):

#         if obj.pdf:
#             return obj.pdf.url

#         return ""


# class BrandSerializer(serializers.ModelSerializer):

#     products = ProductSerializer(source='product_set', many=True)

#     class Meta:
#         model = Brand
#         fields = ['id', 'name', 'slug', 'products']



class ProductSerializer(serializers.ModelSerializer):

    pdf = serializers.SerializerMethodField()

    image = serializers.SerializerMethodField()

    brand_name = serializers.CharField(source="brand.name", read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def get_pdf(self, obj):

        if obj.pdf:
            return obj.pdf.url

        return ""

    # def get_image(self, obj):
    #     request = self.context.get('request')

    #     if obj.image:
    #         return request.build_absolute_uri(obj.image.url)

    #     return ""
    def get_image(self, obj):

        if obj.image:
            return obj.image.url

        return ""

class BrandSerializer(serializers.ModelSerializer):

    products = ProductSerializer(source='product_set', many=True)

    class Meta:
        model = Brand
        fields = ['id', 'name', 'slug', 'products']