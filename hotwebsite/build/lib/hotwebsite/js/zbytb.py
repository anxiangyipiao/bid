# encoding: utf-8  
import execjs
import requests
import requests_html
import execjs

SESSION = requests_html.HTMLSession()

HEADERS = {
     'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
}   

 
class zbytb_js:
    def __init__(self):

        pass

    def first_cookie_decode(self,base_url):

        try:
            response = SESSION.get(base_url, headers=HEADERS, timeout=(8, 8))

            if response.status_code == 521:
                cookies = response.cookies
                str_js_cookie = response.text.replace("<script>document.", "").replace(
                    ";location.href=location.pathname+location.search</script>", "")
                js_result = execjs.eval(str_js_cookie).split(";")[0]
                cookies_text = ';'.join(['='.join(item) for item in cookies.items()])
                HEADERS['cookie'] = cookies_text + "; " + js_result
                return HEADERS, cookies_text
            
            elif response.status_code == 200:
                return HEADERS, None  # 明确返回None
        except Exception as e:
            return HEADERS, None  # 在发生异常时返回None


    def second_cookie_decode(self,base_url):

        """
        破解第二次加密
        :param HEADERS: 浏览器请求头，首次破解加密字段一
        :return: 浏览器请求头，第二次破解加密字段二
        """
        HEADERS,cookie_first_decode =  self.first_cookie_decode(base_url)
        
        if cookie_first_decode is None:
            return None,None
        
        response = SESSION.get(base_url, headers=HEADERS, timeout=(8, 8))

        if response.status_code == 521:

            # 获取全部js
            response.encoding = 'utf-8' # 防止中文乱码
            str_base = response.text.replace("</script>","").replace("<script>","")
            head_str= 'const jsdom = require("jsdom");const { JSDOM } = jsdom;const dom = new JSDOM(`<!DOCTYPE html><p>Hello world</p>`);window = dom.window;document = window.document;XMLHttpRequest = window.XMLHttpRequest;'
            str_cookie_index1 = 'var cookie = '
            index1 = str_base.find('go({')
            str_base = head_str + str_base[:index1] + str_cookie_index1 + str_base[index1:]+";function getCookie() {return cookie;};"
        
            index2 = str_base.find('setTimeout')
            if str_base[index2 - 1] == "(":
                str_base =  str_base.replace("(setTimeout,function(){",";")
            elif str_base[index2 - 1] == "}":
                str_base =  str_base.replace("setTimeout(function(){","")

            # 获取加密字段内容
            str_ie_cookie = str_base.replace(" ", "")[
                            str_base.replace(" ", "").find("'ie']=") + 6:str_base.replace(" ", "").find("location[")]
    
            str_cookie_index2 = '''var cookies={};return cookies;'''.format(str_ie_cookie)

            # 在str_base中document前插入str_cookie_temp
            index3 = str_base.find('document[')
            index4 = index3
            count = 0
            # 寻找document后第3个;
            for i in str_base[index3:]:
                if i ==";":
                    count = count + 1       
                if count == 3:
                    break     
                index4 = index4 + 1 

            str_base = str_base[:index3]+str_cookie_index2+str_base[index4+1:]

            
            return str_base,cookie_first_decode


    def execjs_cookie_decode(self,js):

        ct = execjs.compile(js,cwd=r'C:\Users\zax\AppData\Roaming\npm\node_modules')

        js_cookie = ct.call("getCookie")

        second_cookie = js_cookie.split(";")[0]

        return second_cookie


    def get_cookie(self,url):

        str_js,cookie_first_decode = self.second_cookie_decode(url)
        if cookie_first_decode is None:
            return None

        cookie_second_decode = self.execjs_cookie_decode(str_js)

        a = cookie_first_decode.split("=")
        b = cookie_second_decode.split("=")

        cookie = {
            a[0]: a[1],
            b[0]: b[1]
        }

        return cookie






# if __name__ == '__main__':


#     url = 'https://www.zbytb.com/search/?kw=&okw=&catid=0&zizhi=&zdxm=&zdyear=&field=0&moduleid=25&areaids=&page=1'

#     zb = zbytb_js()

#     cookie = zb.get_cookie(url)

#     # cookie dict转换为requests可用的格式
#     cookie = requests.utils.cookiejar_from_dict(cookie)

#     header = {
#         'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
#         # "cookie":'__jsluid_s=134c562d15598a35d132232e65640b32;__jsl_clearance_s=1722474306.754|0|dkHQ78qxVrB%2FB%2BOnU5pUUzyjHS0%3D',
#     }

#     res =requests.get(url, headers=header, timeout=(8, 8),cookies=cookie)


#     print(res.text)



  



