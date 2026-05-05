from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    """
    Форма для создания заказа.
    Содержит поля для ввода контактной информации и адреса доставки.
    """
    
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите фамилию'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@email.com'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите адрес доставки'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Почтовый индекс'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Город'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (999) 123-45-67'}),
        }
    
    def clean_phone(self):
        """
        Валидация номера телефона.
        Удаляет все нецифровые символы и проверяет длину.
        """
        phone = self.cleaned_data['phone']
        # Удаляем все нецифровые символы
        phone_clean = ''.join(filter(str.isdigit, phone))
        
        if len(phone_clean) < 10:
            raise forms.ValidationError('Номер телефона должен содержать минимум 10 цифр.')
        
        return phone
    
    def clean_postal_code(self):
        """
        Валидация почтового индекса.
        Проверяет, что индекс содержит только цифры и имеет правильную длину.
        """
        postal_code = self.cleaned_data['postal_code']
        postal_code_clean = ''.join(filter(str.isdigit, postal_code))
        
        if len(postal_code_clean) != 6:
            raise forms.ValidationError('Почтовый индекс должен содержать 6 цифр.')
        
        return postal_code_clean
