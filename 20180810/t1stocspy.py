import requests
from bs4 import BeautifulSoup
import traceback
import re
def getHTMLText(url,code="utf-8"):
     try:
        #headers = {'user-agent': 'my-app/0.0.1'}
        r=requests.get(url,timeout =30)
        r.raise_for_status()
        r.encoding=code
       # print(r.text)
        return r.text        
     except:
        return""
def getStockList(lst,stockURL):
    html=getHTMLText(stockURL,"GB2312")
    soup=BeautifulSoup(html,'html.parser')
    a=soup.find_all('a')
    k=0
    for i in a:
        try:
            k+=1
            href=i.attrs['href']
            rfind=re.findall(r"[s][hz]\d{6}",href)[0]
            #print(re.findall(r"[s][hz]\d{6})",href)[0])
            lst.append(rfind)
        except:
            continue
def getStockInfo(lst,stockURL,fpath):
    count=0
    for stock in lst:
        url=stockURL+stock+".html"
        html=getHTMLText(url)
        try:
            if html =='':
                continue
            infoDict={}
            soup = BeautifulSoup(html,"html.parser")
            stockInfo=soup.find('div',attrs={'class':'stock-bets'})
            name=stockInfo.find_all(attrs={'class':'bets-name'})[0]
            infoDict.update({'股票名称':name.text.split()[0]})
            keyList=stockInfo.find_all('dt')
            valueList=stockInfo.find_all('dd')
            for i in range(len(keyList)):
                key=keyList[i].text
                val=valueList[i].text
                infoDict[key]=val
            
            with open(fpath,'a',encoding='utf-8') as f:
                f.write(str(infoDict)+'\n')
                count +=1
                print ('\r当前进度：{:.2f}%'.format(count*100/len(lst)),end='')
            
        except:
            traceback.print_exc()
            count +=1
            print ('\r当前进度：{:.2f}%'.format(count*100/len(lst)),end='')
            continue
def main():
    stock_list_url='http://quote.eastmoney.com/stocklist.html'
    stock_info_url='https://gupiao.baidu.com/stock/'
    output_file='C:\\pyNote\\BaiduStockInfo.txt'
    sList=[]
    getStockList(sList,stock_list_url)
    getStockInfo(sList,stock_info_url,output_file)


main()