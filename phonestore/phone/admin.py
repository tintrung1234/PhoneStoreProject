from django.contrib import admin
from .models import Category,Product, Order
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
  list_display = ("name",)

class ProductAdmin(admin.ModelAdmin):
  list_display = ("name",)
  def get_form(self, request, obj=None, **kwargs):
    form = super(ProductAdmin, self).get_form(request, obj, **kwargs)
    form.base_fields['name'].label_from_instance = lambda inst: "{} {}".format(inst.id, inst.first_name)
    return form



admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Order)

