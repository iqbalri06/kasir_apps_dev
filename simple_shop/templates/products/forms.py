class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'stock', 'description', 'image']
        widgets = {
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan harga',
                'min': '0',
                'step': '1'
            }),
            # ...other fields...
        }
