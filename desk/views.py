from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from .models import City, Day, Sector, Row, Seat, User
from django.http import HttpResponseRedirect, HttpResponse
import xlsxwriter
from string import ascii_uppercase
import io
import datetime
import pytz

class Index(LoginRequiredMixin, View):
    template_name = 'desk/index.html'
    def get(self, request, *arg, **kwargs):
        context = City.get_all_cities(self)
        return render(request, self.template_name, context)

class CreateCity(UserPassesTestMixin, LoginRequiredMixin, View):
    def test_func(self):
        return self.request.user.staff
    template_name = 'desk/create_city.html'

    def get(self, request, *arg, **kwargs):
        return render(request, self.template_name)
    def post(self, request, *arg, **kwargs):
        city_name = request.POST['city_name']
        try:
            City.objects.get(city_name=city_name)
            return HttpResponse('<h1>Такой день уже открыт.</>')
        except City.DoesNotExist:
            City(city_name=city_name).save()
            return HttpResponseRedirect('/')


class Days(LoginRequiredMixin, View):
    template_name = 'desk/days.html'

    def get(self, request, city_id, *arg, **kwargs):
        city_id = city_id
        city = City.objects.get(id=city_id)
        try:
            # context = Day.get_all_days(self, city_id)['all_days'].order_by(now, date)
            context = {}

            all_days = Day.objects.filter(city_id=city_id).order_by('-date')

            print(all_days)
            context["city_id"] = city_id
            context["city"] = city
            context["all_days"] = all_days
        except Day.DoesNotExist:
            context["city_id"] = city_id
            context["city"] = city
        return render(request, self.template_name, context)


