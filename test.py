module = 'desk/cache.city_{}'.format(str(2))
def my_import(name):
                components = name.split('.')
                mod = __import__(components[0])
                for comp in components[1:]:
                    mod = getattr(mod, comp)
                return mod

a = my_import(module)
print(a)