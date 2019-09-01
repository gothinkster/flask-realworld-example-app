
import pytest

from conduit.articles.models import Category


@pytest.mark.usefixtures('db')
class TestCategory:
    """Category tests."""

    def test_get_categories(self):
        """Get categories."""
        category1 = Category(catname='music')
        category2 = Category(catname='sports')
        category1.save()
        category2.save()

        retrieved = Category.query.all()
        assert len(retrieved) == 2

    def test_append_children_category(self):
        """Test creation children category."""
        category = Category(catname='olympic games')
        category1 = Category(catname='Tennis')
        category.parents.append(category1)
        category.save()
        assert category.parents
        

    def test_create_category(self):
        """Test create category."""
        category = Category(catname='Goof')
        category.save()
        assert category


