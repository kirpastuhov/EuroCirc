from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager,
	)

class UserManager(BaseUserManager):
	def create_user(self, full_name, email, password=None, is_staff=False, is_admin=False, is_active=True):
		if not email: 
			raise ValueError("Users must have an email address")
		if not password:
			raise ValueError("Users must have password")
		user_obj = self.model(email = self.normalize_email(email),)
		user_obj.set_password(password)
		user_obj.active = is_active
		user_obj.staff = is_staff
		user_obj.admin = is_admin
		user_obj.full_name = full_name
		user_obj.save(using=self._db)
			
		return user_obj

	def create_staffuser(self, full_name, email, password=None):
		user = self.create_user(
			full_name = full_name,
			email=email,
			password = password,
			is_staff = True
			)
		return user
	def create_superuser(self, full_name, email, password=None):
		user = self.create_user(
			full_name = full_name,
			email=email,
			password = password,
			is_staff = True,
			is_admin = True
			)
		return user

class User(AbstractBaseUser):

	email = models.EmailField(max_length=255, unique=True)
	full_name = models.CharField(max_length=255, blank=True, null=True)
	active = models.BooleanField(default=True) # can login
	staff = models.BooleanField(default=False) # is staff
	admin = models.BooleanField(default=False) # is admin
	batch = models.IntegerField(default=0)
	gain = models.IntegerField(default=0)
	sold_share = models.IntegerField(default=0)
	sold_normal = models.IntegerField(default=0)
	sold_vacant = models.IntegerField(default=0)
	sold_500 = models.IntegerField(default=0)
	sold_700 = models.IntegerField(default=0)
	sold_800 = models.IntegerField(default=0)
	sold_900 = models.IntegerField(default=0)
	sold_1000 = models.IntegerField(default=0)
	sold_1200 = models.IntegerField(default=0)
	sold_1500 = models.IntegerField(default=0)




	timestamp = models.DateTimeField(auto_now_add=True)
	#sold_discount = models.IntegerField(default=0)



	USERNAME_FIELD = 'email'
	
	REQUIRED_FIELDS = ['full_name']

	objects = UserManager()

	def has_perm(self, perm, obj=None):
		return True
	def has_module_perms(self, app_label):
		return True

	@property
	def is_active(self):
		return self.active

	@property
	def is_staff(self):
		return self.staff

	@property
	def is_admin(self):
		return self.admin


class City(models.Model):
	city_name = models.CharField(max_length=255, default=None)

	def __str__(self):
		return str(self.city_name)

	def get_all_cities(self):
		all_cities = City.objects.all()
		context = {'all_cities': all_cities}
		return context

class Day(models.Model):

	city = models.ForeignKey(City, on_delete=models.CASCADE)
	date = models.DateTimeField(default=None)

	def __str__(self):
	    return 'Открытый день' + str(self.date) + 'Город    ' + str(self.city)

	def get_all_days(self, city_id):
	    all_days = (Day.objects.all().filter(city__id=int(city_id)))
	    print(all_days)
	    #all_days = all_days.sort(key=lambda r: r.date)
	    context = {'all_days':all_days}
	    return context



class Sector(models.Model):
	city = models.ForeignKey(City, on_delete=models.CASCADE)
	sector_number = models.IntegerField()
	date = models.DateTimeField()

	def __str__(self):
	    return str(self.sector_number) + 'СЕКТОР' + str(self.date)

	def get_all_rows(self):
	    return self.row_set.all()[::1]

	def get_sector(self, date, hour, sector_number, city_id):
		return Sector.objects.get(date__date=date, date__hour=hour, sector_number=sector_number, city__id=city_id)

	def get_all_sectors(self, date, hour, city_id):
	    all_sectors = []
	    for i in range(1, 6):
	        all_sectors.append(Sector.objects.get(date__date=date, date__hour=hour, sector_number=i, city__id=int(city_id)))
	    context = {'all_sectors':all_sectors}
	    return context


class Row(models.Model):
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    row_number = models.IntegerField()
    date = models.DateTimeField()

    def __str__(self):
        return str(self.sector.sector_number) + 'СЕКТОР :' +  str(self.row_number) + 'РЯД :' + str(self.date)

    def get_all_seats(self):
        pass


class Seat(models.Model):
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    row = models.ForeignKey(Row, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    price = models.IntegerField()
    selected = models.BooleanField(default=False)
    sold = models.CharField(max_length=50, default='Vacant')
    user_id = models.IntegerField(default=0)
    date = models.DateTimeField()
    #holder_name = models.CharField(max_length=1000, default=None, null=True, blank=True)

    def __str__(self):
        return str(self.row.sector.sector_number) + ' СЕКТОР, ' + str(self.row.row_number) + ' РЯД, ' + str(self.seat_number) + ' МЕСТО ' +  str(self.date)

    def get_all_selected_seats(self, id, date, hour, city_id):
       return Seat.objects.all().filter(date__date=date, date__hour=hour, sector__city__id=city_id,  user_id=id, selected=True)

    def get_all_seats(self, date, hour, sector):
        context = {}
        for row in range(1, 10):
            context['row_{0}'.format(row)] = Seat.objects.filter(date__date=date, date__hour=hour, sector__sector_number=sector, row__row_number=row)
        return context

    def get_all_free_seats(self, date, hour, city_id):
    	lens = []
    	for s in range(1, 6):
    		lens.append(len(Seat.objects.all().filter(sector__sector_number=s, date__date=date, date__hour=hour, sector__city__id=city_id, sold='Vacant')))

    	return lens


