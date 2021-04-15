import warnings
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from dataextraction.management.commands.constants import Constants
from selenium.common.exceptions import \
    TimeoutException, \
    SessionNotCreatedException, \
    ErrorInResponseException, \
    WebDriverException, \
    InvalidElementStateException, \
    NoSuchElementException, \
    RemoteDriverServerException, \
    StaleElementReferenceException, \
    UnexpectedAlertPresentException
from .LoadDataException import LoadDataExeception


class WebdriverLoader:
    driver = None
    waitTime = 0
    waitElement = None

    def __init__(self, wait_time):
        try:
            warnings.filterwarnings("ignore")
            self.waitTime = wait_time
            self.driver = webdriver.PhantomJS(executable_path=Constants.PHANTOMJS_EXE)
        except SessionNotCreatedException as e:
            raise LoadDataExeception("SESSION_NOT_CREATED", e)
        except RemoteDriverServerException as e:
            raise LoadDataExeception("REMOTE_DRIVER", e)
        except WebDriverException as e:
            raise LoadDataExeception("WEBDRIVER_EXCEPTION", e)
        except Exception as e:
            raise e

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.close()

    def start_phantom(self, url):
        try:
            self.driver.get(url)
            self.waitElement = WebDriverWait(self.driver, self.waitTime)
        except TimeoutException as e:
            raise LoadDataExeception("TIMEOUT", e)
        except ErrorInResponseException as e:
            raise LoadDataExeception("RESPONSE_ERROR", e)
        except RemoteDriverServerException as e:
            raise LoadDataExeception("REMOTE_DRIVER", e)
        except WebDriverException as e:
            raise LoadDataExeception("WEBDRIVER_EXCEPTION", e)
        except Exception as e:
            raise e

    def get_elements(self, xpath):
        try:
            self.waitElement.until(EC.presence_of_element_located((By.XPATH, xpath)))
            return self.driver.find_elements_by_xpath(xpath)
        except InvalidElementStateException as e:
            raise LoadDataExeception("INVALID_STATE", e)
        except TimeoutException as e:
            raise LoadDataExeception("TIMEOUT_EXCEPTION", e)
        except NoSuchElementException as e:
            raise LoadDataExeception("NO_SUCH_ELEMENT", e)
        except StaleElementReferenceException as e:
            raise LoadDataExeception("NO_SUCH_ELEMENT", e)
        except UnexpectedAlertPresentException as e:
            raise LoadDataExeception("NO_SUCH_ELEMENT", e)
        except Exception as e:
            raise e

    def get_url_text_map(self, elements):
        try:
            return {ele.text: ele.get_attribute("href") for ele in elements}
        except StaleElementReferenceException as e:
            raise LoadDataExeception("NO_SUCH_ELEMENT", e)
        except TimeoutException as e:
            raise LoadDataExeception("TIMEOUT_EXCEPTION", e)
        except WebDriverException as e:
            raise LoadDataExeception("WEBDRIVER_EXCEPTION", e)
        except Exception as e:
            raise e
