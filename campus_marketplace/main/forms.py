from django import forms
from .models import Product, Category


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'slug', 'image', 'description', 'price', 'available']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_category(self):
        # Ensure users cannot create categories via the form — only select existing ones
        category = self.cleaned_data.get('category')
        if not Category.objects.filter(id=getattr(category, 'id', None)).exists():
            raise forms.ValidationError('Invalid category selected')
        return category

    def save(self, commit=True, seller=None):
        product = super().save(commit=False)
        if seller is not None:
            product.seller = seller
        if commit:
            product.save()
        return product
