from django import template
from django.utils.safestring import mark_safe

register = template.Library()    #register 名字是固定的,写法就这样

@register.filter
def yl(t):
	#园龄
    import datetime
    user_current_time = datetime.datetime(year=t.year,month=t.month,day=t.day,hour=t.hour,minute=t.minute,second=t.second)
    ret = datetime.datetime.now()-user_current_time
    ret = str(ret).split(',')[0]
    print(ret)
    print(type(ret))

    # return mark_safe(ret)
    return mark_safe(ret)