for each_row in Row.objects.filter(date=creation_date, sector__city_id=city_id, sector__sector_number=5):
                if each_row.row_number == 1:
                    try:
                        if int(Cache.objects.get(city_id=city_id, name='s_5_row_1_1').instance.split(',')[
                                   0]) > 0 and int(
                                Cache.objects.get(city_id=city_id, name='s_5_row_1_1').instance.split(',')[1]) > 0:
                            for s in range(1, int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_1_1').instance.split(',')[0]) + 1):
                                Seat(seat_number=s, price=int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_1_1').instance.split(',')[1]),
                                     sector=each_row.sector, row=each_row, date=creation_date).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if Cache.objects.get(city_id=city_id, name='s_5_row_1_2').instance.split(',')[0] != '':
                            if int(Cache.objects.get(city_id=city_id, name='s_5_row_1_2').instance.split(',')[0]) > int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_1_1').instance.split(',')[
                                        0]) and int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_1_2').instance.split(',')[1]) > 0:
                                for k in range(int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_1_1').instance.split(',')[
                                            0]) + 1, int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_1_2').instance.split(',')[
                                            0]) + 1):
                                    Seat(seat_number=k, price=int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_1_2').instance.split(',')[1]),
                                         sector=each_row.sector, row=each_row, date=creation_date).save()
                        if Cache.objects.get(city_id=city_id, name='s_5_row_1_2').instance.split(',')[0] != '' and \
                                Cache.objects.get(city_id=city_id, name='s_5_row_1_3').instance.split(',')[0] != '':
                            if int(Cache.objects.get(city_id=city_id, name='s_5_row_1_3').instance.split(',')[0]) > int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_1_2').instance.split(',')[
                                        0]) and int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_1_3').instance.split(',')[1]) > 0:
                                for k in range(int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_1_2').instance.split(',')[
                                            0]) + 1, int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_1_3').instance.split(',')[
                                            0].strip()) + 1):
                                    Seat(seat_number=k, price=int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_1_2').instance.split(',')[1]),
                                         sector=each_row.sector, row=each_row, date=creation_date).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест ПЕРВЫЙ!</h1>')

                if each_row.row_number == 2:
                    try:
                        if int(Cache.objects.get(city_id=city_id, name='s_5_row_2_1').instance.split(',')[
                                   0]) > 0 and int(
                                Cache.objects.get(city_id=city_id, name='s_5_row_2_1').instance.split(',')[1]) > 0:
                            for s in range(1, int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_2_1').instance.split(',')[0]) + 1):
                                Seat(seat_number=s, price=int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_2_1').instance.split(',')[1]),
                                     sector=each_row.sector, row=each_row, date=creation_date).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if Cache.objects.get(city_id=city_id, name='s_5_row_2_2').instance.split(',')[0] != '':
                            if int(Cache.objects.get(city_id=city_id, name='s_5_row_2_2').instance.split(',')[0]) > int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_2_1').instance.split(',')[
                                        0]) and int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_2_2').instance.split(',')[1]) > 0:
                                for k in range(int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_2_1').instance.split(',')[
                                            0]) + 1, int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_2_2').instance.split(',')[
                                            0]) + 1):
                                    Seat(seat_number=k, price=int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_2_2').instance.split(',')[1]),
                                         sector=each_row.sector, row=each_row, date=creation_date).save()
                        if Cache.objects.get(city_id=city_id, name='s_5_row_2_2').instance.split(',')[0] != '' and \
                                Cache.objects.get(city_id=city_id, name='s_5_row_2_3').instance.split(',')[0] != '':
                            if int(Cache.objects.get(city_id=city_id, name='s_5_row_2_3').instance.split(',')[0]) > int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_2_2').instance.split(',')[
                                        0]) and int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_2_3').instance.split(',')[1]) > 0:
                                for k in range(int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_2_2').instance.split(',')[
                                            0]) + 1, int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_2_3').instance.split(',')[
                                            0].strip()) + 1):
                                    Seat(seat_number=k, price=int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_2_2').instance.split(',')[1]),
                                         sector=each_row.sector, row=each_row, date=creation_date).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест ПЕРВЫЙ!</h1>')

                if each_row.row_number == 3:
                    try:
                        if int(Cache.objects.get(city_id=city_id, name='s_5_row_3_1').instance.split(',')[
                                   0]) > 0 and int(
                                Cache.objects.get(city_id=city_id, name='s_5_row_3_1').instance.split(',')[1]) > 0:
                            for s in range(1, int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_3_1').instance.split(',')[0]) + 1):
                                Seat(seat_number=s, price=int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_3_1').instance.split(',')[1]),
                                     sector=each_row.sector, row=each_row, date=creation_date).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if Cache.objects.get(city_id=city_id, name='s_5_row_3_2').instance.split(',')[0] != '':
                            if int(Cache.objects.get(city_id=city_id, name='s_5_row_3_2').instance.split(',')[0]) > int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_3_1').instance.split(',')[
                                        0]) and int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_3_2').instance.split(',')[1]) > 0:
                                for k in range(int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_3_1').instance.split(',')[
                                            0]) + 1, int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_3_2').instance.split(',')[
                                            0]) + 1):
                                    Seat(seat_number=k, price=int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_3_2').instance.split(',')[1]),
                                         sector=each_row.sector, row=each_row, date=creation_date).save()
                        if Cache.objects.get(city_id=city_id, name='s_5_row_3_2').instance.split(',')[0] != '' and \
                                Cache.objects.get(city_id=city_id, name='s_5_row_3_3').instance.split(',')[0] != '':
                            if int(Cache.objects.get(city_id=city_id, name='s_5_row_3_3').instance.split(',')[0]) > int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_3_2').instance.split(',')[
                                        0]) and int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_3_3').instance.split(',')[1]) > 0:
                                for k in range(int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_3_2').instance.split(',')[
                                            0]) + 1, int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_3_3').instance.split(',')[
                                            0].strip()) + 1):
                                    Seat(seat_number=k, price=int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_3_2').instance.split(',')[1]),
                                         sector=each_row.sector, row=each_row, date=creation_date).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест ПЕРВЫЙ!</h1>')

                if each_row.row_number == 4:
                    try:
                        if int(Cache.objects.get(city_id=city_id, name='s_5_row_4_1').instance.split(',')[
                                   0]) > 0 and int(
                                Cache.objects.get(city_id=city_id, name='s_5_row_4_1').instance.split(',')[1]) > 0:
                            for s in range(1, int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_4_1').instance.split(',')[0]) + 1):
                                Seat(seat_number=s, price=int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_4_1').instance.split(',')[1]),
                                     sector=each_row.sector, row=each_row, date=creation_date).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if Cache.objects.get(city_id=city_id, name='s_5_row_4_2').instance.split(',')[0] != '':
                            if int(Cache.objects.get(city_id=city_id, name='s_5_row_4_2').instance.split(',')[0]) > int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_4_1').instance.split(',')[
                                        0]) and int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_4_2').instance.split(',')[1]) > 0:
                                for k in range(int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_4_1').instance.split(',')[
                                            0]) + 1, int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_4_2').instance.split(',')[
                                            0]) + 1):
                                    Seat(seat_number=k, price=int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_4_2').instance.split(',')[1]),
                                         sector=each_row.sector, row=each_row, date=creation_date).save()
                        if Cache.objects.get(city_id=city_id, name='s_5_row_4_2').instance.split(',')[0] != '' and \
                                Cache.objects.get(city_id=city_id, name='s_5_row_4_3').instance.split(',')[0] != '':
                            if int(Cache.objects.get(city_id=city_id, name='s_5_row_4_3').instance.split(',')[0]) > int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_4_2').instance.split(',')[
                                        0]) and int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_4_3').instance.split(',')[1]) > 0:
                                for k in range(int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_4_2').instance.split(',')[
                                            0]) + 1, int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_4_3').instance.split(',')[
                                            0].strip()) + 1):
                                    Seat(seat_number=k, price=int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_4_2').instance.split(',')[1]),
                                         sector=each_row.sector, row=each_row, date=creation_date).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест ПЕРВЫЙ!</h1>')

                if each_row.row_number == 5:
                    try:
                        if int(Cache.objects.get(city_id=city_id, name='s_5_row_5_1').instance.split(',')[
                                   0]) > 0 and int(
                                Cache.objects.get(city_id=city_id, name='s_5_row_5_1').instance.split(',')[1]) > 0:
                            for s in range(1, int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_5_1').instance.split(',')[0]) + 1):
                                Seat(seat_number=s, price=int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_5_1').instance.split(',')[1]),
                                     sector=each_row.sector, row=each_row, date=creation_date).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if Cache.objects.get(city_id=city_id, name='s_5_row_5_2').instance.split(',')[0] != '':
                            if int(Cache.objects.get(city_id=city_id, name='s_5_row_5_2').instance.split(',')[0]) > int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_5_1').instance.split(',')[
                                        0]) and int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_5_2').instance.split(',')[1]) > 0:
                                for k in range(int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_5_1').instance.split(',')[
                                            0]) + 1, int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_5_2').instance.split(',')[
                                            0]) + 1):
                                    Seat(seat_number=k, price=int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_5_2').instance.split(',')[1]),
                                         sector=each_row.sector, row=each_row, date=creation_date).save()
                        if Cache.objects.get(city_id=city_id, name='s_5_row_5_2').instance.split(',')[0] != '' and \
                                Cache.objects.get(city_id=city_id, name='s_5_row_5_3').instance.split(',')[0] != '':
                            if int(Cache.objects.get(city_id=city_id, name='s_5_row_5_3').instance.split(',')[0]) > int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_5_2').instance.split(',')[
                                        0]) and int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_5_3').instance.split(',')[1]) > 0:
                                for k in range(int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_5_2').instance.split(',')[
                                            0]) + 1, int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_5_3').instance.split(',')[
                                            0].strip()) + 1):
                                    Seat(seat_number=k, price=int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_5_2').instance.split(',')[1]),
                                         sector=each_row.sector, row=each_row, date=creation_date).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест ПЕРВЫЙ!</h1>')

                if each_row.row_number == 6:
                    try:
                        if int(Cache.objects.get(city_id=city_id, name='s_5_row_6_1').instance.split(',')[
                                   0]) > 0 and int(
                                Cache.objects.get(city_id=city_id, name='s_5_row_6_1').instance.split(',')[1]) > 0:
                            for s in range(1, int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_6_1').instance.split(',')[0]) + 1):
                                Seat(seat_number=s, price=int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_6_1').instance.split(',')[1]),
                                     sector=each_row.sector, row=each_row, date=creation_date).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if Cache.objects.get(city_id=city_id, name='s_5_row_6_2').instance.split(',')[0] != '':
                            if int(Cache.objects.get(city_id=city_id, name='s_5_row_6_2').instance.split(',')[0]) > int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_6_1').instance.split(',')[
                                        0]) and int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_6_2').instance.split(',')[1]) > 0:
                                for k in range(int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_6_1').instance.split(',')[
                                            0]) + 1, int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_6_2').instance.split(',')[
                                            0]) + 1):
                                    Seat(seat_number=k, price=int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_6_2').instance.split(',')[1]),
                                         sector=each_row.sector, row=each_row, date=creation_date).save()
                        if Cache.objects.get(city_id=city_id, name='s_5_row_6_2').instance.split(',')[0] != '' and \
                                Cache.objects.get(city_id=city_id, name='s_5_row_6_3').instance.split(',')[0] != '':
                            if int(Cache.objects.get(city_id=city_id, name='s_5_row_6_3').instance.split(',')[0]) > int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_6_2').instance.split(',')[
                                        0]) and int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_6_3').instance.split(',')[1]) > 0:
                                for k in range(int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_6_2').instance.split(',')[
                                            0]) + 1, int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_6_3').instance.split(',')[
                                            0].strip()) + 1):
                                    Seat(seat_number=k, price=int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_6_2').instance.split(',')[1]),
                                         sector=each_row.sector, row=each_row, date=creation_date).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест ПЕРВЫЙ!</h1>')

                if each_row.row_number == 7:
                    try:
                        if int(Cache.objects.get(city_id=city_id, name='s_5_row_7_1').instance.split(',')[
                                   0]) > 0 and int(
                                Cache.objects.get(city_id=city_id, name='s_5_row_7_1').instance.split(',')[1]) > 0:
                            for s in range(1, int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_7_1').instance.split(',')[0]) + 1):
                                Seat(seat_number=s, price=int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_7_1').instance.split(',')[1]),
                                     sector=each_row.sector, row=each_row, date=creation_date).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if Cache.objects.get(city_id=city_id, name='s_5_row_7_2').instance.split(',')[0] != '':
                            if int(Cache.objects.get(city_id=city_id, name='s_5_row_7_2').instance.split(',')[0]) > int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_7_1').instance.split(',')[
                                        0]) and int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_7_2').instance.split(',')[1]) > 0:
                                for k in range(int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_7_1').instance.split(',')[
                                            0]) + 1, int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_7_2').instance.split(',')[
                                            0]) + 1):
                                    Seat(seat_number=k, price=int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_7_2').instance.split(',')[1]),
                                         sector=each_row.sector, row=each_row, date=creation_date).save()
                        if Cache.objects.get(city_id=city_id, name='s_5_row_7_2').instance.split(',')[0] != '' and \
                                Cache.objects.get(city_id=city_id, name='s_5_row_7_3').instance.split(',')[0] != '':
                            if int(Cache.objects.get(city_id=city_id, name='s_5_row_7_3').instance.split(',')[0]) > int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_7_2').instance.split(',')[
                                        0]) and int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_7_3').instance.split(',')[1]) > 0:
                                for k in range(int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_7_2').instance.split(',')[
                                            0]) + 1, int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_7_3').instance.split(',')[
                                            0].strip()) + 1):
                                    Seat(seat_number=k, price=int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_7_2').instance.split(',')[1]),
                                         sector=each_row.sector, row=each_row, date=creation_date).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест ПЕРВЫЙ!</h1>')

                if each_row.row_number == 8:
                    try:
                        if int(Cache.objects.get(city_id=city_id, name='s_5_row_8_1').instance.split(',')[
                                   0]) > 0 and int(
                                Cache.objects.get(city_id=city_id, name='s_5_row_8_1').instance.split(',')[1]) > 0:
                            for s in range(1, int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_8_1').instance.split(',')[0]) + 1):
                                Seat(seat_number=s, price=int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_8_1').instance.split(',')[1]),
                                     sector=each_row.sector, row=each_row, date=creation_date).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if Cache.objects.get(city_id=city_id, name='s_5_row_8_2').instance.split(',')[0] != '':
                            if int(Cache.objects.get(city_id=city_id, name='s_5_row_8_2').instance.split(',')[0]) > int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_8_1').instance.split(',')[
                                        0]) and int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_8_2').instance.split(',')[1]) > 0:
                                for k in range(int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_8_1').instance.split(',')[
                                            0]) + 1, int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_8_2').instance.split(',')[
                                            0]) + 1):
                                    Seat(seat_number=k, price=int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_8_2').instance.split(',')[1]),
                                         sector=each_row.sector, row=each_row, date=creation_date).save()
                        if Cache.objects.get(city_id=city_id, name='s_5_row_8_2').instance.split(',')[0] != '' and \
                                Cache.objects.get(city_id=city_id, name='s_5_row_8_3').instance.split(',')[0] != '':
                            if int(Cache.objects.get(city_id=city_id, name='s_5_row_8_3').instance.split(',')[0]) > int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_8_2').instance.split(',')[
                                        0]) and int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_8_3').instance.split(',')[1]) > 0:
                                for k in range(int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_8_2').instance.split(',')[
                                            0]) + 1, int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_8_3').instance.split(',')[
                                            0].strip()) + 1):
                                    Seat(seat_number=k, price=int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_8_2').instance.split(',')[1]),
                                         sector=each_row.sector, row=each_row, date=creation_date).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест ПЕРВЫЙ!</h1>')

                if each_row.row_number == 9:
                    try:
                        if int(Cache.objects.get(city_id=city_id, name='s_5_row_9_1').instance.split(',')[
                                   0]) > 0 and int(
                                Cache.objects.get(city_id=city_id, name='s_5_row_9_1').instance.split(',')[1]) > 0:
                            for s in range(1, int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_9_1').instance.split(',')[0]) + 1):
                                Seat(seat_number=s, price=int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_9_1').instance.split(',')[1]),
                                     sector=each_row.sector, row=each_row, date=creation_date).save()
                        else:
                            err_()
                            return HttpResponse('<h1>Ошибка в заполнении мест!</h1>')
                        if Cache.objects.get(city_id=city_id, name='s_5_row_9_2').instance.split(',')[0] != '':
                            if int(Cache.objects.get(city_id=city_id, name='s_5_row_9_2').instance.split(',')[0]) > int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_9_1').instance.split(',')[
                                        0]) and int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_9_2').instance.split(',')[1]) > 0:
                                for k in range(int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_9_1').instance.split(',')[
                                            0]) + 1, int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_9_2').instance.split(',')[
                                            0]) + 1):
                                    Seat(seat_number=k, price=int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_9_2').instance.split(',')[1]),
                                         sector=each_row.sector, row=each_row, date=creation_date).save()
                        if Cache.objects.get(city_id=city_id, name='s_5_row_9_2').instance.split(',')[0] != '' and \
                                Cache.objects.get(city_id=city_id, name='s_5_row_9_3').instance.split(',')[0] != '':
                            if int(Cache.objects.get(city_id=city_id, name='s_5_row_9_3').instance.split(',')[0]) > int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_9_2').instance.split(',')[
                                        0]) and int(
                                    Cache.objects.get(city_id=city_id, name='s_5_row_9_3').instance.split(',')[1]) > 0:
                                for k in range(int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_9_2').instance.split(',')[
                                            0]) + 1, int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_9_3').instance.split(',')[
                                            0].strip()) + 1):
                                    Seat(seat_number=k, price=int(
                                        Cache.objects.get(city_id=city_id, name='s_5_row_9_2').instance.split(',')[1]),
                                         sector=each_row.sector, row=each_row, date=creation_date).save()

                    except ValueError:
                        err_()
                        return HttpResponse('<h1>Ошибка в заполнении мест ПЕРВЫЙ!</h1>')