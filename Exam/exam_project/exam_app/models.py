from django.db import models

class Сотрудники(models.Model):
    УИД_Сотрудника = models.AutoField(primary_key=True)
    Должность = models.TextField()


class Контрагенты(models.Model):
    УИД_Контрагента = models.AutoField(primary_key=True)
    Наименование = models.TextField()
    ИНН = models.CharField(max_length=12)
    Адрес = models.CharField(max_length=100)
    Телефон = models.CharField(max_length=11)
    Тип = models.TextField()

class Продукция(models.Model):
    УИД_Продукция = models.AutoField(primary_key=True)
    Наименование = models.CharField(max_length=50)
    Код = models.IntegerField()
    Единица_измерения = models.TextField()

class Спецификации(models.Model):
    УИД_Спецификации = models.AutoField(primary_key=True)
    Наименование = models.TextField()
    Утвердил_УИД = models.ForeignKey(Сотрудники, on_delete=models.CASCADE)
    Изготовитель_УИД = models.ForeignKey(Контрагенты, on_delete=models.CASCADE)
    Продукция_УИД = models.ForeignKey(Продукция, on_delete=models.CASCADE)

class Заказы_покупателей(models.Model):
    УИД_Заказ_покупателей = models.AutoField(primary_key=True)
    Номер = models.IntegerField()
    Дата = models.DateField()
    Исполнитель_УИД = models.ForeignKey(Контрагенты, on_delete=models.CASCADE, related_name='заказы_как_исполнитель')
    Заказчик_УИД = models.ForeignKey(Контрагенты, on_delete=models.CASCADE,related_name='заказы_как_заказчик')

class Заказы_на_производство(models.Model):
    УИД_Заказ_на_производство = models.AutoField(primary_key=True)
    Номер = models.IntegerField()
    Дата_запуска = models.DateField()
    Спецификация_УИД = models.ForeignKey(Спецификации, on_delete=models.CASCADE)
    Заказ_покупателя_УИД = models.ForeignKey(Заказы_покупателей, on_delete=models.CASCADE)
    Подразделение = models.CharField(max_length=50)

class Товары_в_заказах(models.Model):
    УИД_Товары = models.AutoField(primary_key=True)
    Заказ_покупателя_УИД = models.ForeignKey(Заказы_покупателей, on_delete=models.CASCADE)
    Продукция_УИД = models.ForeignKey(Продукция, on_delete=models.CASCADE)
    Количество = models.IntegerField()
    Цена = models.DecimalField(max_digits=10, decimal_places=2)
    Скидка = models.IntegerField()
    Сумма = models.DecimalField(max_digits=10, decimal_places=2)


class Материалы(models.Model):
    УИД_Материалы = models.AutoField(primary_key=True)
    Наименование = models.CharField(max_length=50)
    Код = models.IntegerField()
    Единица_измерения = models.TextField()

class Состав_спецификаций(models.Model):
    УИД_Состав_спецификаций = models.AutoField(primary_key=True)
    Материал_УИД = models.ForeignKey(Материалы, on_delete=models.CASCADE)
    Спецификация_УИД = models.ForeignKey(Спецификации, on_delete=models.CASCADE)
    Количество = models.IntegerField()

class Состав_производства(models.Model):
    УИД_Состав_производства = models.AutoField(primary_key=True)
    Материал_УИД = models.ForeignKey(Материалы, on_delete=models.CASCADE)
    Заказы_на_производство = models.ForeignKey(Заказы_на_производство, on_delete=models.CASCADE)
    Продукция_УИД = models.ForeignKey(Продукция, on_delete = models.CASCADE)
    Тип_записи = models.TextField()
    Количество = models.IntegerField()
    Цена = models.DecimalField(max_digits=10, decimal_places=2)
    Сумма = models.DecimalField(max_digits=10, decimal_places=2)

