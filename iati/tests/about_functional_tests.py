"""A module of functional tests for the about page and its sub pages."""
from django.utils.text import slugify
import pytest

ABOUT_PAGE = {
    'title': 'About',
    'heading': 'Test About Heading',
    'excerpt': 'This is an excerpt for the About page'
}
ABOUT_SUB_PAGE = {
    'page_type': 'About sub page',
    'title': 'test sub page',
    'heading': 'Test Sub Page',
    'excerpt': 'This is an excerpt for an About Sub page'
}
CASE_STUDY_INDEX_PAGE = {
    'page_type': 'Case study index page',
    'title': 'test case study index page',
    'heading': 'Test Case Study Index Page',
    'excerpt': 'This is an excerpt for a Case Study Index page'
}
HISTORY_PAGE = {
    'page_type': 'History page',
    'title': 'test history page',
    'heading': 'Test History Page',
    'excerpt': 'This is an excerpt for the History page'
}
PEOPLE_PAGE = {
    'page_type': 'People page',
    'title': 'test people page',
    'heading': 'Test People Page',
    'excerpt': 'This is an excerpt for the People page'
}
CASE_STUDY_PAGE = {
    'page_type': 'Case study page',
    'title': 'test case study page',
    'heading': 'Test Case Study Page',
    'excerpt': 'This is an excerpt for a Case Study page.'
}


def navigate_to_default_page_cms_section(admin_browser, default_page_title):
    """Navigate to the About page section of the CMS."""
    admin_browser.click_link_by_text('Pages')
    admin_browser.find_by_xpath('//span[@class="icon icon-arrow-right "]').click()
    admin_browser.find_by_text(default_page_title).click()


def enter_page_content(admin_browser, page_type, page_title):
    """Add title and slug to a page in the CMS."""
    admin_browser.find_by_text('English').click()
    admin_browser.fill('title_en', page_title)
    admin_browser.find_by_text('Promote').click()
    admin_browser.fill('slug_en', slugify(page_title))


def publish_page(admin_browser):
    """Publish page created in the CMS."""
    admin_browser.find_by_xpath('//div[@class="dropdown-toggle icon icon-arrow-up"]').click()
    admin_browser.find_by_text('Publish').click()


def create_about_child_page(admin_browser, page_type, page_title):
    """Create a child page in the CMS."""
    navigate_to_default_page_cms_section(admin_browser, 'About')
    admin_browser.find_by_text('Add child page').click()
    admin_browser.find_by_text(page_type).click()
    enter_page_content(admin_browser, page_type, page_title)
    publish_page(admin_browser)


def view_live_page(admin_browser, page_title):
    """Navigate to the published page on the site."""
    admin_browser.find_by_text(page_title).mouse_over()
    button_link = admin_browser.find_by_text('View live')
    href = button_link[0].__dict__['_element'].get_property('href')
    admin_browser.visit(href)


def fill_cms_content_field(admin_browser, page_title, cms_field, page_heading):
    """Add English heading to page title."""
    admin_browser.find_by_text(page_title).click()
    admin_browser.find_by_text('English').click()
    admin_browser.fill(cms_field, page_heading)


def edit_site_page(admin_browser, page_title, cms_field, cms_content):
    """Edit a page by adding content via the CMS."""
    fill_cms_content_field(admin_browser, page_title, cms_field, cms_content)
    publish_page(admin_browser)
    view_live_page(admin_browser, page_title)


@pytest.mark.django_db
class TestAboutPage():
    """A container for tests to check functionality of About pages and child pages."""

    def test_can_edit_about_page_heading(self, admin_browser):
        """Check that an existing About page heading can be edited."""
        navigate_to_default_page_cms_section(admin_browser, 'About')
        edit_site_page(admin_browser, ABOUT_PAGE['title'], 'heading_en', ABOUT_PAGE['heading'])
        assert admin_browser.find_by_text(ABOUT_PAGE['heading'])

    def test_can_edit_about_page_excerpt(self, admin_browser):
        """Check that an existing About page excerpt can be edited."""
        edit_site_page(admin_browser, ABOUT_PAGE['title'], 'excerpt_en', ABOUT_PAGE['excerpt'])
        assert admin_browser.find_by_text(ABOUT_PAGE['excerpt'])


@pytest.mark.django_db
class TestAboutChildPages():
    """A container for tests to check functionality of About child pages."""

    ABOUT_CHILD_PAGES = [
        ABOUT_SUB_PAGE,
        CASE_STUDY_INDEX_PAGE,
        HISTORY_PAGE,
        PEOPLE_PAGE
    ]

    @pytest.mark.parametrize('child_page', ABOUT_CHILD_PAGES)
    def test_can_create_about_child_pages(self, admin_browser, child_page):
        """Check that when an about child page is created it appears in the website."""
        create_about_child_page(admin_browser, child_page['page_type'], child_page['title'])
        view_live_page(admin_browser, child_page['title'])
        assert not admin_browser.is_text_present('Home')
        assert admin_browser.is_text_present(child_page['title'])

    @pytest.mark.parametrize('child_page', ABOUT_CHILD_PAGES)
    def test_can_edit_about_child_page_heading(self, admin_browser, child_page):
        """Check that About child page headings can be edited."""
        edit_site_page(admin_browser, child_page['title'], 'heading_en', child_page['heading'])
        assert admin_browser.find_by_text(child_page['heading'])

    @pytest.mark.parametrize('child_page', ABOUT_CHILD_PAGES)
    def test_can_edit_about_child_page_excerpt(self, admin_browser, child_page):
        """Check that About child page excerpts can be edited."""
        edit_site_page(admin_browser, child_page['title'], 'excerpt_en', child_page['excerpt'])
        assert admin_browser.find_by_text(child_page['excerpt'])


@pytest.mark.django_db
class TestCaseStudyIndexChildPageCreation():
    """A container for tests to check the ability to create Case Study pages."""

    def setup_case_study_index_page(self, admin_browser):
        """Create a Case Study Index page as a child of the About page."""
        case_study_index_page_title = 'test case study index page 2'
        create_about_child_page(admin_browser, CASE_STUDY_INDEX_PAGE['page_type'], case_study_index_page_title)

    def test_can_create_case_study_page(self, admin_browser):
        """Check that a Case Study page can be created as a child of the Case Study Index page."""
        self.setup_case_study_index_page(admin_browser)
        admin_browser.find_by_xpath('//td[@class="no-children"]').click()
        enter_page_content(admin_browser, CASE_STUDY_PAGE['page_type'], CASE_STUDY_PAGE['title'])
        publish_page(admin_browser)
        view_live_page(admin_browser, CASE_STUDY_PAGE['title'])
        assert admin_browser.is_text_present(CASE_STUDY_PAGE['title'])

    def test_can_edit_case_study_page_heading(self, admin_browser):
        """Check that Case Study page headings can be edited."""
        edit_site_page(admin_browser, CASE_STUDY_PAGE['title'], 'heading_en', CASE_STUDY_PAGE['heading'])
        assert admin_browser.find_by_text(CASE_STUDY_PAGE['heading'])
