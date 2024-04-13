
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import smtplib
from email.mime.text import MIMEText


last_found_list = []

while True:
    url = 'https://www.mydealz.de/diskussion/kunden-werben-kunden-regeln-1764080'
    dr = webdriver.Chrome()
    dr.implicitly_wait(10)
    dr.get(url)
    dr.find_element(By.CSS_SELECTOR, 'button[class="overflow--wrap-on flex--grow-1 flex--fromW3-grow-0 width--fromW3-ctrl-m space--mb-3 space--fromW3-mb-0 space--fromW3-mr-2 button button--shape-circle button--type-primary button--mode-brand"]').click()
    time.sleep(1)
    dr.find_element(By.CSS_SELECTOR, 'button[aria-label="Letzte Seite"]').click()
    time.sleep(6)
    soup = BeautifulSoup(dr.page_source, 'html.parser')
    page_text = soup.get_text()

    search_words = ['Amex', "American"]  # todo: need to change, search words
    for word in search_words:
        if word in page_text:
            # check if the word is already found and email sent
            word_area = page_text[page_text.find(word):page_text.find(word)+len(word)+25]
            if word_area not in last_found_list:
                last_found_list.append(word_area)
            else:
                continue

            # send email
            sender_email = 'sender@outlook.com'             # todo: need to change, sender email, must be outlook
            recipient_email = 'recipient_email@xxx.com'     # todo: need to change, recipient email
            subject = 'Keyword Found in Page'               # todo: need to change, email title
            message = page_text[page_text.find(word)-50:page_text.find(word)+len(word)+50]              # todo: need to change, email message
            smtp_server = 'smtp-mail.outlook.com'
            smtp_port = 587
            smtp_username = 'ender@outlook.com'             # todo: need to change, sender email username
            smtp_password = 'PASSWORT'                      # todo: need to change, sender email password

            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            msg = MIMEText(message)
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg['To'] = recipient_email
            server.sendmail(sender_email, recipient_email, msg.as_string())
            server.quit()

    time.sleep(60*5)  # todo: need to change, currently it will run every 5 minutes
