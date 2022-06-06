from django.contrib import admin
from .models import Usuario
from django.urls import path
from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

# Register your models here.

class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'senha')
    search_field = ('nome', 'email')
    readonly_fields = ('senha',)
    
    def get_urls(self):
        urls=super().get_urls()
        new_urls=[path('upload-csv/',self.upload_csv),]
        return new_urls+urls

    def upload_csv(self,request):
       
        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]
            
            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)
            
            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")

            for x in csv_data:
                fields = x.split(",")
                created = Usuario.objects.update_or_create(
                    nome = fields[0],
                    email = fields[1],
                    senha = fields[2],
                    )
            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)   

admin.site.register(Usuario, UsuarioAdmin)