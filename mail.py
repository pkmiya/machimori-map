from flask_mail import Mail, Message
#from flask import Flask

class My_Mail:
    def __init__(self, app):
        self.mail = Mail(app)

    def ab_send_mail(self, mail_addresses):
        email_sender = "sender@example.com"

        msg = Message("[まちもりブザー]異常を検知しました", #title
                      sender=email_sender, # 送信元
                      recipients=mail_addresses, # 送信先
                      charset="shift_jis") # 日本語表示するため
        msg.html = """
        <!DOCTYPE html>
        <head>
        </head>
        <body style="background-color:rgb(255,183,36);color:black;padding: 1em 2em;">
        <header>
        <div class="header-logo">
            <h2>まちもりブザーからのお知らせ</h2>
        </div>
        </header>
        <p>こんにちは、〇〇さま。まちもりブザーのからのお知らせです。</p>
        <p>〇〇さまのまちもりブザーで異常を検知しました。<br>お子様が普段の通学路から外れた場所を歩いている可能性がありますのでご注意ください。</p>
        <br>
        <p>以下のサイトで、街の危険エリアやこどもをまもるいえを示した「まちもりマップ」がご確認できます。</p>
        <p>machimori.japanwest.cloudapp.azure.com</p>
        </body>
        </html>
        """
        self.mail.send(msg) #メール送信

    # parent buzzer
    def pbz_send_mail(self, senddata):
        msg = Message("[まちもりブザー]ブザーが鳴らされました",
                      sender=email_sender,
                      bcc=[senddata[0][1]],
                      charset="shift_jis")
        msg.html = """
        <!DOCTYPE html>
        <head>
        </head>
        <body style="background-color:rgb(255,183,36);color:black;padding: 1em 2em;">
        <header>
        <div class="header-logo">
            <h2>まちもりブザーからのお知らせ</h2>
        </div>
        </header>
        <p>こんにちは、{0}さま。まちもりブザーのからのお知らせです。</p>
        <p>{0}さまのまちもりブザーが鳴らされました。<br>お子様に何らかの危険が迫っている可能性がありますのでご注意ください。</p>
        <br> 
        <p>もし誤操作だった場合は、こちらのサイトにアクセスしていただき、お取消しいただきますようお願いします。</p>
        <p>machimori_buzzer.torikeshi.com</p>
        <br>
        <p>以下のサイトで、街の危険エリアやこどもをまもるいえを示した「まちもりマップ」がご確認できます。</p>
        <p>machimori.japanwest.cloudapp.azure.com</p>
        </body>
        </html>
        """.format(senddata[0][0])
        self.mail.send(msg)

    # safeguard buzzer
    def sbz_send_mail(self, sdata):
        for sd in sdata:
            msg = Message("[まちもりブザー]ブザーが鳴らされました",
                          sender=email_sender,
                          bcc=[sd['mail_address']],
                          charset="shift_jis")
            msg.html = """
            <!DOCTYPE html>
            <head>
            </head>
            <body style="background-color:rgb(255,183,36);color:black;padding: 1em 2em;">
            <header>
            <div class="header-logo">
                <h2>まちもりブザーからのお知らせ</h2>
            </div>
            </header>
            <p>こんにちは、{0}さま。まちもりブザーのからのお知らせです。</p>
            <p>{0}さまのまちもりブザーが鳴らされました。<br>お子様に何らかの危険が迫っている可能性がありますのでご注意ください。</p>
            <br> 
            <p>もし誤操作だった場合は、こちらのサイトにアクセスしていただき、お取消しいただきますようお願いします。</p>
            <p>machimori_buzzer.torikeshi.com</p>
            <br>
            <p>以下のサイトで、街の危険エリアやこどもをまもるいえを示した「まちもりマップ」がご確認できます。</p>
            <p>machimori.japanwest.cloudapp.azure.com</p>
            </body>
            </html>
            """.format(sd['name'])
            self.mail.send(msg)

    def wio_get_mail(self, mail_addresses, flag_text, lat, lon):
        msg = Message("[連絡用]Wioからデータがきました",
                      sender=email_sender,
                      bcc=mail_addresses,
                      charset="shift_jis")
        msg.body = "Wioからデータがきました。\n" + flag_text + "\nlat : " + str(lat) + "\nlon : " + str(lon)
        self.mail.send(msg)

    def p_registration_mail(self, mail_addresses, parent_name, parent_ID):
        msg = Message("[まちもりブザー]ブザー新規登録",
                      sender=email_sender,
                      recipients=mail_addresses,
                      charset="shift_jis")
        msg.html = """
        %sさんのIDは%sです
        """ % (parent_name, parent_ID)
        self.mail.send(msg)

    def s_registration_mail(self, mail_addresses, parent_name, parent_ID):
        msg = Message("[まちもりブザー]こどもをまもるいえ新規登録",
                      sender=email_sender,
                      recipients=mail_addresses,
                      charset="shift_jis")
        msg.html = """
        %sさんのIDは%sです
        """ % (parent_name, parent_ID)
        self.mail.send(msg)

if __name__ == "__main__":
    print('done')
