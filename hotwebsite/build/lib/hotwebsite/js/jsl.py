# encoding: utf-8  
import execjs
import requests_html
import re



class JSL():
    def __init__(self,headers,url):

        self.SESSION = requests_html.HTMLSession()
        self.headers = headers
        self.url = url
        self.first_cookie = None
        self.second_cookie = None

    def first_cookie_decode(self):

        try:
            response = self.SESSION.get(self.url, headers=self.headers, timeout=(8, 8))
            if response.status_code == 521:
                cookies = response.cookies
                str_js_cookie = response.text.replace("<script>document.", "").replace(
                    ";location.href=location.pathname+location.search</script>", "")
                js_result = execjs.eval(str_js_cookie).split(";")[0]
                self.first_cookie = ';'.join(['='.join(item) for item in cookies.items()])
                self.headers['cookie'] = self.first_cookie + "; " + js_result

                return True

            elif response.status_code == 200:
                return False  # 明确返回None
        except Exception as e:
            print(e)
            return False  # 在发生异常时返回None

    def second_cookie_decode(self):

        """
        破解第二次加密
        :param HEADERS: 浏览器请求头，首次破解加密字段一
        :return: 浏览器请求头，第二次破解加密字段二
        """   
        response = self.SESSION.get(self.url, headers=self.headers, timeout=(8, 8))

        if response.status_code == 521:

            response.encoding = 'utf-8' # 防止中文乱码

            # 处理js代码
            str_base = self.process_js(response.text)

            # 获取加密字段内容
            str_ie_cookie = self.get_js_cookie(str_base)

            str_base = self.replace_js(str_base,str_ie_cookie)

            return str_base

    def replace_js(self,str_base,str_ie_cookie):
        
        # 移除setTimeout
        index2 = str_base.find('setTimeout')
        if str_base[index2 - 1] == "(":
                str_base =  str_base.replace("(setTimeout,function(){",";")
        elif str_base[index2 - 1] == "}":
                str_base =  str_base.replace("setTimeout(function(){","")

        # 用str_ie_cookie代替document[到}else的内容
        index1 = str_base.find('document[')
        # ,_0x4cc2a6); 匹配这个格式的字符串
        pattern = r',_0x[0-9A-Fa-f]+\);'
        match = re.search(pattern, str_base[index1:])  

        # 补}，防止替换后语法错误

        re_str = str_base[index1:match.end()+index1]
        
        # 查找}的数量
        count = re_str.count("}")-1

        str_base = str_base[:index1] + str_ie_cookie + count*"}" + str_base[match.end()+index1:]
        return str_base

    def process_js(self,str_base):
            
            str_base = str_base.replace("</script>","").replace("<script>","")
            head_str= 'const jsdom = require("jsdom");const { JSDOM } = jsdom;const dom = new JSDOM(`<!DOCTYPE html><p>Hello world</p>`);window = dom.window;document = window.document;XMLHttpRequest = window.XMLHttpRequest;'
            str_cookie_index1 = 'var cookie = '
            index1 = str_base.find('go({')
            str_base = head_str + str_base[:index1] + str_cookie_index1 + str_base[index1:]+";function getCookie() {return cookie;};"

            return str_base

    def get_js_cookie(self,str_base):
        # 获取加密字段内容
        str_ie_cookie = str_base.replace(" ", "")[
                            str_base.replace(" ", "").find("'ie']=") + 6:str_base.replace(" ", "").find("location[")]
    
        str_cookie_index2 = 'var cookies={}return cookies;'.format(str_ie_cookie)


        return str_cookie_index2

    def execjs_cookie_decode(self,js):

        try:
            ct = execjs.compile(js,cwd=r'C:\Users\zax\AppData\Roaming\npm\node_modules')

            js_cookie = ct.call("getCookie")

            second_cookie = js_cookie.split(";")[0]

            return second_cookie
        
        except Exception as e:
            return None



    def get_header_cookie(self):

        """
        获取cookie
        :return: 返回cookie字典
        """
        flag = self.first_cookie_decode()

        if not flag:
            return None

        str_js = self.second_cookie_decode()
       
        cookie_second_decode = self.execjs_cookie_decode(str_js)

        if not cookie_second_decode:
            return None

        compile_cookie = self.first_cookie + "; " + cookie_second_decode

        # '__jsluid_s=12871b495b4524fe5fc82ec2ab9f8f7a;__jsl_clearance_s=1722578913.689|0|kSyFRz5yUtIOp26s%2B6OGoP2q0nk%3D'

        # 格式化为字典形式
        cookies = {}

        for item in compile_cookie.split(";"):
            key, value = item.split("=")
            cookies[key] = value


        return cookies

# if __name__ == '__main__':

#     header = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
#     }
#     jsl_js = JSL(headers=header,url ='https://www.zbytb.com/search/?kw=&okw=&catid=0&zizhi=&zdxm=&zdyear=&field=0&moduleid=25&areaids=&page=1')

#     he = jsl_js.get_cookie()
    
#     print(he)


  



