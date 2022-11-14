import time, random, csv, pyautogui, traceback
from builtins import print

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from itertools import product


class diceBot:
    def __init__(self, parameters, driver):
        self.browser = driver
        self.parameters = parameters
        self.email = parameters['emailDice']
        self.password = parameters['passwordDice']
        self.disable_lock = parameters['disableAntiLock']
        self.company_blacklist = parameters.get('companyBlacklist', []) or []
        self.title_blacklist = parameters.get('titleBlacklist', []) or []
        self.positions = parameters.get('positions', [])
        self.locations = parameters.get('locations', [])
        self.base_search_url = ""
        self.seen_jobs = []
        self.file_name = "output"
        self.output_file_directory = parameters['outputFileDirectory']
        self.resume_dir = parameters['uploads']['resume']
        if 'coverLetter' in parameters['uploads']:
            self.cover_letter_dir = parameters['uploads']['coverLetter']
        else:
            self.cover_letter_dir = ''
        self.checkboxes = parameters.get('checkboxes', [])
        self.university_gpa = parameters['universityGpa']
        self.languages = parameters.get('languages', [])
        self.industry = parameters.get('industry', [])
        self.technology = parameters.get('technology', [])
        self.personal_info = parameters.get('personalInfo', [])
        self.eeo = parameters.get('eeo', [])
        self.technology_default = self.technology['default']
        self.industry_default = self.industry['default']
        self.currentURL = "dice.com/jobs?"

    def login(self):
        try:
            self.browser.get("https://www.dice.com/dashboard/login")
            time.sleep(random.uniform(5, 10))
            self.browser.find_element(By.ID, "email").send_keys(self.email)
            self.browser.find_element(By.ID, "password").send_keys(self.password)
            self.browser.find_element(By.CSS_SELECTOR, ".btn.btn-primary").click()
            time.sleep(random.uniform(5, 10))
        except TimeoutException:
            raise Exception("Could not login!")

    def security_check(self):
        current_url = self.browser.current_url
        page_source = self.browser.page_source

        if '/checkpoint/challenge/' in current_url or 'security check' in page_source:
            input("Please complete the security check and press enter in this console when it is done.")
            time.sleep(random.uniform(5.5, 10.5))

    def start_applying(self):
        searches = list(product(self.positions, self.locations))
        random.shuffle(searches)

        pageSleep = 0
        minimum_time = 60 * 15
        minimum_page_time = time.time() + minimum_time

        for (position, location) in searches:
            self.currentURL = self.browser.current_url
            # Begins the search by creating a base url with information from config.yaml
            print("Starting the search for " + position + " in " + location + ".")
            position = position.replace(" ", "%")

            self.browser.get("https://www.dice.com/jobs?" + self.get_base_search_url(self.parameters, position, "1"))
            jobPageNum = 0

            try:
                while True:
                    pageSleep += 1
                    jobPageNum += 1
                    print("Going to job page " + str(jobPageNum))
                    time.sleep(random.uniform(1.5, 3.5))
                    print("Starting the application process for this page...")
                    self.apply_jobs(location)
                    print("Applying to jobs on this page has been completed!")

                    time_left = minimum_page_time - time.time()
                    if time_left > 0:
                        print("Sleeping for " + str(time_left) + " seconds.")
                        time.sleep(time_left)
                        minimum_page_time = time.time() + minimum_time
                    if pageSleep % 5 == 0:
                        sleep_time = random.randint(500, 900)
                        print("Sleeping for " + str(sleep_time / 60) + " minutes.")
                        time.sleep(sleep_time)
                        pageSleep += 1
            except:
                traceback.print_exc()
                pass

            time_left = minimum_page_time - time.time()
            if time_left > 0:
                print("Sleeping for " + str(time_left) + " seconds.")
                time.sleep(time_left)
                minimum_page_time = time.time() + minimum_time
            if pageSleep % 5 == 0:
                sleep_time = random.randint(500, 900)
                print("Sleeping for " + str(sleep_time / 60) + " minutes.")
                time.sleep(sleep_time)
                pageSleep += 1

    def apply_jobs(self, location):
        no_jobs_text = ""
        try:
            no_jobs_element = self.browser.find_element(By.CLASS_NAME, 'no-jobs-message')
            no_jobs_text = no_jobs_element.text
        except:
            pass
        if 'No matching jobs found' in no_jobs_text:
            raise Exception("No more jobs on this page")

        if 'we were unable to find any results' in self.browser.page_source.lower():
            raise Exception("No more jobs on this page")

        try:
            job_list = self.browser.find_elements(By.CSS_SELECTOR, 'div.card.search-card')
        except:
            raise Exception("No more jobs on this page")

        if len(job_list) == 0:
            raise Exception("No more jobs on this page")
        jobNum = 0
        jobLinks = []
        searchURL = self.browser.current_url
        for jobTile in job_list:
            print("Job number " + str(jobNum))
            jobNum += 1
            try:
                try:
                    jobTile.find_element(By.XPATH, "/html/body/dhi-js-dice-client/div/dhi-search-page-container/dhi-search-page/div/dhi-search-page-results/div/div[3]/js-search-display/div/div[3]/dhi-search-cards-widget/div/dhi-search-card[1]/div/div[1]/div/div[1]/dhi-status-ribbon/div/div/div/span" == None)
                    print("Already applied to job")
                except:
                    titleTile = jobTile.find_element(By.CLASS_NAME, "card-header").find_element(By.CLASS_NAME, "m-card-header-margin-left").find_element(By.CLASS_NAME, "d-flex").find_element(By.TAG_NAME, "h5").find_element(By.TAG_NAME, "a")
                    title = titleTile.text.split('\n')[0]
                    for word in self.title_blacklist:
                        if word.lower() in title:
                            raise Exception("Blacklisted job title")
                    jobLinks += [self.browser.find_element(By.LINK_TEXT, title).get_attribute('href')]
            except:
                print("failed to get link")
                traceback.print_exc()
                pass

            contains_blacklisted_keywords = False
        for jobLink in jobLinks:
            if jobLink not in self.seen_jobs:
                try:
                    self.browser.get(jobLink)
                    time.sleep(random.uniform(3, 5))
                    try:
                        done_applying = self.apply_to_job()
                        if done_applying:
                            print("Done applying to the job!")
                        else:
                            print('Already applied to the job!')
                    except:
                        traceback.print_exc()
                except:
                    traceback.print_exc()
                    print("Could not apply to the job!")
                    pass
            else:
                print("Job contains blacklisted keyword or company name!")

            self.seen_jobs += jobLink
            self.browser.get(searchURL)

            time.sleep(random.uniform(5, 10))

    def apply_to_job(self):
        try:
            time.sleep(random.uniform(5, 10))
            firstApplyButton = self.browser.find_element(By.XPATH, "/html/body/div[3]/div[5]/div[2]/div[2]/div/div[2]/div[1]/dhi-wc-apply-button")
            firstApplyButton.click()
            time.sleep(random.uniform(5, 10))
            secondApplyButton = self.browser.find_element(By.XPATH, "/html/body/div[3]/div[4]/div/div[1]/div/div/span/div/main/div[4]/button[2]")
            secondApplyButton.click()
            time.sleep(random.uniform(5, 10))
            thirdApplyButton = self.browser.find_element(By.XPATH, "/html/body/div[4]/div[4]/div/div[1]/div/div/span/div/main/div[3]/button[2]")
            thirdApplyButton.click()
            return True

        except:
            traceback.print_exc()
            return False


    def write_to_file(self, company, job_title, link, location, search_location):
        to_write = [company, job_title, link, location]
        file_path = self.output_file_directory + self.file_name + search_location + ".csv"

        with open(file_path, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(to_write)

    def scroll_slow(self, start=0, end=3600, step=100, reverse=False):
        if reverse:
            start, end = end, start
            step = -step

        for i in range(start, end, step):
            self.browser.execute_script("window.scrollTo(0, {})".format(i))
            time.sleep(random.uniform(1.0, 2.6))

    def avoid_lock(self):
        if self.disable_lock:
            return

        pyautogui.keyDown('ctrl')
        pyautogui.press('esc')
        pyautogui.keyUp('ctrl')
        time.sleep(1.0)
        pyautogui.press('esc')

    def get_base_search_url(self, parameters, position, newPageURL):

        countryCode = "countryCode=US"
        radiusURL = "radiusUnit=mi"
        radiusUnitURL = "radius=30"
        pageSizeURL = "pageSize=100"
        languageURL = "language=en"
        easyApplyUrl = "filters.easyApply=true"

        if newPageURL == "":
            pageURL = "page=1"
        else:
            pageURL = str(newPageURL)

        if position == "":
            jobURL = ""
        else:
            jobURL = "q=" + str(position)

        dates = {"all time": "", "7 Days": "SEVEN", "3 Days": "THREE", "Today": "ONE"}
        date_table = parameters.get('dateDice', [])
        for key in date_table.keys():
            if date_table[key]:
                dateURL = "filters.postedDate=" + str(dates[key])
                break
            else:
                dateURL = ""

        jobTypes = {"full-time": "FULLTIME", "part-time": "PARTTIME", "contract": "CONTRACT", "third-party": "THIRDPARTY"}
        job_table = parameters.get('jobTypes', [])
        for key in job_table.keys():
            if job_table[key]:
                jobTypeURL = "filters.employmentType=" + str(jobTypes[key])
                break

        searchTerms = [jobURL, countryCode, radiusURL, radiusUnitURL, pageURL, pageSizeURL, dateURL, jobTypeURL, languageURL, easyApplyUrl]
        extra_search_terms_str = '&'.join(filter(None,searchTerms))
        print(extra_search_terms_str)
        return extra_search_terms_str

    def next_job_page(self, job_page):
        self.avoid_lock()
        new_page = "page=" + job_page
        self.get_base_search_url(self.parameters, "")

