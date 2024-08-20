from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import exceptions as SE
from selenium.webdriver.common.keys import Keys


def get_ss_from_twitch():
    # Set up Chrome driver
    mobile_emulation = {"deviceName": "Nexus 5"}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    driver = webdriver.Chrome(
        options=chrome_options
    )
    driver.get("https://m.twitch.tv")

    # Wait for the Search button to be clickable
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/search']"))
    )

    # Click the button
    button.click()

    input_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input"))
    )

    input_field.send_keys("Starcraft II")
    input_field.send_keys(Keys.RETURN)

    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Channels"))
    )
    # Click the Channels button
    button.click()

    # Scroll down twice
    scroll_pause_time = 1  # Time to wait after each scroll

    for _ in range(2):
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(scroll_pause_time)

    # Click on a stream link in the active window
    stream_links = driver.find_elements(By.TAG_NAME, "h2")
    for stream_link in stream_links:
        try:
            stream_link.click()
            break
        except SE.ElementClickInterceptedException:
            continue
        raise Exception

    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//video"))
    )

    # JavaScript code to wait for the video to start playing
    js_script = """
        return new Promise((resolve) => {
            const video = document.querySelector('video');
            if (video && video.readyState >= 3) {
                resolve(true);
            } else {
                video.addEventListener('playing', () => {
                    resolve(true);
                }, { once: true });
            }
        });
    """

    # Wait until the video starts playing
    WebDriverWait(driver, 60).until(lambda d: d.execute_script(js_script))

    # Stamp screenshots so that they won't be overwritten
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_filename = f"twitch_screenshot_{timestamp}.png"

    # Take a screenshot once the video is playing
    driver.save_screenshot(screenshot_filename)


if __name__ == "__main__":
    get_ss_from_twitch()
