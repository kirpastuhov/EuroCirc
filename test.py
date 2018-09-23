def my_import(name):
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
        print(mod)
    return mod



a = 'cache.city_1'

my_import(a)