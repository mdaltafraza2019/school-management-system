from django.db import models

# Create your models here.
GENDER=(
    ('M','Male'),
    ('F','Female'),
    ('O','Other'),
)
CLASSLIST=(
    ('NUR','NUR'),
    ('LKG','LKG'),
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    ('6','6'),
    ('7','7'),
    ('8','8'),
    ('9','9'),
    ('10','10'),
    
)
MONTH=(
    ('january','january'),
    ('february','february'),
    ('march','march'),  
    ('aprial','aprial'),
    ('may','may'),
    ('june','june'),
    ('july','july'),
    ('august','august'),
    ('september','september'),
    ('october','october'),
    ('november','november'),
    ('december','december'),
)

class Classes(models.Model):
    class_name=models.CharField(max_length=30,choices=CLASSLIST)

    def __str__(self):
        return self.class_name

class Student(models.Model):
    name=models.CharField(max_length=100)
    father_name=models.CharField(max_length=100)
    contact=models.CharField(max_length=15)
    email=models.EmailField()
    address=models.CharField(max_length=100)
    nationalitly=models.CharField(max_length=100,choices=(("india","india"),("other","other")))
    state=models.CharField(max_length=100,choices=(('bihar','bihar'),('other','other')))
    city=models.CharField(max_length=100,choices=(('purnia','purnia'),('other','other')))
    gender=models.CharField(max_length=30,choices=GENDER)
    dob=models.DateField(help_text='use MM/DD/YYY' ,null=True,blank=True)
    pin=models.CharField(max_length=20)
    image=models.ImageField(upload_to='media',default=None,blank=True,null=True)
    className=models.ForeignKey('Classes',on_delete=models.CASCADE)
    isApproved=models.BooleanField(default=False)
    rf_code=models.CharField(max_length=100,blank=True,null=True,unique=True)
    

    def __str__(self):
        return self.name
    
class Payment(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    month=models.CharField(max_length=200,choices=MONTH)
    date_of_payment=models.DateTimeField(auto_now=False,null=True,blank=True)
    status=models.BooleanField(default=False)
    amount=models.IntegerField(default=1000)
    
    def __str__(self):
        return self.student.name+"-"+self.month