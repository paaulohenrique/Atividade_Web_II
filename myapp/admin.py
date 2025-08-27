from django.contrib import admin
from .models import Client, Product, Order

class SoftDeleteAdmin(admin.ModelAdmin):
    """
    Admin base para aplicar soft delete em todos os modelos que herdam de BaseModel.
    """
    def delete_model(self, request, obj):
        obj.delete()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()

    def get_queryset(self, request):
        # Mostra todos os registros, inclusive deletados
        return self.model.all_objects.all()

@admin.register(Client)
class ClientAdmin(SoftDeleteAdmin):
    list_display = ('name', 'email', 'birth_date', 'created_at', 'updated_at', 'is_deleted')
    list_filter = ('is_deleted',)
    search_fields = ('name', 'email')


@admin.register(Product)
class ProductAdmin(SoftDeleteAdmin):
    list_display = ('name', 'price', 'created_at', 'updated_at', 'is_deleted')
    list_filter = ('is_deleted',)
    search_fields = ('name',)


@admin.register(Order)
class OrderAdmin(SoftDeleteAdmin):
    list_display = ('id', 'client', 'product', 'quantity', 'total_price', 'status', 'created_at', 'updated_at', 'is_deleted')
    list_filter = ('status', 'is_deleted')
    search_fields = ('client__name', 'product__name')
