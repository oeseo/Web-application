from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from .utils import Valid_form, get_db_handle, find_forms


class HomePageView(View):
    def get(self, request):
        db = get_db_handle()
        context = ''.join([f'{x}<br/>' for x in
                           db['forms'].find({}, {'_id': 0})])
        return HttpResponse(context)


class GetFormView(View):
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        context = {'result': ''}
        requests_post = request.POST.copy()
        requests_post.pop('csrfmiddlewaretoken', None)
        db = get_db_handle()

        if requests_post:
            for key in requests_post.keys():
                requests_post[key] = Valid_form(requests_post[key]).type_form
            result_find = find_forms(db['forms'], requests_post)
            result = [form['name'] for form in result_find]
            if result:
                context['result'] = ('Имена подходящих форм:\n ' +
                                     '\n '.join(result))
            else:
                formatted_request = ',\n      '.join(
                    [f'{x}: {y}' for x, y in requests_post.items()])
                context['result'] = (
                    "Форма не найдена, по запросу "
                    "должна быть такая форма \n{\n      " +
                    formatted_request + '\n}')
        else:
            context['result'] = ('Для поиска форм необходимо передать '
                                 'не пустой запрос')
        return HttpResponse(context['result'])
