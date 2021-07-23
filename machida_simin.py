from bs4 import BeautifulSoup
import time  # for sleep
from scraper import Scraper
from selenium import webdriver # installしたseleniumからwebdriverを呼び出せるようにする
from selenium.webdriver.common.keys import Keys # webdriverからスクレイピングで使用するキーを使えるようにする。


class GroundNotifier(Scraper) :
    
    def __init__(self):
      super(GroundNotifier, self).__init__()

    def execute_main(self) :
      # TO_ADDRESS_1 = 'tk.cw.milds@gmail.com'
      TO_ADDRESS_2 = 'ohnukihiroki8585@yahoo.co.jp'
      SUBJECT = "町田市民球場に空きがあります"

      # 町田市公共施設予約システムのサイトを開く
      self.driver.get('https://www.pf489.com/machida/dselect.html')
      # 詳細条件を指定するページに移動する
      self.click('#content > div.wrap-content > div.secondbox.clearfix > div > h2 > a')

      # グラウンドの条件を記入
      # STEP2の施設選択で町田市民球場を選択
      self.click('#wpManager_gwppnlLeftZone_dgSSSelect_ctl11_cbSSSelect')
      # STEP3の期間で１ヶ月を選択
      self.click('#wpManager_gwppnlLeftZone_ucTermSettings_cmbTerm > option:nth-child(4)')
      # STEP3の曜日で日を選択
      self.click('#wpManager_gwppnlLeftZone_ucTermSettings_cblWeek_6')
      # # STEP3の時間帯で午後を選択
      # self.click('#wpManager_gwppnlLeftZone_ucTermSettings_cmbTime > option:nth-child(2)')
      # time.sleep(3)
      # # STEP3の時間帯で9時〜と入力
      # self.driver.find_element_by_xpath("//*[@id='wpManager_gwppnlLeftZone_ucTermSettings_txtTimeFrom']").send_keys("9")
      # # STEP3の時間帯で〜16時と入力
      # self.driver.find_element_by_xpath("//*[@id='wpManager_gwppnlLeftZone_ucTermSettings_txtTimeTo']").send_keys("16")
      # STEP4の空き照会をクリック
      self.click('#wpManager_gwppnlLeftZone_btnShoukai')
      # ソースコードを取得
      html_main = self.driver.page_source 
      # HTMLをパースする
      soup = BeautifulSoup(html_main, 'lxml') # または、'html.parser'

      # スクレイピングした《日曜日の日付》を変数に格納
      table_sun = soup.find_all(class_ = 'TitleColor')[0]
      table_month = soup.find_all(class_ = 'TitleColor')[0]
      # スクレイピングした《町田市のグラウンドの空き状況》を変数に格納
      table_simin = soup.find_all(id = "dlRepeat_ctl00_tpItem_dgTable")[0]
      # table_fuji = soup.find_all(id = "dlRepeat_ctl01_tpItem_dgTable")[0]
      # table_turu = soup.find_all(id = "dlRepeat_ctl02_tpItem_dgTable")[0]
      # table_midori = soup.find_all(id = "dlRepeat_ctl03_tpItem_dgTable")[0]
      # table_ono = soup.find_all(id = "dlRepeat_ctl04_tpItem_dgTable")[0]
      # table_nozuta = soup.find_all(id = "dlRepeat_ctl05_tpItem_dgTable")[0]


      # 日曜日の日付を格納する変数を宣言
      sunday_date = []
      # グラウンドの空き状況を格納する変数を宣言
      result_simin = []
      # result_fuji = []
      # result_turu = []
      # result_midori = []
      # result_ono = []
      # result_nozuta = []

      # 日曜日の日付をsunday_dateに格納する
      # スクレイピングしたものをテキスト化
      sunday_text = table_sun.get_text()
      sunday_text = sunday_text.replace('\n定員\n','')
      # sunday_textをトリミングして使いやすくする
      sunday_splits = sunday_text.split('月')
      sunday_date = sunday_splits[1]
      sunday_date = sunday_date.split('日')
      del sunday_date[0]
      del sunday_date[5]

      # グラウンドを利用する月をmonth_textに代入する
      month_text = table_month.get_text()
      month_text = month_text.replace('\n定員\n','')
      month_splits = month_text.split('月')
      month_date = month_splits[0]
      month_date = month_date.split('年')
      month_date = month_date[1]

      # 町田市民球場の空き状況をresuli_siminに格納する
      # 空き状況を1個ずつtext_siminnに格納する
      row_index_simin = 0
      rows_simin = table_simin.find_all('tr')
      for row_simin in rows_simin:
        row_index_simin += 1
        cells_simin = row_simin.find_all('td')
        for cell_simin in cells_simin:
          text_simin = cell_simin.find().get_text()
          #文字列から\xa0を消去する
          text_simin = text_simin.replace('\xa0','')
          #⚪︎△×のみをtext_siminに格納
          if (text_simin == "⚪︎" or text_simin == "△" or text_simin == "×"):
            result_simin.append(text_simin)

      # ループを用いてresult_siminに△か⚪︎があったらsunday_dateに紐ずける
      message_simin = "町田市民球場"
      pre_index_num_simin = 0
      index_num_simin = 0
      for item_simin in result_simin:
        pre_index_num_simin += 1
        if(item_simin != "×"):
          # message_siminに△か⚪︎があったら追加していく
          message_simin += "\n" + sunday_date[index_num_simin] + "日" + item_simin + "  空きあり"
          index_num_simin = pre_index_num_simin

      # 町田市民球場の空き状況に△があった場合はクリックする
      new_month_date = int(month_date) + 1;
      if("空きあり" in message_simin and sunday_date[index_num_simin] < sunday_date[0]):
        self.click('#dlRepeat_ctl00_tpItem_dgTable_ctl02_b2021' + '0' + str(new_month_date) + '0' + str(sunday_date[index_num_simin - 1]))
        time.sleep(2)
      if("空きあり" in message_simin and sunday_date[index_num_simin] > sunday_date[0]):
        self.click('#dlRepeat_ctl00_tpItem_dgTable_ctl02_b2021' + '0' + str(month_date) + '0' + str(sunday_date[index_num_simin - 1]))
        time.sleep(2)

      # 次へをクリック
      self.click('#ucPCFooter_btnForward')
      time.sleep(2)
      # ソースコードを取得
      html_simin = self.driver.page_source 
      # HTMLをパースする
      soup = BeautifulSoup(html_simin, 'lxml') # または、'html.parser'

      # スクレイピングした《町田市民球場の指定日の空き状況》をtable_simin2_textに格納
      table_simin2 = soup.find_all(id = "dlRepeat_ctl00_tpItem_dgTable")[0]
      table_simin2_text = table_simin2.get_text()

      # table_simin2_textをトリミングして使いやすくする
      table_simin2_text2 = table_simin2_text.split("－")
      del table_simin2_text2[0]
      table_simin2_text2 = table_simin2_text2[0].replace('\xa0','')
      table_simin2_text3 = list(table_simin2_text2)
      del table_simin2_text3[0]
      del table_simin2_text3[5]
      del table_simin2_text3[5]

      # ⚪︎がついている日にちを扱えるようにする
      index_num_simin2 = 0
      index_num_simin3 = 0
      for i in table_simin2_text3:
        index_num_simin2 += 1
        if (i == '○'):
          index_num_simin3 = index_num_simin2

      if(index_num_simin3 == 1):
        ground_time = "9:00~11:00"
      if(index_num_simin3 == 2):
        ground_time = "11:00~13:00"
      if(index_num_simin3 == 3):
        ground_time = "13:00~15:00"
      if(index_num_simin3 == 4):
        ground_time = "15:00~17:00"
      if(index_num_simin3 == 5):
        ground_time = "17:00~19:00"


      if(sunday_date[index_num_simin] < sunday_date[0]):
        message =  "町田市民球場" + " " + str(new_month_date) + "月" + str(sunday_date[index_num_simin-1]) + "日" + " " + ground_time + " " + str(table_simin2_text3[index_num_simin3-1])
      if(sunday_date[index_num_simin] > sunday_date[0]):
        message =  "町田市民球場" + " " + str(month_date) + "月" + str(sunday_date[index_num_simin-1]) + "日" + " " + ground_time + " " + str(table_simin2_text3[index_num_simin3-1])
     
      print(message)

      # self.driver.get('https://www.pf489.com/machida/dselect.html')
      # # 詳細条件を指定するページに移動する
      # self.click('#content > div.wrap-content > div.secondbox.clearfix > div > h2 > a')

      # # グラウンドの条件を記入
      # # STEP2の施設選択で藤の台球場を選択
      # self.click('#wpManager_gwppnlLeftZone_dgSSSelect_ctl12_cbSSSelect')
      # # STEP3の期間で１ヶ月を選択
      # self.click('#wpManager_gwppnlLeftZone_ucTermSettings_cmbTerm > option:nth-child(4)')
      # # STEP3の曜日で日を選択
      # self.click('#wpManager_gwppnlLeftZone_ucTermSettings_cblWeek_6')
      # # # STEP3の時間帯で午後を選択
      # # self.click('#wpManager_gwppnlLeftZone_ucTermSettings_cmbTime > option:nth-child(2)')
      # # time.sleep(3)
      # # # STEP3の時間帯で9時〜と入力
      # # self.driver.find_element_by_xpath("//*[@id='wpManager_gwppnlLeftZone_ucTermSettings_txtTimeFrom']").send_keys("9")
      # # # STEP3の時間帯で〜16時と入力
      # # self.driver.find_element_by_xpath("//*[@id='wpManager_gwppnlLeftZone_ucTermSettings_txtTimeTo']").send_keys("16")
      # # STEP4の空き照会をクリック
      # self.click('#wpManager_gwppnlLeftZone_btnShoukai')
      # # ソースコードを取得
      # html_main = self.driver.page_source 
      # # HTMLをパースする
      # soup = BeautifulSoup(html_main, 'lxml') # または、'html.parser'

      # # スクレイピングした《町田市のグラウンドの空き状況》を変数に格納
      # table_fuji = soup.find_all(id = "dlRepeat_ctl00_tpItem_dgTable")[0]
    
      # # 藤の台球場の空き状況をresuli_fujiに格納する
      # # 空き状況を1個ずつtext_fujiに格納する
      # row_index_fuji = 0
      # rows_fuji = table_fuji.find_all('tr')
      # for row_fuji in rows_fuji:
      #   row_index_fuji += 1
      #   cells_fuji = row_fuji.find_all('td')
      #   for cell_fuji in cells_fuji:
      #     text_fuji = cell_fuji.find().get_text()
      #     #文字列から\xa0を消去する
      #     text_fuji = text_fuji.replace('\xa0','')
      #     #⚪︎△×のみをtext_fujiに格納
      #     if (text_fuji == "⚪︎" or text_fuji == "△" or text_fuji == "×"):
      #       result_fuji.append(text_fuji)

      # # ループを用いてresult_fujiに△か⚪︎があったらsunday_dateに紐ずける
      # message_fuji = "藤の台球場"
      # pre_index_num_fuji = 0
      # index_num_fuji = 0
      # for item_fuji in result_fuji:
      #   pre_index_num_fuji += 1
      #   if(item_fuji != "×"):
      #     # message_fujiに△か⚪︎があったら追加していく
      #     message_fuji += "\n" + sunday_date[index_num_fuji] + "日" + item_fuji + "  空きあり"
      #     index_num_fuji = pre_index_num_fuji

      # # 藤の台球場の空き状況に△があった場合はクリックする
      # # new_month_date = int(month_date) + 1;
      # if("空きあり" in message_fuji and sunday_date[index_num_fuji] < sunday_date[0]):
      #   self.click('#dlRepeat_ctl00_tpItem_dgTable_ctl02_b2021' + '0' + str(new_month_date) + '0' + str(sunday_date[index_num_fuji - 1]))
      #   time.sleep(2)
      # if("空きあり" in message_fuji and sunday_date[index_num_fuji] > sunday_date[0]):
      #   self.click('#dlRepeat_ctl00_tpItem_dgTable_ctl02_b2021' + '0' + str(month_date) + '0' + str(sunday_date[index_num_fuji - 1]))
      #   time.sleep(2)

      # # 次へをクリック
      # self.click('#ucPCFooter_btnForward')
      # time.sleep(2)
      # # ソースコードを取得
      # html_fuji = self.driver.page_source 
      # # HTMLをパースする
      # soup = BeautifulSoup(html_fuji, 'lxml') # または、'html.parser'

      # # スクレイピングした《藤の台球場の指定日の空き状況》をtable_fuji2_textに格納
      # table_fuji2 = soup.find_all(id = "dlRepeat_ctl00_tpItem_dgTable")[0]
      # table_fuji2_text = table_fuji2.get_text()

      # # table_fuji2_textをトリミングして使いやすくする
      # table_fuji2_text2 = table_fuji2_text.split("－")
      # del table_fuji2_text2[0]
      # table_fuji2_text2 = table_fuji2_text2[0].replace('\xa0','')
      # table_fuji2_text3 = list(table_fuji2_text2)
      # del table_fuji2_text3[0]
      # del table_fuji2_text3[5]
      # del table_fuji2_text3[5]

      # # ⚪︎がついている日にちを扱えるようにする
      # index_num_fuji2 = 0
      # index_num_fuji3 = 0
      # for i in table_fuji2_text3:
      #   index_num_fuji2 += 1
      #   if (i == '○'):
      #     index_num_fuji3 = index_num_fuji2

      # if(index_num_fuji3 == 1):
      #   ground_time = "9:00~11:00"
      # if(index_num_fuji3 == 2):
      #   ground_time = "11:00~13:00"
      # if(index_num_fuji3 == 3):
      #   ground_time = "13:00~15:00"
      # if(index_num_fuji3 == 4):
      #   ground_time = "15:00~17:00"
      # if(index_num_fuji3 == 5):
      #   ground_time = "17:00~19:00"
      
      # message_fuji2 =  "藤の台球場" + " " + str(new_month_date) + "月" + str(sunday_date[index_num_fuji-1]) + "日" + " " + ground_time + " " + str(table_fuji2_text3[index_num_fuji3-1])
      # print(message_fuji2)

      # self.driver.get('https://www.pf489.com/machida/dselect.html')
      # # 詳細条件を指定するページに移動する
      # self.click('#content > div.wrap-content > div.secondbox.clearfix > div > h2 > a')

      # # グラウンドの条件を記入
      # # STEP2の施設選択で鶴川球場を選択
      # self.click('#wpManager_gwppnlLeftZone_dgSSSelect_ctl13_cbSSSelect')
      # # STEP3の期間で１ヶ月を選択
      # self.click('#wpManager_gwppnlLeftZone_ucTermSettings_cmbTerm > option:nth-child(4)')
      # # STEP3の曜日で日を選択
      # self.click('#wpManager_gwppnlLeftZone_ucTermSettings_cblWeek_6')
      # # # STEP3の時間帯で午後を選択
      # # self.click('#wpManager_gwppnlLeftZone_ucTermSettings_cmbTime > option:nth-child(2)')
      # # time.sleep(3)
      # # # STEP3の時間帯で9時〜と入力
      # # self.driver.find_element_by_xpath("//*[@id='wpManager_gwppnlLeftZone_ucTermSettings_txtTimeFrom']").send_keys("9")
      # # # STEP3の時間帯で〜16時と入力
      # # self.driver.find_element_by_xpath("//*[@id='wpManager_gwppnlLeftZone_ucTermSettings_txtTimeTo']").send_keys("16")
      # # STEP4の空き照会をクリック
      # self.click('#wpManager_gwppnlLeftZone_btnShoukai')
      # # ソースコードを取得
      # html_main = self.driver.page_source 
      # # HTMLをパースする
      # soup = BeautifulSoup(html_main, 'lxml') # または、'html.parser'

      # # スクレイピングした《町田市のグラウンドの空き状況》を変数に格納
      # table_turu = soup.find_all(id = "dlRepeat_ctl00_tpItem_dgTable")[0]
    
      # # 鶴川球場の空き状況をresuli_turuに格納する
      # # 空き状況を1個ずつtext_turuに格納する
      # row_index_turu = 0
      # rows_turu = table_turu.find_all('tr')
      # for row_turu in rows_turu:
      #   row_index_turu += 1
      #   cells_turu = row_turu.find_all('td')
      #   for cell_turu in cells_turu:
      #     text_turu = cell_turu.find().get_text()
      #     #文字列から\xa0を消去する
      #     text_turu = text_turu.replace('\xa0','')
      #     #⚪︎△×のみをtext_turuに格納
      #     if (text_turu == "⚪︎" or text_turu == "△" or text_turu == "×"):
      #       result_turu.append(text_turu)

      # # ループを用いてresult_turuに△か⚪︎があったらsunday_dateに紐ずける
      # message_turu = "鶴川球場"
      # pre_index_num_turu = 0
      # index_num_turu = 0
      # for item_turu in result_turu:
      #   pre_index_num_turu += 1
      #   if(item_turu != "×"):
      #     # message_turuに△か⚪︎があったら追加していく
      #     message_turu += "\n" + sunday_date[index_num_turu] + "日" + item_turu + "  空きあり"
      #     index_num_turu = pre_index_num_turu

      # # 鶴川球場の空き状況に△があった場合はクリックする
      # # new_month_date = int(month_date) + 1;
      # if("空きあり" in message_turu and sunday_date[index_num_turu] < sunday_date[0]):
      #   self.click('#dlRepeat_ctl00_tpItem_dgTable_ctl02_b2021' + '0' + str(new_month_date) + '0' + str(sunday_date[index_num_turu - 1]))
      #   time.sleep(2)
      # if("空きあり" in message_turu and sunday_date[index_num_turu] > sunday_date[0]):
      #   self.click('#dlRepeat_ctl00_tpItem_dgTable_ctl02_b2021' + '0' + str(month_date) + '0' + str(sunday_date[index_num_turu - 1]))
      #   time.sleep(2)

      # # 次へをクリック
      # self.click('#ucPCFooter_btnForward')
      # time.sleep(2)
      # # ソースコードを取得
      # html_turu = self.driver.page_source 
      # # HTMLをパースする
      # soup = BeautifulSoup(html_turu, 'lxml') # または、'html.parser'

      # # スクレイピングした《藤の台球場の指定日の空き状況》をtable_turu2_textに格納
      # table_turu2 = soup.find_all(id = "dlRepeat_ctl00_tpItem_dgTable")[0]
      # table_turu2_text = table_turu2.get_text()

      # # table_turu2_textをトリミングして使いやすくする
      # table_turu2_text2 = table_turu2_text.split("－")
      # del table_turu2_text2[0]
      # table_turu2_text2 = table_turu2_text2[0].replace('\xa0','')
      # table_turu2_text3 = list(table_turu2_text2)
      # del table_turu2_text3[0]
      # del table_turu2_text3[5]
      # del table_turu2_text3[5]

      # # ⚪︎がついている日にちを扱えるようにする
      # index_num_turu2 = 0
      # index_num_turu3 = 0
      # for i in table_turu2_text3:
      #   index_num_turu2 += 1
      #   if (i == '○'):
      #     index_num_turu3 = index_num_turu2

      # if(index_num_turu3 == 1):
      #   ground_time = "9:00~11:00"
      # if(index_num_turu3 == 2):
      #   ground_time = "11:00~13:00"
      # if(index_num_turu3 == 3):
      #   ground_time = "13:00~15:00"
      # if(index_num_turu3 == 4):
      #   ground_time = "15:00~17:00"
      # if(index_num_turu3 == 5):
      #   ground_time = "17:00~19:00"
      
      # message_turu2 =  "鶴川球場" + " " + str(new_month_date) + "月" + str(sunday_date[index_num_turu-1]) + "日" + " " + ground_time + " " + str(table_turu2_text3[index_num_turu3-1])
      # print(message_turu2)

      # ブラウザを終了する
      self.driver.quit()
    

    #   message = message_simin + "\n\n" + message_fuji + "\n\n" + message_turu + "\n\n" + message_midori + "\n\n" + message_ono + "\n\n" + message_nozuta + "\n\n" +"https://www.pf489.com/machida/"

      # LINEに通知させる
      # self.line_notify(message)

      # グラウンドに空きがあったらメールを送る。無かったら何もしない。
      if("○" in message):
        #メール送信
        # msg = self.create_mail(TO_ADDRESS_1, '', SUBJECT, message)
        # self.send(TO_ADDRESS_1, msg)
        msg = self.create_mail(TO_ADDRESS_2, '', SUBJECT, message)
        self.send(TO_ADDRESS_2, msg)
      else:
        print("空きなし")
        # pass

if __name__ == '__main__':
  notifier = GroundNotifier()
  notifier.execute_main()

