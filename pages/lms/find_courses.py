from e2e_framework.page_object import PageObject
from selenium.common.exceptions import WebDriverException
from . import BASE_URL


class FindCoursesPage(PageObject):
    """
    Find courses page (main page of the LMS).
    """

    @property
    def name(self):
        return "lms.find_courses"

    @property
    def requirejs(self):
        return []

    @property
    def js_globals(self):
        return []

    def url(self):
        return BASE_URL

    def is_browser_on_page(self):
        return self.browser.title == "edX"

    def course_id_list(self):
        """
        Retrieve the list of available course IDs
        on the page.
        """
        return [el['id'] for el in self.css_find('article.course')]

    def go_to_course(self, course_id):
        """
        Navigate to the course with `course_id`.
        Currently the course id has the form
        edx/999/2013_Spring, but this could change.
        """

        # Try clicking the link directly
        try:
            css = 'a[href="/courses/{0}/about"]'.format(course_id)

            # In most browsers, there are multiple links
            # that match this selector, most without text
            # In IE 10, only the second one works.
            # In IE 9, there is only one link
            if len(self.css_find(css)) > 1:
                index = 1
            else:
                index = 0

            self.css_click(css, index=index)

        # Chrome gives an error that another element would receive the click.
        # So click higher up in the DOM
        except WebDriverException:
            # We need to escape forward slashes in the course_id
            # to create a valid CSS selector
            course_id = course_id.replace('/', '\/')
            self.css_click('article.course#{0}'.format(course_id))