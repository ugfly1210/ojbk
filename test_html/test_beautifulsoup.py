content = """
<p id='i1' a='123' b='999'>
	<script>alert(123)</script>
</p>

<p id='i2'>
	<div>
		<p>asdfasdf</p>
	</div>
	<img id='i3' src="/static/imgs\6.jpg" alt="" />
</p>
"""

from bs4 import BeautifulSoup

soup = BeautifulSoup(content,'html.parser')

valid_tag = {
    'p' : ['class','id'],
    'img' : 'src',
    'div' : 'class'
}

#Tag.decompose() 方法将当前节点移除文档树并完全销毁:

#找到所有的标签名
tags = soup.find_all()

for tag in tags :
    # print('tag--------',tag)
    if tag.name in valid_tag:
        # print(tag.attrs)    取属性
        tag.decompose()
    if tag.attrs:   #是否有属性
        for k in list(tag.attrs.keys()):   #{id:'i1',a=123,b=999}
            if k not in valid_tag[tag.name]:
                del tag.attrs[k]

content_str = soup.decode()
print(content_str)



# v = soup.find(name='p',attrs={'id':'i2'})
# print(v)


# tag = soup.find(name='p')
# sc = tag.find('script')
# print(sc)

# tag = soup.find(name='p')
# sc = tag.find('script')
# print(sc)

