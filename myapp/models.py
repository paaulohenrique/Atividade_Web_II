from django.db import models
from django.utils import timezone
from myapp.managers import ActiveManager 


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # data de criação
    updated_at = models.DateTimeField(auto_now=True)      # data de atualização
    is_deleted = models.BooleanField(default=False)       # soft delete
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True  # não cria tabela no banco

    def delete(self, using=None, keep_parents=False):
        """Soft delete: marca como deletado em vez de remover"""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        """Restaura um item deletado"""
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    
class Client(BaseModel):  # agora herda do BaseModel
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    birth_date = models.DateField()

    objects = ActiveManager()       # só retorna registros ativos
    all_objects = models.Manager()  # retorna tudo (inclusive deletados)

    def __str__(self):
        return self.name

class Product(BaseModel):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    objects = ActiveManager()
    all_objects = models.Manager()

    def __str__(self):
        return self.name


class Order(BaseModel):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('enviado', 'Enviado'),
    ]

    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')

    objects = ActiveManager()
    all_objects = models.Manager()

    def save(self, *args, **kwargs):
        # Calcula automaticamente o total_price
        self.total_price = self.quantity * self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pedido {self.id} - {self.client.name}"