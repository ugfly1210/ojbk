def filter_tag(html_str):
    # valid_tag_list = ["p", "div", "a", "img", "html", "body", "br", "strong", "b"]
    valid_attr_dic = {'p' : ['class','id'],
                      'div' : ['class','id'],
                      'img' : ['src']}

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_str,'html.parser')  #将soup --> document

    for tag in soup.find_all():
        if tag.name not in valid_attr_dic:    #如果不在我们的合法标签范围内,干掉它
            tag.decompose()
        else:
            if tag.attrs :   #如果它有属性的话,才执行下一步,看它的属性在不在,  过滤非法属性
                for k in list(tag.attrs.keys()):   #如题,遍历出来属性名,如果不在白名单也过滤
                    if k not in valid_attr_dic[tag.name]:
                        del tag.attrs[k]
    content_str = soup.decode()
    return content_str