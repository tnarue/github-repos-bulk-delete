import time
import githubdelete.util as util
import githubdelete.githubdelete as gitdelete

username = "Your User Name"
password = "Your Password"
t = 5  # set time of delay
repo_exception_list = ['add list of repos that you do not want to delete']
string_to_delete_list = ['test']

driver = util.browser_start()
driver = util.github_login(driver, username, password)
time.sleep(40)

reposurl = util.get_pageurl(username, 1)


driver.get(reposurl)
time.sleep(t)
total_page = util.get_totalpage(driver)

# use this if you want to bulk delete all repositories
gitdelete.bulk_delete_all(driver, username, t)

# use this if you want to bulk delete all repositories except repositories in given list
gitdelete.bulk_delete_with_exception(driver, username, t, repo_exception_list)

# use this if you want to bulk delete any repositories that their name contain given string list
driver = gitdelete.bulk_delete_by_reponame(driver, username, t, string_to_delete_list)

driver.exit()
