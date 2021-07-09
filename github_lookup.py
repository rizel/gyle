from playwright.sync_api import sync_playwright
from pprint import pprint


def snapshot_user(context, username):
    users_page_url  = f"https://github.com/{username}?tab=repositories"
    users_page      = context.new_page()
    users_page.goto(users_page_url)
    users_page.screenshot(path=f"repositories_of_{username}.png")
    users_page.close()
    return users_page_url
            

# this function executed with at least one user in the search result.
def look_for_best_match(context, page, total_users):
    # first user data, as best match by default.
    best_user_match = {
        'users_url' : None,
        'username'  : None,
        'about_user': None
    }
    user_found  = False

    for user_index in range(1,total_users+1):
        best_user_match['username']    = page.eval_on_selector( f":nth-match(a.color-text-secondary, {user_index})", 'e => e.textContent')
        best_user_match['about_user']  = page.eval_on_selector(f":nth-match(.mb-1, {user_index})", 'e => e.textContent')
        print(best_user_match['username'])

        # try to match the user.
        if 'argyle' in best_user_match['about_user']:
            user_found  = True
            best_user_match['users_url'] = snapshot_user(context, best_user_match['username'])
        page.wait_for_load_state('networkidle')

    if not user_found:
        # process the first users url
        best_user_match['users_url'] = snapshot_user(context, best_user_match['username'])
    return best_user_match


def search_in_github(name):
    github_fullname = f"fullname:{name}"
    title = f"Search · fullname:{name} · GitHub"
    total_users = 0

    with sync_playwright() as p:
        # browser = p.firefox.launch(headless=False, slow_mo=350)
        browser = p.firefox.launch()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f'https://github.com/search?q=fullname%3A%22{name}%22')
        try:
            section_text = page.eval_on_selector('div.codesearch-results h3', 'e => e.textContent')
            total_users = int(section_text.split()[0])
            print(total_users)
        except:
            print('no users were found.')
            best_user_match = None
        finally:
            # 'div#user_search_results '
            # process first 5 at most.
            if total_users > 5: 
                total_users = 5

            # evaluate search result's list.    
            if total_users > 0:
                best_user_match = look_for_best_match(context, page, total_users)
            else:
                print("there's no user to evaluate")
                best_user_match = None
            browser.close()

    return best_user_match