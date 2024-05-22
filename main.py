#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, re
from selenium.common.exceptions import ElementClickInterceptedException
import selenium
import time

# 시작 시간 기록
start_time = time.time()

# 브라우저 옵션 설정
options = webdriver.ChromeOptions()
options.add_argument("--disable-extensions")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-notifications")
# headless 모드를 비활성화하여 브라우저를 실제로 열어 놓음
# options.add_argument("--headless")  # 주석 처리하여 headless 모드 비활성화

# 웹 드라이버 초기화
driver = webdriver.Chrome(options=options)
driver.maximize_window()

# 1. 페이지 접속
driver.get('https://lab.incruit.com/editor/spell/')

# 2. 글자수 제한 설정 버튼 클릭 (드랍다운 메뉴)
# ElementClickInterceptedException 예외를 처리하여 재시도
while True:
    try:
        WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.d-tool-calc-btn'))
        ).click()
        break
    except selenium.common.exceptions.ElementClickInterceptedException:
        time.sleep(1)

# 3. 글자수 제한. 15000 대신 99999을 입력 -> 설정 버튼 클릭
text_limit_input = WebDriverWait(driver, 2).until(
    EC.presence_of_element_located((By.ID, 'tl_maxlenset'))
)
text_limit_input.clear()
text_limit_input.send_keys('99999')
driver.find_element(By.ID, 'tl_textlenset').click()

# 4. 내용을 입력해주세요 (placeholder="내용을 입력해주세요.")에 맞춤법 검사를 원하는 텍스트 입력.
text_area = WebDriverWait(driver, 2).until(
    EC.presence_of_element_located((By.ID, 'tl_memo'))
)

# 텍스트 파일 내용 읽기
with open('맞춤법TEST_v2.txt', 'r', encoding='utf-8') as file:
    text_to_check = file.read()

text_area.send_keys(text_to_check)


# 5. 맞춤법 검사 버튼 클릭
WebDriverWait(driver, 2).until(
    EC.element_to_be_clickable((By.ID, 'spell-check'))
).click()

# 6. (맞춤법 오류가 없는 경우에만) 팝업창의 아래 확인 버튼 클릭
try:
    no_error_popup = WebDriverWait(driver, 2).until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), '오타가 없습니다.')]"))
    )
    if no_error_popup:
        confirm_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '오타가 없습니다.')]/following::button[@class='on'][1]"))
        )
        confirm_button.click()
        print("맞춤법에 오류가 없습니다.")
        driver.quit()
        end_time = time.time()
        print(f"전체 수행 시간: {end_time - start_time:.2f} 초")
        print("맞춤법 검사를 마쳤습니다.")
except:
    # 스크롤을 제일 위로 올리는 구문 추가
    driver.execute_script("window.scrollTo(0, 0);")

    # 7. 모두수정 버튼 클릭
    WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.ID, 'spell-modify'))
    ).click()

    # 8. 아래 팝업 창에서 확인 클릭
    WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@onclick=\"fn_spellModifyAllV2();$('.dPosLayer').removeClass('open');$('html').removeClass('noFlow');\"]"))
    ).click()

    # 9. 전체 복사 버튼 클릭 이전에 빈칸 추가 구문
    text = text_area.get_attribute('value')
    corrected_text = re.sub(r'(?<=\.)(?=\S)', ' ', text)
    
    # 파일로 저장
    with open('corrected_text.txt', 'w', encoding='utf-8') as file:
        file.write(corrected_text)

    # 브라우저 닫기
    driver.quit()
    end_time = time.time()
    print(f"전체 수행 시간: {end_time - start_time:.2f} 초")
    print("맞춤법 검사를 마쳤습니다.")
