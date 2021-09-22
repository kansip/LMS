class MenuItem:
    def __init__(self, name, title, url):
        self.name = name
        self.title = title
        self.url = url

        self.is_active = False
        self.is_dropdown = False
        self.is_right = True


class DropdownItem(MenuItem):
    def __init__(self, name, title, url):
        super().__init__(name, title, url)

        self.items = []
        self.is_dropdown = True


REGISTER_PAGE_NAME = "register"
LOGIN_PAGE_NAME = "login"
USER_PAGE_NAME = "user"
LOGOUT_PAGE_NAME = "logout"

HOME_PAGE_NAME = "index"

USER_LIST_NAME =  "user_list"
USER_TASK_NAME =  "task_list"
COURSE_LIST_NAME =  "task_list"
login_menu_item = MenuItem(LOGIN_PAGE_NAME, "Вход", "/login")
register_menu_item = MenuItem(REGISTER_PAGE_NAME, "Регистрация", "/register")

my_user_menu_item = MenuItem(LOGOUT_PAGE_NAME, "Профиль", "/user/")
logout_menu_item = MenuItem(LOGOUT_PAGE_NAME, "Выход", "/logout")

home_menu_item = MenuItem(HOME_PAGE_NAME, "Главная", "/")
user_list_item = MenuItem(USER_LIST_NAME, "Список пользователей", "/user/list")
user_task_item = MenuItem(USER_TASK_NAME, "Список всех задач", "/task/list")
course_list_item = MenuItem(COURSE_LIST_NAME, "Мои курсы", "/course/list")

def get_context_menu(request, current_name):
    return {"left": get_context_left_menu(request, current_name),
            "right": get_context_right_menu(request, current_name)}


def get_context_left_menu(request, current_name):
    menu = [home_menu_item]

    if request.user.is_authenticated:
        menu.append(course_list_item)
        pass
        #print("menu")
        #menu.append(votes_menu_item)
        #menu.append(user_votes_menu_item)
        #menu.append(votes_editor_menu_item)
    else:
        menu.append(login_menu_item)
        menu.append(register_menu_item)

    if request.user.is_staff:  # teacher
        menu.append(user_list_item)
        menu.append(user_task_item)
    for item in menu:
        if item.name == current_name:
            item.is_active = True
        else:
            item.is_active = False

    return menu


def get_context_right_menu(request, current_name):
    menu = []

    if request.user.is_authenticated:
        my_user_menu_item.url = '/user/' + str(request.user.id)

        account_menu_item = DropdownItem("account", "Аккаунт", "")
        account_menu_item.items.append(my_user_menu_item)
        account_menu_item.items.append(logout_menu_item)

        account_menu_item.title = request.user.username
        menu.append(account_menu_item)

    for item in menu:
        if item.name == current_name:
            item.is_active = True
        else:
            item.is_active = False

    return menu