class CreateDay(UserPassesTestMixin, LoginRequiredMixin, View):

    def test_func(self):
        return self.request.user.staff


    template_name = 'desk/create_day.html'

    def get(self, request, city_id, *arg,  **kwargs):
        context = {}
        context["city_id"] = city_id
        return render(request, self.template_name, context)

    def post(self, request, city_id, *arg, **kwargs):
        next = request.POST.get('next')
        def err_():
            Day.objects.get(date=creation_date,  city_id=city_id).delete()
            for each_sector in Sector.objects.filter(date=creation_date, city_id=city_id):
                each_sector.delete()
        creation_date = request.POST['date'] # get date that user posted in the form
        try:
            Day.objects.get(date=creation_date,  city_id=city_id)
            return HttpResponse('<h1>Такой день уже существует. Пожалуйста, выберите другую дату или удалите день с выбранной вами датой</h1>')
        except Day.DoesNotExist:
            Day(date=creation_date, city_id=city_id).save() # create a Day object in the db with posted date

            for s in range(1, 6):
                Sector(date=creation_date, sector_number=s, city_id=city_id).save()

            for each_sector in Sector.objects.filter(date=creation_date, city_id=city_id):
                if each_sector.sector_number != 5:
                    for r in range(1, 10):
                        print(r)
                        Row(sector=each_sector, row_number=r, date=creation_date).save()
                if each_sector.sector_number == 5:
                    for r in range(1, 7):
                        Row(sector=each_sector, row_number=r, date=creation_date).save()


            for each_row in Row.objects.filter(date=creation_date, sector__city_id=city_id, sector__sector_number=1):
                if each_row.row_number == 1:
                    try:
                        if int(request.POST.get('s_1_row_1_1').split(',')[0]) > 0 and int(request.POST.get('s_1_row_1_1').split(',')[1]) > 0:
                            for s in range(1, int(request.POST.get('s_1_row_1_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_1_row_1_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_1_row_1_2'):
                            if int(request.POST.get('s_1_row_1_2').split(',')[0]) > int(request.POST.get('s_1_row_1_1').split(',')[0]) and int(request.POST.get('s_1_row_1_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_1_row_1_1').split(',')[0])+1, int(request.POST.get('s_1_row_1_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_1_row_1_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_1_row_1_2') and request.POST.get('s_1_row_1_3'):
                            if int(request.POST.get('s_1_row_1_3').split(',')[0]) > int(request.POST.get('s_1_row_1_2').split(',')[0]) and int(request.POST.get('s_1_row_1_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_1_row_1_2').split(',')[0])+1, int(request.POST.get('s_1_row_1_3').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_1_row_1_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест ПЕРВЫЙ!</h1>')

                if each_row.row_number == 2:
                    try:
                        if int(request.POST.get('s_1_row_2_1').split(',')[0]) > 0 and int(request.POST.get('s_1_row_2_1').split(',')[1]) > 0:
                            for s in range(1, int(request.POST.get('s_1_row_2_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_1_row_2_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_1_row_2_2'):
                            if int(request.POST.get('s_1_row_2_2').split(',')[0]) > int(request.POST.get('s_1_row_2_1').split(',')[0]) and int(request.POST.get('s_1_row_2_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_1_row_2_1').split(',')[0])+1, int(request.POST.get('s_1_row_2_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_1_row_2_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_1_row_2_2') and request.POST.get('s_1_row_2_3'):
                            if int(request.POST.get('s_1_row_2_3').split(',')[0]) > int(request.POST.get('s_1_row_2_2').split(',')[0]) and int(request.POST.get('s_1_row_2_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_1_row_2_2').split(',')[0])+1, int(request.POST.get('s_1_row_2_3').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_1_row_2_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест ВТОРОЙ!</h1>')

                if each_row.row_number == 3:
                    try:
                        if int(request.POST.get('s_1_row_3_1').split(',')[0]) > 0 and int(request.POST.get('s_1_row_3_1').split(',')[1]) > 0:
                            for s in range(1, int(request.POST.get('s_1_row_3_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_1_row_3_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_1_row_3_2'):
                            if int(request.POST.get('s_1_row_3_2').split(',')[0]) > int(request.POST.get('s_1_row_3_1').split(',')[0]) and int(request.POST.get('s_1_row_3_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_1_row_3_1').split(',')[0])+1, int(request.POST.get('s_1_row_3_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_1_row_3_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_1_row_3_2') and request.POST.get('s_1_row_3_3'):
                            if int(request.POST.get('s_1_row_3_3').split(',')[0]) > int(request.POST.get('s_1_row_3_2').split(',')[0]) and int(request.POST.get('s_1_row_3_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_1_row_3_2').split(',')[0])+1, int(request.POST.get('s_1_row_3_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_1_row_3_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()


                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест ТРЕТИЙ!</h1>')


                if each_row.row_number == 4:
                    try:
                        if int(request.POST.get('s_1_row_4_1').split(',')[0]) > 0 and int(request.POST.get('s_1_row_4_1').split(',')[1]) > 0:
                            for s in range(1, int(request.POST.get('s_1_row_4_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_1_row_4_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_1_row_4_2'):
                            if int(request.POST.get('s_1_row_4_2').split(',')[0]) > int(request.POST.get('s_1_row_4_1').split(',')[0]) and int(request.POST.get('s_1_row_4_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_1_row_4_1').split(',')[0])+1, int(request.POST.get('s_1_row_4_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_1_row_4_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_1_row_4_2') and request.POST.get('s_1_row_4_3'):
                            if int(request.POST.get('s_1_row_4_3').split(',')[0]) > int(request.POST.get('s_1_row_4_2').split(',')[0]) and int(request.POST.get('s_1_row_4_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_1_row_4_2').split(',')[0])+1, int(request.POST.get('s_1_row_4_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_1_row_4_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест ТРЕТИЙ!</h1>')



                if each_row.row_number == 5:
                    print('WE ARE HERE')
                    try:
                        if int(request.POST.get('s_1_row_5_1').split(',')[0]) > 0 and int(request.POST.get('s_1_row_5_1').split(',')[1]) > 0:
                            for s in range(1, int(request.POST.get('s_1_row_5_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_1_row_5_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_1_row_5_2'):
                            if int(request.POST.get('s_1_row_5_2').split(',')[0]) > int(request.POST.get('s_1_row_5_1').split(',')[0]) and int(request.POST.get('s_1_row_5_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_1_row_5_1').split(',')[0])+1, int(request.POST.get('s_1_row_5_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_1_row_5_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_1_row_5_2') and request.POST.get('s_1_row_5_3'):
                            if int(request.POST.get('s_1_row_5_3').split(',')[0]) > int(request.POST.get('s_1_row_5_2').split(',')[0]) and int(request.POST.get('s_1_row_5_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_1_row_5_2').split(',')[0])+1, int(request.POST.get('s_1_row_5_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_1_row_5_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест 5 !</h1>')



                if each_row.row_number == 6:
                    print('WE ARE HERE')
                    try:
                        if int(request.POST.get('s_1_row_6_1').split(',')[0]) > 0 and int(request.POST.get('s_1_row_6_1').split(',')[1]) > 0:
                            for s in range(1, int(request.POST.get('s_1_row_6_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_1_row_6_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_1_row_6_2'):
                            if int(request.POST.get('s_1_row_6_2').split(',')[0]) > int(request.POST.get('s_1_row_6_1').split(',')[0]) and int(request.POST.get('s_1_row_6_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_1_row_6_1').split(',')[0])+1, int(request.POST.get('s_1_row_6_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_1_row_6_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_1_row_6_2') and request.POST.get('s_1_row_6_3'):
                            if int(request.POST.get('s_1_row_6_3').split(',')[0]) > int(request.POST.get('s_1_row_6_2').split(',')[0]) and int(request.POST.get('s_1_row_6_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_1_row_6_2').split(',')[0])+1, int(request.POST.get('s_1_row_6_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_1_row_6_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()


                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест 5 !</h1>')


                if each_row.row_number == 7:
                    print('WE ARE HERE')
                    try:
                        if int(request.POST.get('s_1_row_7_1').split(',')[0]) > 0 and int(request.POST.get('s_1_row_7_1').split(',')[1]) > 0:
                            for s in range(1, int(request.POST.get('s_1_row_7_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_1_row_7_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_1_row_7_2'):
                            if int(request.POST.get('s_1_row_7_2').split(',')[0]) > int(request.POST.get('s_1_row_7_1').split(',')[0]) and int(request.POST.get('s_1_row_7_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_1_row_7_1').split(',')[0])+1, int(request.POST.get('s_1_row_7_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_1_row_7_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_1_row_7_2') and request.POST.get('s_1_row_7_3'):
                            if int(request.POST.get('s_1_row_7_3').split(',')[0]) > int(request.POST.get('s_1_row_7_2').split(',')[0]) and int(request.POST.get('s_1_row_7_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_1_row_7_2').split(',')[0])+1, int(request.POST.get('s_1_row_7_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_1_row_7_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест 5 !</h1>')



                if each_row.row_number == 8:
                    print('WE ARE HERE')
                    try:
                        if int(request.POST.get('s_1_row_8_1').split(',')[0]) > 0 and int(request.POST.get('s_1_row_8_1').split(',')[1]) > 0:
                            for s in range(1, int(request.POST.get('s_1_row_8_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_1_row_8_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_1_row_8_2'):
                            if int(request.POST.get('s_1_row_8_2').split(',')[0]) > int(request.POST.get('s_1_row_8_1').split(',')[0]) and int(request.POST.get('s_1_row_8_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_1_row_8_1').split(',')[0])+1, int(request.POST.get('s_1_row_8_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_1_row_8_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_1_row_8_2') and request.POST.get('s_1_row_8_3'):
                            if int(request.POST.get('s_1_row_8_3').split(',')[0]) > int(request.POST.get('s_1_row_8_2').split(',')[0]) and int(request.POST.get('s_1_row_8_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_1_row_8_2').split(',')[0])+1, int(request.POST.get('s_1_row_8_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_1_row_8_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест 5 !</h1>')



                if each_row.row_number == 9:
                    print('WE ARE HERE')
                    try:
                        if int(request.POST.get('s_1_row_9_1').split(',')[0]) > 0 and int(request.POST.get('s_1_row_9_1').split(',')[1]) > 0:
                            for s in range(1, int(request.POST.get('s_1_row_9_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_1_row_9_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_1_row_9_2'):
                            if int(request.POST.get('s_1_row_9_2').split(',')[0]) > int(request.POST.get('s_1_row_9_1').split(',')[0]) and int(request.POST.get('s_1_row_9_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_1_row_9_1').split(',')[0])+1, int(request.POST.get('s_1_row_9_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_1_row_9_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_1_row_9_2') and request.POST.get('s_1_row_9_3'):
                            if int(request.POST.get('s_1_row_9_3').split(',')[0]) > int(request.POST.get('s_1_row_9_2').split(',')[0]) and int(request.POST.get('s_1_row_9_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_1_row_9_2').split(',')[0])+1, int(request.POST.get('s_1_row_9_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_1_row_9_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест 5 !</h1>')


        for each_row in Row.objects.filter(date=creation_date, sector__city_id=city_id, sector__sector_number=2):
                if each_row.row_number == 1:
                    try:
                        if int(request.POST.get('s_2_row_1_1').split(',')[0]) > 0 and int(request.POST.get('s_2_row_1_1').split(',')[1]) > 0:
                            for s in range(14, int(request.POST.get('s_2_row_1_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_2_row_1_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_2_row_1_2'):
                            if int(request.POST.get('s_2_row_1_2').split(',')[0]) > int(request.POST.get('s_2_row_1_1').split(',')[0]) and int(request.POST.get('s_2_row_1_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_2_row_1_1').split(',')[0])+1, int(request.POST.get('s_2_row_1_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_2_row_1_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_2_row_1_2') and request.POST.get('s_2_row_1_3'):
                            if int(request.POST.get('s_2_row_1_3').split(',')[0]) > int(request.POST.get('s_2_row_1_2').split(',')[0]) and int(request.POST.get('s_2_row_1_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_2_row_1_2').split(',')[0])+1, int(request.POST.get('s_2_row_1_3').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_2_row_1_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест ПЕРВЫЙ 2222!</h1>' + str(request.POST.get('s_2_row_1_3')) + str(request.POST.get('s_2_row_1_3')) + str(request.POST.get('s_2_row_1_3')))

                if each_row.row_number == 2:
                    try:
                        if int(request.POST.get('s_2_row_2_1').split(',')[0]) > 0 and int(request.POST.get('s_2_row_2_1').split(',')[1]) > 0:
                            for s in range(16, int(request.POST.get('s_2_row_2_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_2_row_2_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_2_row_2_2'):
                            if int(request.POST.get('s_2_row_2_2').split(',')[0]) > int(request.POST.get('s_2_row_2_1').split(',')[0]) and int(request.POST.get('s_2_row_2_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_2_row_2_1').split(',')[0])+1, int(request.POST.get('s_2_row_2_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_2_row_2_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_2_row_2_2') and request.POST.get('s_2_row_2_3'):
                            if int(request.POST.get('s_2_row_2_3').split(',')[0]) > int(request.POST.get('s_2_row_2_2').split(',')[0]) and int(request.POST.get('s_2_row_2_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_2_row_2_2').split(',')[0])+1, int(request.POST.get('s_2_row_2_3').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_2_row_2_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест ВТОРОЙ!</h1>')

                if each_row.row_number == 3:
                    try:
                        if int(request.POST.get('s_2_row_3_1').split(',')[0]) > 0 and int(request.POST.get('s_2_row_3_1').split(',')[1]) > 0:
                            for s in range(17, int(request.POST.get('s_2_row_3_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_2_row_3_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_2_row_3_2'):
                            if int(request.POST.get('s_2_row_3_2').split(',')[0]) > int(request.POST.get('s_2_row_3_1').split(',')[0]) and int(request.POST.get('s_2_row_3_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_2_row_3_1').split(',')[0])+1, int(request.POST.get('s_2_row_3_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_2_row_3_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_2_row_3_2') and request.POST.get('s_2_row_3_3'):
                            if int(request.POST.get('s_2_row_3_3').split(',')[0]) > int(request.POST.get('s_2_row_3_2').split(',')[0]) and int(request.POST.get('s_2_row_3_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_2_row_3_2').split(',')[0])+1, int(request.POST.get('s_2_row_3_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_2_row_3_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()


                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест ТРЕТИЙ!</h1>')


                if each_row.row_number == 4:
                    try:
                        if int(request.POST.get('s_2_row_4_1').split(',')[0]) > 0 and int(request.POST.get('s_2_row_4_1').split(',')[1]) > 0:
                            for s in range(19, int(request.POST.get('s_2_row_4_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_2_row_4_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_2_row_4_2'):
                            if int(request.POST.get('s_2_row_4_2').split(',')[0]) > int(request.POST.get('s_2_row_4_1').split(',')[0]) and int(request.POST.get('s_2_row_4_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_2_row_4_1').split(',')[0])+1, int(request.POST.get('s_2_row_4_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_2_row_4_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_2_row_4_2') and request.POST.get('s_2_row_4_3'):
                            if int(request.POST.get('s_2_row_4_3').split(',')[0]) > int(request.POST.get('s_2_row_4_2').split(',')[0]) and int(request.POST.get('s_2_row_4_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_2_row_4_2').split(',')[0])+1, int(request.POST.get('s_2_row_4_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_2_row_4_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест ТРЕТИЙ!</h1>')



                if each_row.row_number == 5:
                    print('WE ARE HERE')
                    try:
                        if int(request.POST.get('s_2_row_5_1').split(',')[0]) > 0 and int(request.POST.get('s_2_row_5_1').split(',')[1]) > 0:
                            for s in range(21, int(request.POST.get('s_2_row_5_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_2_row_5_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_2_row_5_2'):
                            if int(request.POST.get('s_2_row_5_2').split(',')[0]) > int(request.POST.get('s_2_row_5_1').split(',')[0]) and int(request.POST.get('s_2_row_5_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_2_row_5_1').split(',')[0])+1, int(request.POST.get('s_2_row_5_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_2_row_5_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_2_row_5_2') and request.POST.get('s_2_row_5_3'):
                            if int(request.POST.get('s_2_row_5_3').split(',')[0]) > int(request.POST.get('s_2_row_5_2').split(',')[0]) and int(request.POST.get('s_2_row_5_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_2_row_5_2').split(',')[0])+1, int(request.POST.get('s_2_row_5_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_2_row_5_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест 5 !</h1>')



                if each_row.row_number == 6:
                    print('WE ARE HERE')
                    try:
                        if int(request.POST.get('s_2_row_6_1').split(',')[0]) > 0 and int(request.POST.get('s_2_row_6_1').split(',')[1]) > 0:
                            for s in range(23, int(request.POST.get('s_2_row_6_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_2_row_6_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_2_row_6_2'):
                            if int(request.POST.get('s_2_row_6_2').split(',')[0]) > int(request.POST.get('s_2_row_6_1').split(',')[0]) and int(request.POST.get('s_2_row_6_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_2_row_6_1').split(',')[0])+1, int(request.POST.get('s_2_row_6_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_2_row_6_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_2_row_6_2') and request.POST.get('s_2_row_6_3'):
                            if int(request.POST.get('s_2_row_6_3').split(',')[0]) > int(request.POST.get('s_2_row_6_2').split(',')[0]) and int(request.POST.get('s_2_row_6_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_2_row_6_2').split(',')[0])+1, int(request.POST.get('s_2_row_6_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_2_row_6_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()


                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест 5 !</h1>')


                if each_row.row_number == 7:
                    print('WE ARE HERE')
                    try:
                        if int(request.POST.get('s_2_row_7_1').split(',')[0]) > 0 and int(request.POST.get('s_2_row_7_1').split(',')[1]) > 0:
                            for s in range(24, int(request.POST.get('s_2_row_7_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_2_row_7_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_2_row_7_2'):
                            if int(request.POST.get('s_2_row_7_2').split(',')[0]) > int(request.POST.get('s_2_row_7_1').split(',')[0]) and int(request.POST.get('s_2_row_7_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_2_row_7_1').split(',')[0])+1, int(request.POST.get('s_2_row_7_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_2_row_7_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_2_row_7_2') and request.POST.get('s_2_row_7_3'):
                            if int(request.POST.get('s_2_row_7_3').split(',')[0]) > int(request.POST.get('s_2_row_7_2').split(',')[0]) and int(request.POST.get('s_2_row_7_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_2_row_7_2').split(',')[0])+1, int(request.POST.get('s_2_row_7_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_2_row_7_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест 5 !</h1>')



                if each_row.row_number == 8:
                    print('WE ARE HERE')
                    try:
                        if int(request.POST.get('s_2_row_8_1').split(',')[0]) > 0 and int(request.POST.get('s_2_row_8_1').split(',')[1]) > 0:
                            for s in range(26, int(request.POST.get('s_2_row_8_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_2_row_8_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_2_row_8_2'):
                            if int(request.POST.get('s_2_row_8_2').split(',')[0]) > int(request.POST.get('s_2_row_8_1').split(',')[0]) and int(request.POST.get('s_2_row_8_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_2_row_8_1').split(',')[0])+1, int(request.POST.get('s_2_row_8_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_2_row_8_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_2_row_8_2') and request.POST.get('s_2_row_8_3'):
                            if int(request.POST.get('s_2_row_8_3').split(',')[0]) > int(request.POST.get('s_2_row_8_2').split(',')[0]) and int(request.POST.get('s_2_row_8_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_2_row_8_2').split(',')[0])+1, int(request.POST.get('s_2_row_8_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_2_row_8_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест 5 !</h1>')



                if each_row.row_number == 9:
                    print('WE ARE HERE')
                    try:
                        if int(request.POST.get('s_2_row_9_1').split(',')[0]) > 0 and int(request.POST.get('s_2_row_9_1').split(',')[1]) > 0:
                            for s in range(28, int(request.POST.get('s_2_row_9_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_2_row_9_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_2_row_9_2'):
                            if int(request.POST.get('s_2_row_9_2').split(',')[0]) > int(request.POST.get('s_2_row_9_1').split(',')[0]) and int(request.POST.get('s_2_row_9_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_2_row_9_1').split(',')[0])+1, int(request.POST.get('s_2_row_9_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_2_row_9_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_2_row_9_2') and request.POST.get('s_2_row_9_3'):
                            if int(request.POST.get('s_2_row_9_3').split(',')[0]) > int(request.POST.get('s_2_row_9_2').split(',')[0]) and int(request.POST.get('s_2_row_9_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_2_row_9_2').split(',')[0])+1, int(request.POST.get('s_2_row_9_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_2_row_9_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест 5 !</h1>')



        for each_row in Row.objects.filter(date=creation_date, sector__city_id=city_id, sector__sector_number=3):
                if each_row.row_number == 1:
                    try:
                        if int(request.POST.get('s_3_row_1_1').split(',')[0]) > 0 and int(request.POST.get('s_3_row_1_1').split(',')[1]) > 0:
                            for s in range(16, int(request.POST.get('s_3_row_1_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_3_row_1_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_3_row_1_2'):
                            if int(request.POST.get('s_3_row_1_2').split(',')[0]) > int(request.POST.get('s_3_row_1_1').split(',')[0]) and int(request.POST.get('s_3_row_1_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_3_row_1_1').split(',')[0])+1, int(request.POST.get('s_3_row_1_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_3_row_1_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_3_row_1_2') and request.POST.get('s_3_row_1_3'):
                            if int(request.POST.get('s_3_row_1_3').split(',')[0]) > int(request.POST.get('s_3_row_1_2').split(',')[0]) and int(request.POST.get('s_3_row_1_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_3_row_1_2').split(',')[0])+1, int(request.POST.get('s_3_row_1_3').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_3_row_1_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест ПЕРВЫЙ 333333!</h1>')

                if each_row.row_number == 2:
                    try:
                        if int(request.POST.get('s_3_row_2_1').split(',')[0]) > 0 and int(request.POST.get('s_3_row_2_1').split(',')[1]) > 0:
                            for s in range(18, int(request.POST.get('s_3_row_2_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_3_row_2_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_3_row_2_2'):
                            if int(request.POST.get('s_3_row_2_2').split(',')[0]) > int(request.POST.get('s_3_row_2_1').split(',')[0]) and int(request.POST.get('s_3_row_2_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_3_row_2_1').split(',')[0])+1, int(request.POST.get('s_3_row_2_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_3_row_2_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_3_row_2_2') and request.POST.get('s_3_row_2_3'):
                            if int(request.POST.get('s_3_row_2_3').split(',')[0]) > int(request.POST.get('s_3_row_2_2').split(',')[0]) and int(request.POST.get('s_3_row_2_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_3_row_2_2').split(',')[0])+1, int(request.POST.get('s_3_row_2_3').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_3_row_2_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест ВТОРОЙ!</h1>')

                if each_row.row_number == 3:
                    try:
                        if int(request.POST.get('s_3_row_3_1').split(',')[0]) > 0 and int(request.POST.get('s_3_row_3_1').split(',')[1]) > 0:
                            for s in range(20, int(request.POST.get('s_3_row_3_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_3_row_3_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_3_row_3_2'):
                            if int(request.POST.get('s_3_row_3_2').split(',')[0]) > int(request.POST.get('s_3_row_3_1').split(',')[0]) and int(request.POST.get('s_3_row_3_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_3_row_3_1').split(',')[0])+1, int(request.POST.get('s_3_row_3_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_3_row_3_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_3_row_3_2') and request.POST.get('s_3_row_3_3'):
                            if int(request.POST.get('s_3_row_3_3').split(',')[0]) > int(request.POST.get('s_3_row_3_2').split(',')[0]) and int(request.POST.get('s_3_row_3_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_3_row_3_2').split(',')[0])+1, int(request.POST.get('s_3_row_3_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_3_row_3_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()


                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест ТРЕТИЙ!</h1>')


                if each_row.row_number == 4:
                    try:
                        if int(request.POST.get('s_3_row_4_1').split(',')[0]) > 0 and int(request.POST.get('s_3_row_4_1').split(',')[1]) > 0:
                            for s in range(22, int(request.POST.get('s_3_row_4_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_3_row_4_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_3_row_4_2'):
                            if int(request.POST.get('s_3_row_4_2').split(',')[0]) > int(request.POST.get('s_3_row_4_1').split(',')[0]) and int(request.POST.get('s_3_row_4_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_3_row_4_1').split(',')[0])+1, int(request.POST.get('s_3_row_4_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_3_row_4_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_3_row_4_2') and request.POST.get('s_3_row_4_3'):
                            if int(request.POST.get('s_3_row_4_3').split(',')[0]) > int(request.POST.get('s_3_row_4_2').split(',')[0]) and int(request.POST.get('s_3_row_4_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_3_row_4_2').split(',')[0])+1, int(request.POST.get('s_3_row_4_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_3_row_4_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест ТРЕТИЙ!</h1>')



                if each_row.row_number == 5:
                    print('WE ARE HERE')
                    try:
                        if int(request.POST.get('s_3_row_5_1').split(',')[0]) > 0 and int(request.POST.get('s_3_row_5_1').split(',')[1]) > 0:
                            for s in range(24, int(request.POST.get('s_3_row_5_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_3_row_5_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_3_row_5_2'):
                            if int(request.POST.get('s_3_row_5_2').split(',')[0]) > int(request.POST.get('s_3_row_5_1').split(',')[0]) and int(request.POST.get('s_3_row_5_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_3_row_5_1').split(',')[0])+1, int(request.POST.get('s_3_row_5_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_3_row_5_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_3_row_5_2') and request.POST.get('s_3_row_5_3'):
                            if int(request.POST.get('s_3_row_5_3').split(',')[0]) > int(request.POST.get('s_3_row_5_2').split(',')[0]) and int(request.POST.get('s_3_row_5_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_3_row_5_2').split(',')[0])+1, int(request.POST.get('s_3_row_5_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_3_row_5_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест 5 !</h1>')



                if each_row.row_number == 6:
                    print('WE ARE HERE')
                    try:
                        if int(request.POST.get('s_3_row_6_1').split(',')[0]) > 0 and int(request.POST.get('s_3_row_6_1').split(',')[1]) > 0:
                            for s in range(26, int(request.POST.get('s_3_row_6_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_3_row_6_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_3_row_6_2'):
                            if int(request.POST.get('s_3_row_6_2').split(',')[0]) > int(request.POST.get('s_3_row_6_1').split(',')[0]) and int(request.POST.get('s_3_row_6_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_3_row_6_1').split(',')[0])+1, int(request.POST.get('s_3_row_6_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_3_row_6_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_3_row_6_2') and request.POST.get('s_3_row_6_3'):
                            if int(request.POST.get('s_3_row_6_3').split(',')[0]) > int(request.POST.get('s_3_row_6_2').split(',')[0]) and int(request.POST.get('s_3_row_6_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_3_row_6_2').split(',')[0])+1, int(request.POST.get('s_3_row_6_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_3_row_6_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()


                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест 5 !</h1>')


                if each_row.row_number == 7:
                    print('WE ARE HERE')
                    try:
                        if int(request.POST.get('s_3_row_7_1').split(',')[0]) > 0 and int(request.POST.get('s_3_row_7_1').split(',')[1]) > 0:
                            for s in range(28, int(request.POST.get('s_3_row_7_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_3_row_7_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_3_row_7_2'):
                            if int(request.POST.get('s_3_row_7_2').split(',')[0]) > int(request.POST.get('s_3_row_7_1').split(',')[0]) and int(request.POST.get('s_3_row_7_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_3_row_7_1').split(',')[0])+1, int(request.POST.get('s_3_row_7_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_3_row_7_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_3_row_7_2') and request.POST.get('s_3_row_7_3'):
                            if int(request.POST.get('s_3_row_7_3').split(',')[0]) > int(request.POST.get('s_3_row_7_2').split(',')[0]) and int(request.POST.get('s_3_row_7_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_3_row_7_2').split(',')[0])+1, int(request.POST.get('s_3_row_7_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_3_row_7_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест 5 !</h1>')



                if each_row.row_number == 8:
                    print('WE ARE HERE')
                    try:
                        if int(request.POST.get('s_3_row_8_1').split(',')[0]) > 0 and int(request.POST.get('s_3_row_8_1').split(',')[1]) > 0:
                            for s in range(30, int(request.POST.get('s_3_row_8_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_3_row_8_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_3_row_8_2'):
                            if int(request.POST.get('s_3_row_8_2').split(',')[0]) > int(request.POST.get('s_3_row_8_1').split(',')[0]) and int(request.POST.get('s_3_row_8_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_3_row_8_1').split(',')[0])+1, int(request.POST.get('s_3_row_8_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_3_row_8_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_3_row_8_2') and request.POST.get('s_3_row_8_3'):
                            if int(request.POST.get('s_3_row_8_3').split(',')[0]) > int(request.POST.get('s_3_row_8_2').split(',')[0]) and int(request.POST.get('s_3_row_8_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_3_row_8_2').split(',')[0])+1, int(request.POST.get('s_3_row_8_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_3_row_8_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест 5 !</h1>')



                if each_row.row_number == 9:
                    print('WE ARE HERE')
                    try:
                        if int(request.POST.get('s_3_row_9_1').split(',')[0]) > 0 and int(request.POST.get('s_3_row_9_1').split(',')[1]) > 0:
                            for s in range(32, int(request.POST.get('s_3_row_9_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_3_row_9_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_3_row_9_2'):
                            if int(request.POST.get('s_3_row_9_2').split(',')[0]) > int(request.POST.get('s_3_row_9_1').split(',')[0]) and int(request.POST.get('s_3_row_9_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_3_row_9_1').split(',')[0])+1, int(request.POST.get('s_3_row_9_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_3_row_9_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_3_row_9_2') and request.POST.get('s_3_row_9_3'):
                            if int(request.POST.get('s_3_row_9_3').split(',')[0]) > int(request.POST.get('s_3_row_9_2').split(',')[0]) and int(request.POST.get('s_3_row_9_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_3_row_9_2').split(',')[0])+1, int(request.POST.get('s_3_row_9_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_3_row_9_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест 5 !</h1>')



        for each_row in Row.objects.filter(date=creation_date, sector__city_id=city_id, sector__sector_number=4):
                if each_row.row_number == 1:
                    try:
                        if int(request.POST.get('s_4_row_1_1').split(',')[0]) > 0 and int(request.POST.get('s_4_row_1_1').split(',')[1]) > 0:
                            for s in range(1, int(request.POST.get('s_4_row_1_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_4_row_1_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_4_row_1_2'):
                            if int(request.POST.get('s_4_row_1_2').split(',')[0]) > int(request.POST.get('s_4_row_1_1').split(',')[0]) and int(request.POST.get('s_4_row_1_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_4_row_1_1').split(',')[0])+1, int(request.POST.get('s_4_row_1_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_4_row_1_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_4_row_1_2') and request.POST.get('s_4_row_1_3'):
                            if int(request.POST.get('s_4_row_1_3').split(',')[0]) > int(request.POST.get('s_4_row_1_2').split(',')[0]) and int(request.POST.get('s_4_row_1_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_4_row_1_2').split(',')[0])+1, int(request.POST.get('s_4_row_1_3').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_4_row_1_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест ПЕРВЫЙ 444444!</h1>')

                if each_row.row_number == 2:
                    try:
                        if int(request.POST.get('s_4_row_2_1').split(',')[0]) > 0 and int(request.POST.get('s_4_row_2_1').split(',')[1]) > 0:
                            for s in range(1, int(request.POST.get('s_4_row_2_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_4_row_2_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_4_row_2_2'):
                            if int(request.POST.get('s_4_row_2_2').split(',')[0]) > int(request.POST.get('s_4_row_2_1').split(',')[0]) and int(request.POST.get('s_4_row_2_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_4_row_2_1').split(',')[0])+1, int(request.POST.get('s_4_row_2_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_4_row_2_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_4_row_2_2') and request.POST.get('s_4_row_2_3'):
                            if int(request.POST.get('s_4_row_2_3').split(',')[0]) > int(request.POST.get('s_4_row_2_2').split(',')[0]) and int(request.POST.get('s_4_row_2_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_4_row_2_2').split(',')[0])+1, int(request.POST.get('s_4_row_2_3').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_4_row_2_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест ВТОРОЙ!</h1>')

                if each_row.row_number == 3:
                    try:
                        if int(request.POST.get('s_4_row_3_1').split(',')[0]) > 0 and int(request.POST.get('s_4_row_3_1').split(',')[1]) > 0:
                            for s in range(1, int(request.POST.get('s_4_row_3_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_4_row_3_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_4_row_3_2'):
                            if int(request.POST.get('s_4_row_3_2').split(',')[0]) > int(request.POST.get('s_4_row_3_1').split(',')[0]) and int(request.POST.get('s_4_row_3_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_4_row_3_1').split(',')[0])+1, int(request.POST.get('s_4_row_3_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_4_row_3_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_4_row_3_2') and request.POST.get('s_4_row_3_3'):
                            if int(request.POST.get('s_4_row_3_3').split(',')[0]) > int(request.POST.get('s_4_row_3_2').split(',')[0]) and int(request.POST.get('s_4_row_3_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_4_row_3_2').split(',')[0])+1, int(request.POST.get('s_4_row_3_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_4_row_3_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()


                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест ТРЕТИЙ!</h1>')


                if each_row.row_number == 4:
                    try:
                        if int(request.POST.get('s_4_row_4_1').split(',')[0]) > 0 and int(request.POST.get('s_4_row_4_1').split(',')[1]) > 0:
                            for s in range(1, int(request.POST.get('s_4_row_4_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_4_row_4_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_4_row_4_2'):
                            if int(request.POST.get('s_4_row_4_2').split(',')[0]) > int(request.POST.get('s_4_row_4_1').split(',')[0]) and int(request.POST.get('s_4_row_4_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_4_row_4_1').split(',')[0])+1, int(request.POST.get('s_4_row_4_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_4_row_4_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_4_row_4_2') and request.POST.get('s_4_row_4_3'):
                            if int(request.POST.get('s_4_row_4_3').split(',')[0]) > int(request.POST.get('s_4_row_4_2').split(',')[0]) and int(request.POST.get('s_4_row_4_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_4_row_4_2').split(',')[0])+1, int(request.POST.get('s_4_row_4_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_4_row_4_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест ТРЕТИЙ!</h1>')



                if each_row.row_number == 5:
                    print('WE ARE HERE')
                    try:
                        if int(request.POST.get('s_4_row_5_1').split(',')[0]) > 0 and int(request.POST.get('s_4_row_5_1').split(',')[1]) > 0:
                            for s in range(1, int(request.POST.get('s_4_row_5_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_4_row_5_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_4_row_5_2'):
                            if int(request.POST.get('s_4_row_5_2').split(',')[0]) > int(request.POST.get('s_4_row_5_1').split(',')[0]) and int(request.POST.get('s_4_row_5_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_4_row_5_1').split(',')[0])+1, int(request.POST.get('s_4_row_5_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_4_row_5_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_4_row_5_2') and request.POST.get('s_4_row_5_3'):
                            if int(request.POST.get('s_4_row_5_3').split(',')[0]) > int(request.POST.get('s_4_row_5_2').split(',')[0]) and int(request.POST.get('s_4_row_5_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_4_row_5_2').split(',')[0])+1, int(request.POST.get('s_4_row_5_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_4_row_5_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест 5 !</h1>')



                if each_row.row_number == 6:
                    print('WE ARE HERE')
                    try:
                        if int(request.POST.get('s_4_row_6_1').split(',')[0]) > 0 and int(request.POST.get('s_4_row_6_1').split(',')[1]) > 0:
                            for s in range(1, int(request.POST.get('s_4_row_6_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_4_row_6_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_4_row_6_2'):
                            if int(request.POST.get('s_4_row_6_2').split(',')[0]) > int(request.POST.get('s_4_row_6_1').split(',')[0]) and int(request.POST.get('s_4_row_6_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_4_row_6_1').split(',')[0])+1, int(request.POST.get('s_4_row_6_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_4_row_6_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_4_row_6_2') and request.POST.get('s_4_row_6_3'):
                            if int(request.POST.get('s_4_row_6_3').split(',')[0]) > int(request.POST.get('s_4_row_6_2').split(',')[0]) and int(request.POST.get('s_4_row_6_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_4_row_6_2').split(',')[0])+1, int(request.POST.get('s_4_row_6_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_4_row_6_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()


                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест 5 !</h1>')


                if each_row.row_number == 7:
                    print('WE ARE HERE')
                    try:
                        if int(request.POST.get('s_4_row_7_1').split(',')[0]) > 0 and int(request.POST.get('s_4_row_7_1').split(',')[1]) > 0:
                            for s in range(1, int(request.POST.get('s_4_row_7_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_4_row_7_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_4_row_7_2'):
                            if int(request.POST.get('s_4_row_7_2').split(',')[0]) > int(request.POST.get('s_4_row_7_1').split(',')[0]) and int(request.POST.get('s_4_row_7_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_4_row_7_1').split(',')[0])+1, int(request.POST.get('s_4_row_7_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_4_row_7_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_4_row_7_2') and request.POST.get('s_4_row_7_3'):
                            if int(request.POST.get('s_4_row_7_3').split(',')[0]) > int(request.POST.get('s_4_row_7_2').split(',')[0]) and int(request.POST.get('s_4_row_7_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_4_row_7_2').split(',')[0])+1, int(request.POST.get('s_4_row_7_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_4_row_7_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест 5 !</h1>')



                if each_row.row_number == 8:
                    print('WE ARE HERE')
                    try:
                        if int(request.POST.get('s_4_row_8_1').split(',')[0]) > 0 and int(request.POST.get('s_4_row_8_1').split(',')[1]) > 0:
                            for s in range(1, int(request.POST.get('s_4_row_8_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_4_row_8_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_4_row_8_2'):
                            if int(request.POST.get('s_4_row_8_2').split(',')[0]) > int(request.POST.get('s_4_row_8_1').split(',')[0]) and int(request.POST.get('s_4_row_8_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_4_row_8_1').split(',')[0])+1, int(request.POST.get('s_4_row_8_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_4_row_8_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_4_row_8_2') and request.POST.get('s_4_row_8_3'):
                            if int(request.POST.get('s_4_row_8_3').split(',')[0]) > int(request.POST.get('s_4_row_8_2').split(',')[0]) and int(request.POST.get('s_4_row_8_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_4_row_8_2').split(',')[0])+1, int(request.POST.get('s_4_row_8_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_4_row_8_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест 5 !</h1>')



                if each_row.row_number == 9:
                    print('WE ARE HERE')
                    try:
                        if int(request.POST.get('s_4_row_9_1').split(',')[0]) > 0 and int(request.POST.get('s_4_row_9_1').split(',')[1]) > 0:
                            for s in range(1, int(request.POST.get('s_4_row_9_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_4_row_9_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_4_row_9_2'):
                            if int(request.POST.get('s_4_row_9_2').split(',')[0]) > int(request.POST.get('s_4_row_9_1').split(',')[0]) and int(request.POST.get('s_4_row_9_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_4_row_9_1').split(',')[0])+1, int(request.POST.get('s_4_row_9_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_4_row_9_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_4_row_9_2') and request.POST.get('s_4_row_9_3'):
                            if int(request.POST.get('s_4_row_9_3').split(',')[0]) > int(request.POST.get('s_4_row_9_2').split(',')[0]) and int(request.POST.get('s_4_row_9_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_4_row_9_2').split(',')[0])+1, int(request.POST.get('s_4_row_9_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_4_row_9_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест 5 !</h1>')



        for each_row in Row.objects.filter(date=creation_date, sector__city_id=city_id, sector__sector_number=5):
                if each_row.row_number == 1:
                    try:
                        if int(request.POST.get('s_5_row_1_1').split(',')[0]) > 0 and int(request.POST.get('s_5_row_1_1').split(',')[1]) > 0:
                            for s in range(1, int(request.POST.get('s_5_row_1_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_5_row_1_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_5_row_1_2'):
                            if int(request.POST.get('s_5_row_1_2').split(',')[0]) > int(request.POST.get('s_5_row_1_1').split(',')[0]) and int(request.POST.get('s_5_row_1_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_5_row_1_1').split(',')[0])+1, int(request.POST.get('s_5_row_1_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_5_row_1_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_5_row_1_2') and request.POST.get('s_5_row_1_3'):
                            if int(request.POST.get('s_5_row_1_3').split(',')[0]) > int(request.POST.get('s_5_row_1_2').split(',')[0]) and int(request.POST.get('s_5_row_1_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_5_row_1_2').split(',')[0])+1, int(request.POST.get('s_5_row_1_3').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_5_row_1_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест ПЕРВЫЙ 5555!</h1>')

                if each_row.row_number == 2:
                    try:
                        if int(request.POST.get('s_5_row_2_1').split(',')[0]) > 0 and int(request.POST.get('s_5_row_2_1').split(',')[1]) > 0:
                            for s in range(1, int(request.POST.get('s_5_row_2_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_5_row_2_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_5_row_2_2'):
                            if int(request.POST.get('s_5_row_2_2').split(',')[0]) > int(request.POST.get('s_5_row_2_1').split(',')[0]) and int(request.POST.get('s_5_row_2_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_5_row_2_1').split(',')[0])+1, int(request.POST.get('s_5_row_2_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_5_row_2_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_5_row_2_2') and request.POST.get('s_5_row_2_3'):
                            if int(request.POST.get('s_5_row_2_3').split(',')[0]) > int(request.POST.get('s_5_row_2_2').split(',')[0]) and int(request.POST.get('s_5_row_2_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_5_row_2_2').split(',')[0])+1, int(request.POST.get('s_5_row_2_3').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_5_row_2_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест ВТОРОЙ!</h1>')

                if each_row.row_number == 3:
                    try:
                        if int(request.POST.get('s_5_row_3_1').split(',')[0]) > 0 and int(request.POST.get('s_5_row_3_1').split(',')[1]) > 0:
                            for s in range(1, int(request.POST.get('s_5_row_3_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_5_row_3_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_5_row_3_2'):
                            if int(request.POST.get('s_5_row_3_2').split(',')[0]) > int(request.POST.get('s_5_row_3_1').split(',')[0]) and int(request.POST.get('s_5_row_3_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_5_row_3_1').split(',')[0])+1, int(request.POST.get('s_5_row_3_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_5_row_3_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_5_row_3_2') and request.POST.get('s_5_row_3_3'):
                            if int(request.POST.get('s_5_row_3_3').split(',')[0]) > int(request.POST.get('s_5_row_3_2').split(',')[0]) and int(request.POST.get('s_5_row_3_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_5_row_3_2').split(',')[0])+1, int(request.POST.get('s_5_row_3_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_5_row_3_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()


                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест ТРЕТИЙ!</h1>')


                if each_row.row_number == 4:
                    try:
                        if int(request.POST.get('s_5_row_4_1').split(',')[0]) > 0 and int(request.POST.get('s_5_row_4_1').split(',')[1]) > 0:
                            for s in range(1, int(request.POST.get('s_5_row_4_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_5_row_4_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_5_row_4_2'):
                            if int(request.POST.get('s_5_row_4_2').split(',')[0]) > int(request.POST.get('s_5_row_4_1').split(',')[0]) and int(request.POST.get('s_5_row_4_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_5_row_4_1').split(',')[0])+1, int(request.POST.get('s_5_row_4_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_5_row_4_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_5_row_4_2') and request.POST.get('s_5_row_4_3'):
                            if int(request.POST.get('s_5_row_4_3').split(',')[0]) > int(request.POST.get('s_5_row_4_2').split(',')[0]) and int(request.POST.get('s_5_row_4_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_5_row_4_2').split(',')[0])+1, int(request.POST.get('s_5_row_4_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_5_row_4_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест ТРЕТИЙ!</h1>')



                if each_row.row_number == 5:
                    print('WE ARE HERE')
                    try:
                        if int(request.POST.get('s_5_row_5_1').split(',')[0]) > 0 and int(request.POST.get('s_5_row_5_1').split(',')[1]) > 0:
                            for s in range(1, int(request.POST.get('s_5_row_5_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_5_row_5_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_5_row_5_2'):
                            if int(request.POST.get('s_5_row_5_2').split(',')[0]) > int(request.POST.get('s_5_row_5_1').split(',')[0]) and int(request.POST.get('s_5_row_5_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_5_row_5_1').split(',')[0])+1, int(request.POST.get('s_5_row_5_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_5_row_5_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_5_row_5_2') and request.POST.get('s_5_row_5_3'):
                            if int(request.POST.get('s_5_row_5_3').split(',')[0]) > int(request.POST.get('s_5_row_5_2').split(',')[0]) and int(request.POST.get('s_5_row_5_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_5_row_5_2').split(',')[0])+1, int(request.POST.get('s_5_row_5_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_5_row_5_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест 5 !</h1>')



                if each_row.row_number == 6:
                    print('WE ARE HERE')
                    try:
                        if int(request.POST.get('s_5_row_6_1').split(',')[0]) > 0 and int(request.POST.get('s_5_row_6_1').split(',')[1]) > 0:
                            for s in range(1, int(request.POST.get('s_5_row_6_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_5_row_6_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_5_row_6_2'):
                            if int(request.POST.get('s_5_row_6_2').split(',')[0]) > int(request.POST.get('s_5_row_6_1').split(',')[0]) and int(request.POST.get('s_5_row_6_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_5_row_6_1').split(',')[0])+1, int(request.POST.get('s_5_row_6_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_5_row_6_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_5_row_6_2') and request.POST.get('s_5_row_6_3'):
                            if int(request.POST.get('s_5_row_6_3').split(',')[0]) > int(request.POST.get('s_5_row_6_2').split(',')[0]) and int(request.POST.get('s_5_row_6_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_5_row_6_2').split(',')[0])+1, int(request.POST.get('s_5_row_6_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_5_row_6_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()


                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест 5 !</h1>')


                if each_row.row_number == 7:
                    print('WE ARE HERE')
                    try:
                        if int(request.POST.get('s_5_row_7_1').split(',')[0]) > 0 and int(request.POST.get('s_5_row_7_1').split(',')[1]) > 0:
                            for s in range(1, int(request.POST.get('s_5_row_7_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_5_row_7_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_5_row_7_2'):
                            if int(request.POST.get('s_5_row_7_2').split(',')[0]) > int(request.POST.get('s_5_row_7_1').split(',')[0]) and int(request.POST.get('s_5_row_7_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_5_row_7_1').split(',')[0])+1, int(request.POST.get('s_5_row_7_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_5_row_7_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_5_row_7_2') and request.POST.get('s_5_row_7_3'):
                            if int(request.POST.get('s_5_row_7_3').split(',')[0]) > int(request.POST.get('s_5_row_7_2').split(',')[0]) and int(request.POST.get('s_5_row_7_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_5_row_7_2').split(',')[0])+1, int(request.POST.get('s_5_row_7_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_5_row_7_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест 5 !</h1>')



                if each_row.row_number == 8:
                    print('WE ARE HERE')
                    try:
                        if int(request.POST.get('s_5_row_8_1').split(',')[0]) > 0 and int(request.POST.get('s_5_row_8_1').split(',')[1]) > 0:
                            for s in range(1, int(request.POST.get('s_5_row_8_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_5_row_8_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_5_row_8_2'):
                            if int(request.POST.get('s_5_row_8_2').split(',')[0]) > int(request.POST.get('s_5_row_8_1').split(',')[0]) and int(request.POST.get('s_5_row_8_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_5_row_8_1').split(',')[0])+1, int(request.POST.get('s_5_row_8_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_5_row_8_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_5_row_8_2') and request.POST.get('s_5_row_8_3'):
                            if int(request.POST.get('s_5_row_8_3').split(',')[0]) > int(request.POST.get('s_5_row_8_2').split(',')[0]) and int(request.POST.get('s_5_row_8_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_5_row_8_2').split(',')[0])+1, int(request.POST.get('s_5_row_8_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_5_row_8_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест 5 !</h1>')



                if each_row.row_number == 9:
                    print('WE ARE HERE')
                    try:
                        if int(request.POST.get('s_5_row_9_1').split(',')[0]) > 0 and int(request.POST.get('s_5_row_9_1').split(',')[1]) > 0:
                            for s in range(1, int(request.POST.get('s_5_row_9_1').split(',')[0])+1):
                                Seat( seat_number = s, price = int(request.POST.get('s_5_row_9_1').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if request.POST.get('s_5_row_9_2'):
                            if int(request.POST.get('s_5_row_9_2').split(',')[0]) > int(request.POST.get('s_5_row_9_1').split(',')[0]) and int(request.POST.get('s_5_row_9_2').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_5_row_9_1').split(',')[0])+1, int(request.POST.get('s_5_row_9_2').split(',')[0])+1):
                                    Seat( seat_number =k, price = int(request.POST.get('s_5_row_9_2').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()
                        if request.POST.get('s_5_row_9_2') and request.POST.get('s_5_row_9_3'):
                            if int(request.POST.get('s_5_row_9_3').split(',')[0]) > int(request.POST.get('s_5_row_9_2').split(',')[0]) and int(request.POST.get('s_5_row_9_3').split(',')[1]) > 0:
                                for k in range(int(request.POST.get('s_5_row_9_2').split(',')[0])+1, int(request.POST.get('s_5_row_9_3').split(',')[0])+1):
                                    Seat( seat_number=k, price = int(request.POST.get('s_5_row_9_3').split(',')[1]), sector = each_row.sector,  row=each_row, date=creation_date ).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест 5 !</h1>')

        return HttpResponseRedirect(next)



class Odeum(LoginRequiredMixin, View):
    template_name = 'desk/odeum.html'
    def get(self, request, city_id, *arg, **kwargs):
        seat_given = Seat.objects.all().filter(date__date=self.kwargs['date'], date__hour=self.kwargs['hour'], sold='Local_cashdesks', sector__city__id=city_id)
        seat_vacant = Seat.objects.all().filter(date__date=self.kwargs['date'], date__hour=self.kwargs['hour'], sold='Vacant', sector__city__id=city_id)
        seat_sold = Seat.objects.all().filter(date__date=self.kwargs['date'], date__hour=self.kwargs['hour'], sold='Sold', sector__city__id=city_id)
        seat_share = Seat.objects.all().filter(date__date=self.kwargs['date'], date__hour=self.kwargs['hour'], sold='Share', sector__city__id=city_id)
        #seat_discount = Seat.objects.all().filter(date__date=date, date__hour=hour, sold='Discount')
        seat_free = Seat.objects.all().filter(date__date=self.kwargs['date'], date__hour=self.kwargs['hour'], sold='Free', sector__city__id=city_id)
        gain_total = 0
        gain_sold = 0
        gain_share = 0
        gain_discount = 0
        for seat in seat_sold:
            gain_sold = gain_sold + seat.price
        #for seat in seat_discount:
            #gain_discount = gain_discount + seat.price*0.8
        for seat in seat_share:
            gain_share = gain_share + 1
        for seat in seat_given:
        	gain_sold = gain_sold + seat.price
        gain_total = gain_sold


        count_share = len(seat_share)
        count_sold = len(seat_sold)
        #count_discount = len(seat_discount)
        count_free = len(seat_free)
        count_vacant = len(seat_vacant)
        if len(seat_vacant) != 0 :
            stat = int(((828 - len(seat_vacant))/828)*100)
        elif len(seat_vacant) == 0:
            stat = 100

        if count_sold !=0:
            gain_sold_pr = int(((count_sold)/828)*100)

        elif count_sold == 0:
            gain_sold_pr = 0

        if count_free != 0:
            gain_free_pr = int(((count_free)/828)*100)
        elif count_free == 0:
            gain_free_pr = 0

        lens = Seat.get_all_free_seats(self, self.kwargs['date'], self.kwargs['hour'], city_id)
        print(len(Seat.objects.all().filter(sector__sector_number=4, date__date=self.kwargs['date'], date__hour=self.kwargs['hour'], sector__city__id=city_id,)))
        context = Sector.get_all_sectors(self, self.kwargs['date'], self.kwargs['hour'], city_id)
        context['len_1'] = lens[0]
        context['len_2'] = lens[1]
        context['len_3'] = lens[2]
        context['len_4'] = lens[3]
        context['len_5'] = lens[4]
        sec = Sector.get_all_sectors(self, self.kwargs['date'], self.kwargs['hour'], city_id)
        context['date'] = self.kwargs['date']
        context['hour'] = self.kwargs['hour']
        context['city_id'] = city_id
        context['time'] = context['all_sectors'][0].date

        context['city_id'] = city_id
        context['gain_total'] = gain_total
        context['stat'] = stat
        context['gain_sold_pr'] = gain_sold_pr
        context['count_sold'] = count_sold
        context['count_free'] = count_free
        context['count_share'] = count_share
        context['gain_free_pr'] = gain_free_pr
        context['count_vacant'] = count_vacant
        return render(request, self.template_name, context)

    def post(self, request, *arg, city_id, **kwargs):
        next = request.POST.get('next')
        if 'Delete' in request.POST:
            if User.objects.get(id=request.user.id).staff   == True:
                Day.objects.all().filter(date__date=self.kwargs['date'], date__hour=self.kwargs['hour'], city__id=city_id).delete()
                Sector.objects.all().filter(date__date=self.kwargs['date'], date__hour=self.kwargs['hour'], city__id=city_id).delete()
                return HttpResponseRedirect(next)
            else:
                return HttpResponse('<h1>У вас нет прав удалять дни.</h1>')


class Stats(LoginRequiredMixin, View):
    template_name = 'desk/stats.html'
    def post(self, request, city_id, *arg, **kwargs):
        seat_vacant = Seat.objects.all().filter(date__date=self.kwargs['date'], date__hour=self.kwargs['hour'], sold='Vacant', sector__city__id=city_id)
        seat_sold = Seat.objects.all().filter(date__date=self.kwargs['date'], date__hour=self.kwargs['hour'], sold='Sold', sector__city__id=city_id)
        seat_share = Seat.objects.all().filter(date__date=self.kwargs['date'], date__hour=self.kwargs['hour'], sold='Share', sector__city__id=city_id)
        #seat_discount = Seat.objects.all().filter(date__date=date, date__hour=hour, sold='Discount')
        seat_free = Seat.objects.all().filter(date__date=self.kwargs['date'], date__hour=self.kwargs['hour'], sold='Free', sector__city__id=city_id)
        gain_total = 0
        gain_sold = 0
        gain_share = 0
        gain_discount = 0
        for seat in seat_sold:
            gain_sold = gain_sold + seat.price
        #for seat in seat_discount:
            #gain_discount = gain_discount + seat.price*0.8
        for seat in seat_share:
            gain_share = gain_share + 1
        gain_total = gain_sold

        count_sold = len(seat_sold)
        #count_discount = len(seat_discount)
        count_free = len(seat_free)
        count_vacant = len(seat_vacant)
        if len(seat_vacant) != 0 :
            stat = int(((828 - len(seat_vacant))/828)*100)
        elif len(seat_vacant) == 0:
            stat = 100

        if count_sold !=0:
            gain_sold_pr = int(((count_sold)/828)*100)

        elif count_sold == 0:
            gain_sold_pr = 0

        if count_free != 0:
            gain_free_pr = int(((count_free)/828)*100)
        elif count_free == 0:
            gain_free_pr = 0


        context = {
        'gain_sold':gain_sold,
        'gain_total':gain_total,
        'gain_discount':gain_discount,
        'count_sold': count_sold,
        'count_free':count_free,
        'count_vacant':count_vacant,
        'gaint_share':gain_share,
        'stat':stat,
        'gain_sold_pr': gain_sold_pr,
        'gain_free_pr': gain_free_pr}
        return render(request, self.template_name, context)

class CityStats(LoginRequiredMixin, View):
    template_name = "desk/city_stats.html"

    def post(self, request, city_id,  *args, **kwargs):
        next = request.POST.get('next')
        seat_given = Seat.objects.all().filter(sold='Local_cashdesks', sector__city__id=city_id)
        seat_vacant = Seat.objects.all().filter(sold='Vacant', sector__city__id=city_id)
        seat_sold = Seat.objects.all().filter(sold='Sold', sector__city__id=city_id)
        seat_share = Seat.objects.all().filter(sold='Share', sector__city__id=city_id)
        #seat_discount = Seat.objects.all().filter(date__date=date, date__hour=hour, sold='Discount')
        seat_free = Seat.objects.all().filter(sold='Free', sector__city__id=city_id)
        city = City.objects.get(id=city_id)
        gain_total = 0
        gain_sold = 0
        gain_share = 0
        gain_discount = 0
        for seat in seat_sold:
            gain_sold = gain_sold + seat.price
        #for seat in seat_discount:
            #gain_discount = gain_discount + seat.price*0.8
        for seat in seat_share:
            gain_share = gain_share + 1
        for seat in seat_given:
        	gain_sold = gain_sold + seat.price
        gain_total = gain_sold


        count_sold = len(seat_sold)
        #count_discount = len(seat_discount)
        count_free = len(seat_free)
        count_vacant = len(seat_vacant)
        if len(seat_vacant) != 0 :
            stat = int(((828 - len(seat_vacant))/828)*100)
        elif len(seat_vacant) == 0:
            stat = 100

        if count_sold !=0:
            gain_sold_pr = int(((count_sold)/828)*100)

        elif count_sold == 0:
            gain_sold_pr = 0

        if count_free != 0:
            gain_free_pr = int(((count_free)/828)*100)
        elif count_free == 0:
            gain_free_pr = 0

        if 'export' in request.POST:
            output = io.BytesIO()
            next = request.POST.get('next')
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet1 = workbook.add_worksheet()

            cell_format = workbook.add_format()
            cell_format2 = workbook.add_format()

            chart = workbook.add_chart({'type': 'pie'})

            cell_format.set_font_size(16)
            cell_format.set_center_across()
            cell_format.set_border()
            cell_format.set_bg_color('#b4b4b4')

            cell_format2.set_font_size(16)
            cell_format2.set_center_across()
            cell_format2.set_border()
            cell_format2.set_bg_color('#b4b4b4')

            worksheet1.set_column(0,1,30)
            worksheet1.set_column(1,1,20)

            worksheet1.write(ascii_uppercase[0]+"1","Общая прибыль", cell_format2)
            worksheet1.write(ascii_uppercase[1]+"1",gain_total, cell_format)

            worksheet1.write(ascii_uppercase[0]+"2","Продано билетов", cell_format2)
            worksheet1.write(ascii_uppercase[1]+"2",count_sold, cell_format)


            worksheet1.write(ascii_uppercase[0]+"3","Продано по акции", cell_format2)
            worksheet1.write(ascii_uppercase[1]+"3",gain_share, cell_format)

            worksheet1.write(ascii_uppercase[0]+"4","По пригласительным", cell_format2)
            worksheet1.write(ascii_uppercase[1]+"4",count_free, cell_format)

            worksheet1.write(ascii_uppercase[0]+"5","Не продано", cell_format2)
            worksheet1.write(ascii_uppercase[1]+"5",count_vacant, cell_format)

            chart.add_series({
                'name': str(city),
                'categories': '=Sheet1!$A$2:$A$5',
                'values':     '=Sheet1!$B$2:$B$5',
                'points': [
                    {'fill': {'color': 'green'}},
                    {'fill': {'color': 'red'}},
                ],
            })

            worksheet1.insert_chart('D1', chart)

            workbook.close()

            output.seek(0)

            response = HttpResponse(output.read(),content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=" + str(city) + ".xlsx"

            output.close()

            return response



    def get(self, request, city_id,  *args, **kwargs):
        seat_vacant = Seat.objects.all().filter(sold='Vacant', sector__city__id=city_id)
        seat_sold = Seat.objects.all().filter(sold='Sold', sector__city__id=city_id)
        seat_share = Seat.objects.all().filter(sold='Share', sector__city__id=city_id)
        #seat_discount = Seat.objects.all().filter(date__date=date, date__hour=hour, sold='Discount')
        seat_free = Seat.objects.all().filter(sold='Free', sector__city__id=city_id)
        city = City.objects.get(id=city_id)
        gain_total = 0
        gain_sold = 0
        gain_share = 0
        gain_discount = 0
        for seat in seat_sold:
            gain_sold = gain_sold + seat.price
        #for seat in seat_discount:
            #gain_discount = gain_discount + seat.price*0.8
        for seat in seat_share:
            gain_share = gain_share + 1
        gain_total = gain_sold

        count_sold = len(seat_sold)
        #count_discount = len(seat_discount)
        count_free = len(seat_free)
        count_vacant = len(seat_vacant)

        context = {
        'city':city,
        'gain_sold':gain_sold,
        'gain_total':gain_total,
        'gain_discount':gain_discount,
        'count_sold': count_sold,
        'count_free':count_free,
        'count_vacant':count_vacant,
        'gaint_share':gain_share}


        return render(request, self.template_name, context)

class Box(LoginRequiredMixin, View):
    def get(self, request, city_id, *arg, **kwargs):
        current_user = User.objects.get(id=request.user.id)
        if self.kwargs['name'] != 'Noname':
            seats = Seat.objects.filter(sold = 'Booked', name = str(self.kwargs['name']), sector__city=self.kwargs['city_id'], date__hour=self.kwargs['hour'], date__date=self.kwargs['date'], sector__sector_number=int(self.kwargs['sector_number']))
            print(self.kwargs['name'])
            for seat in seats:
                seat.selected = True
                seat.user_id = current_user.id
                current_user.batch = current_user.batch + seat.price
                seat.save()
                current_user.save()
        sector = Sector.get_sector(self, self.kwargs['date'], self.kwargs['hour'], self.kwargs['sector_number'], city_id )
        city = City.objects.get(id=city_id)
        date = self.kwargs['date']
        hour = self.kwargs['hour']
        rows = sector.get_all_rows()
        all_rows = []
        
        if current_user.staff == True:
        	template_name = 'desk/box_admin.html'
        else: 
        	template_name = 'desk/box.html'



        batch = current_user.batch
        date_ = datetime.datetime.now().replace(second=0, microsecond=0, tzinfo=pytz.timezone('UTC'))

        c = sector.date.replace(second=0, microsecond=0) - date_
        print(c.total_seconds)
        if c.total_seconds() < 3600:
        	needed = Seat.objects.all().filter(date__date=self.kwargs['date'], date__hour=self.kwargs['hour'], sold='Booked', sector__city__id=city_id)
        	for seat in needed:
        		seat.sold = 'Vacant'
        		seat.name = ' '
        		seat.save()

        if self.kwargs['sector_number'] != '5':
            for i in range(0,9):
                all_rows.append(rows[i].seat_set.all()[::1])
        elif self.kwargs['sector_number'] == '5':
            for i in range(0,6):
                all_rows.append(rows[i].seat_set.all()[::1])
        if self.kwargs['sector_number'] == '3' or self.kwargs['sector_number'] =='4':
            for row in all_rows:
                row.sort(key=lambda x: x.seat_number, reverse=False)
        elif self.kwargs['sector_number'] == '1' or self.kwargs['sector_number'] == '2' or self.kwargs['sector_number'] == '5':
            for row in all_rows:
                row.sort(key=lambda x: x.seat_number, reverse=True)




        all_rows =  sorted(all_rows,key = len)
        context = {'all_rows':all_rows,
                   'batch':batch,
                   'sector':self.kwargs['sector_number'],
                   'city':city,
                   'date':date,
                   'hour':hour,
                   'date_full':sector.date
                  }
        return render(request, template_name, context)


    def post(self, request, *arg, city_id, **kwargs):
        next = request.POST.get('next')
        print(request.POST.get('next'))
        current_user = User.objects.get(id=request.user.id)
        all_seats = Seat.get_all_selected_seats(self, current_user.id, city_id=city_id, hour=self.kwargs['hour'], date=self.kwargs['date'])

        if 'Change_Price' in request.POST:
            if current_user.staff == True:
                for seat in all_seats:
                    if  seat.sold == 'Vacant':
                            seat.user_id = 0
                            current_user.batch = 0
                            current_user.save()
                            print(request.POST.get('booked_name'))
                            seat.price =  request.POST.get('change_price')
                            seat.selected = False
                            seat.save()
                    else:
    	                seat.selected = False
    	                seat.save()
                return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect(next)


        if 'Book' in request.POST:
            for seat in all_seats:
                if  seat.sold == 'Vacant':
                        seat.user_id = 0
                        current_user.batch = 0
                        current_user.save()
                        print(request.POST.get('booked_name'))
                        seat.name =  request.POST.get('booked_name')
                        seat.sold = 'Booked'
                        seat.selected = False
                        seat.save()
                else:
	                seat.selected = False
	                seat.save()
            return HttpResponseRedirect(next)

        if 'Back' in request.POST:
            current_user.batch = 0
            current_user.save()
            #all_seats = Seat.get_all_selected_seats(self, sector__city__id=city_id, hour=self.kwargs['hour'], date=self.kwargs['date'], current_user.id)
            for seat in all_seats:
                seat.selected = False
                seat.save()
            return HttpResponseRedirect(next)

        if 'Select' in request.POST:
            next = request.POST.get('next', '/')
            selected_seat = Seat.objects.get(id=request.POST.get("Select", ""))
            if selected_seat.selected == False and selected_seat.sold == 'Vacant':
                selected_seat.user_id = request.user.id
                selected_seat.selected = True
                current_user.batch = current_user.batch + selected_seat.price
            elif selected_seat.selected == False and selected_seat.sold == 'Booked':
                selected_seat.user_id = request.user.id
                selected_seat.selected = True
                current_user.batch = current_user.batch + selected_seat.price
            elif selected_seat.selected == False and selected_seat.sold != 'Vacant':
                 selected_seat.user_id = request.user.id
                 selected_seat.selected = True
            elif selected_seat.selected == True and selected_seat.user_id == request.user.id and selected_seat.sold == 'Vacant':
                selected_seat.selected = False
                selected_seat.user_id = 0
                current_user.batch = current_user.batch - selected_seat.price
            elif selected_seat.selected == True and selected_seat.user_id == request.user.id and selected_seat.sold == 'Booked':
                selected_seat.selected = False
                selected_seat.user_id = 0
                current_user.batch = current_user.batch - selected_seat.price
            elif selected_seat.selected == True and selected_seat.user_id == request.user.id and selected_seat.sold != 'Vacant':
                selected_seat.selected = False
                selected_seat.user_id = 0
            selected_seat.save()
            current_user.save()
            return HttpResponseRedirect(next)

        if 'Sell' in request.POST:
            next = request.POST.get('next', '/')
            #all_seats = Seat.get_all_selected_seats(self, sector__city__id=city_id, hour=self.kwargs['hour'], date=self.kwargs['date'], current_user.id)
            for seat in all_seats:
                if  seat.sold == 'Vacant' or seat.sold == 'Booked':
                        seat.user_id = 0
                        seat.sold = 'Sold'
                        seat.selected = False
                        seat.save()
                        seat.name = ''
                        if seat.price == 500:
                            current_user.sold_500 += 1

                        if seat.price == 700:
                            current_user.sold_700 += 1

                        elif seat.price == 800:
                            current_user.sold_800 += 1

                        elif seat.price == 900:
                            current_user.sold_900 += 1

                        elif seat.price == 1000:
                            current_user.sold_1000 += 1

                        elif seat.price == 1200:
                            current_user.sold_1200 += 1

                        elif seat.price == 1500:
                            current_user.sold_1500 += 1


                        current_user.sold_normal = current_user.sold_normal + 1
                        seat.save()
                        current_user.save()
                elif  seat.sold != 'Vacant':
                        seat.selected = False
                        seat.save()


            current_user.gain = current_user.gain + current_user.batch
            current_user.batch = 0
            current_user.save()
            return HttpResponseRedirect(next)

        if 'Free' in request.POST:
                    next = request.POST.get('next', '/')
                    #all_seats = Seat.get_all_selected_seats(self, sector__city__id=city_id, hour=self.kwargs['hour'], date=self.kwargs['date'], current_user.id)
                    for seat in all_seats:
                        if  seat.sold != 'Free' and seat.sold != 'Local_cashdesks'and seat.sold != 'Discount' and seat.sold != 'Share':
                            current_user.sold_vacant = current_user.sold_vacant + 1
                            seat.user_id = 0
                            current_user.gain = current_user.gain - seat.price
                            current_user.sold_normal = current_user.sold_normal - 1
                            current_user.save()
                            seat.sold = 'Vacant'
                            seat.selected = False
                            seat.name = ' '
                            seat.save()
                        elif seat.sold == 'Booked':
                        	seat.sold == 'Vacant'
                        	seat.name = ' '
                        	seat.save()
                        elif  seat.sold != 'Free' and seat.sold != 'Local_cashdesks'  and seat.sold == 'Discount':
                            current_user.sold_vacant = current_user.sold_vacant + 1
                            seat.user_id = 0
                            current_user.gain = current_user.gain - (seat.price)*0.8
                            current_user.sold_discount = current_user.sold_discount - 1
                            current_user.save()
                            seat.sold = 'Vacant'
                            seat.selected = False
                            seat.name = ' '
                            seat.save()
                        elif  seat.sold != 'Free'and seat.sold != 'Local_cashdesks' and seat.sold == 'Share':
                            current_user.sold_vacant = current_user.sold_vacant + 1
                            seat.user_id = 0
                            current_user.sold_share = current_user.sold_share - 1
                            current_user.save()
                            seat.sold = 'Vacant'
                            seat.selected = False
                            seat.name = ' '
                            seat.save()
                        if seat.price == 500 :
                            current_user.sold_500 -= 1

                        elif seat.price == 700:
                            current_user.sold_700 -= 1

                        elif seat.price == 800:
                            current_user.sold_800 -= 1

                        elif seat.price == 900:
                            current_user.sold_900 -= 1

                        elif seat.price == 1000:
                            current_user.sold_1000 -= 1

                        elif seat.price == 1200:
                            current_user.sold_1200 -= 1

                        elif seat.price == 1500:
                            current_user.sold_1500 -= 1

                    current_user.batch = 0
                    current_user.save()
                    return HttpResponseRedirect(next)

        if 'Share' in request.POST:
                next = request.POST.get('next', '/')
                #all_seats = Seat.get_all_selected_seats(self, self.kwargs['sector_number'], current_user.id)
                if len(all_seats) == 4 and all_seats[0].price == all_seats[1].price == all_seats[2].price == all_seats[3].price:
                    all_seats = all_seats.order_by('price')
                    min_seat = all_seats[0]
                    seat_1 = all_seats[1]
                    seat_2 = all_seats[2]
                    seat_3 = all_seats[3]
                    min_seat.sold = 'Share'
                    current_user.sold_share  = current_user.sold_share + 1
                    if min_seat.price == 500:
                        current_user.sold_500 += 1
                    elif min_seat.price == 700:
                        current_user.sold_700 += 1

                    elif min_seat.price == 800:
                        current_user.sold_800 += 1

                    elif min_seat.price == 900:
                        current_user.sold_900 += 1

                    elif min_seat.price == 1000:
                        current_user.sold_1000 += 1

                    elif min_seat.price == 1200:
                        current_user.sold_1200 += 1

                    elif min_seat.price == 1500:
                        current_user.batch = current_user.batch - min_seat.price
                    current_user.save()
                    min_seat.selected = False
                    min_seat.user_id = 0
                    min_seat.save()
                    seat_1.sold = 'Sold'
                    seat_1.user_id = 0
                    seat_1.selected = False
                    current_user.sold_normal  = current_user.sold_normal + 1
                    if seat_1.price == 500:
                        current_user.sold_500 += 1
                    elif seat_1.price == 700:
                        current_user.sold_700 += 1

                    elif seat_1.price == 800:
                        current_user.sold_800 += 1

                    elif seat_1.price == 900:
                        current_user.sold_900 += 1

                    elif seat_1.price == 1000:
                        current_user.sold_1000 += 1

                    elif seat_1.price == 1200:
                        current_user.sold_1200 += 1

                    elif seat_1.price == 1500:
                        current_user.sold_1500 += 1
                    current_user.save()
                    seat_1.save()
                    seat_2.sold = 'Sold'
                    seat_2.user_id = 0
                    seat_2.selected = False
                    current_user.sold_normal  = current_user.sold_normal + 1
                    if seat_2.price == 500:
                        current_user.sold_500 += 1
                    elif seat_2.price == 700:
                        current_user.sold_700 += 1

                    elif seat_2.price == 800:
                        current_user.sold_800 += 1

                    elif seat_2.price == 900:
                        current_user.sold_900 += 1

                    elif seat_2.price == 1000:
                        current_user.sold_1000 += 1

                    elif seat_2.price == 1200:
                        current_user.sold_1200 += 1

                    elif seat_2.price == 1500:
                        current_user.sold_1500 += 1
                    current_user.save()
                    seat_2.save()
                    seat_3.sold = 'Sold'
                    seat_3.user_id = 0
                    seat_3.selected = False
                    current_user.sold_normal  = current_user.sold_normal + 1
                    if seat_3.price == 500:
                        current_user.sold_500 += 1
                    elif seat_3.price == 700:
                        current_user.sold_700 += 1

                    elif seat_3.price == 800:
                        current_user.sold_800 += 1

                    elif seat_3.price == 900:
                        current_user.sold_900 += 1

                    elif seat_3.price == 1000:
                        current_user.sold_1000 += 1

                    elif seat_3.price == 1200:
                        current_user.sold_1200 += 1

                    elif seat_3.price == 1500:
                        current_user.sold_1500 += 1

                    current_user.save()
                    seat_3.save()
                    current_user.gain = current_user.gain + current_user.batch
                    current_user.batch = 0
                    current_user.save()
                    return HttpResponseRedirect(next)
                else:
                    return HttpResponseRedirect(next)

        if 'Sell_Free' in request.POST:
                next = request.POST.get('next', '/')
                if current_user.staff == True:
                    #all_seats = Seat.get_all_selected_seats(self, self.kwargs['sector_number'], current_user.id)
                    for seat in all_seats:
                        if  seat.sold == 'Vacant':
                                seat.user_id = 0
                                seat.sold = 'Free'
                                seat.selected = False
                                seat.save()
                        elif  seat.sold == 'Free':
                                seat.user_id = 0
                                seat.sold = 'Vacant'
                                seat.selected = False
                                seat.save()
                    current_user.batch = 0
                    current_user.save()
                    return HttpResponseRedirect(next)
                else:
                    return HttpResponseRedirect(next)
        if 'Local_cashdesks' in request.POST:
                next = request.POST.get('next', '/')
                if current_user.staff == True:
                    #all_seats = Seat.get_all_selected_seats(self, self.kwargs['sector_number'], current_user.id)
                    for seat in all_seats:
                        if  seat.sold == 'Vacant':
                                seat.user_id = 0
                                seat.sold = 'Local_cashdesks'
                                seat.selected = False
                                seat.save()
                        elif  seat.sold == 'Local_cashdesks':
                                seat.user_id = 0
                                seat.sold = 'Vacant'
                                seat.selected = False
                                seat.save()
                    current_user.batch = 0
                    current_user.save()
                    return HttpResponseRedirect(next)
                else:
                    return HttpResponseRedirect(next)


class BookedList(LoginRequiredMixin, View):
    template_name = "desk/booked_list.html"

    def get(self, request, city_id, date, hour, *arg, **kwargs):
        seats = Seat.objects.filter(date__date=date, date__hour=hour, sold='Booked', sector__city__id=city_id)
        context = {}
        for seat in seats:
            context[seat.name] = seat
        seats = list(context.values())
        print(seats)
        try:
            context['time'] = seats[0].date
        except IndexError:
            pass
        context['seats'] = seats
        return render(request, self.template_name, context)