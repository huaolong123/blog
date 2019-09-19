from django import forms

class Register(forms.Form):
    name = forms.CharField(max_length=8,min_length=3,label='用户名:')
    password = forms.CharField(max_length=32,label='密 码:',required=True)

    #  自定义校验，固定写法
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name == 'admin':
            self.add_error('name','不可以是admin')
        else:
            return name