from .models import Student,Classes
from django.forms import ModelForm



class StudentForm(ModelForm):
    
    class Meta:
        model = Student
        fields = ("__all__")
        exclude =('isApproved','rf_code')

    
class Editstudent(ModelForm):
    class Meta:
        model=Student
        exclude=('isApproved',)


class ClassForm(ModelForm):
    
    class Meta:
        model = Classes
        fields = ("__all__")