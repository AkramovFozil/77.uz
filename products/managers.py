from django.db import models
from rest_framework.exceptions import ValidationError


class CategoryManager(models.Manager):
    def get_root_categories(self):
        return self.filter(parent__isnull=True)

    def children(self, id):
        try:
            parent = self.get(guid=id)
        except self.model.DoesNotExist:
            raise ValidationError(
                {"product": f"Object with guid={id} does not exist."},
                code="DOES_NOT_EXIST",
            )
        return parent.child.all()

    def _build_tree(self, parent=None):
        categories = self.all()
        tree = []
        children = categories.filter(parent=parent)
        for child in children:
            sub_tree = self._build_tree(categories, parent=child)
            tree.append({
                'category': child,
                'children': sub_tree
            })
        return tree