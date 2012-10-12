from zope.component import getMultiAdapter
from plone.app.layout.navigation.interfaces import INavigationQueryBuilder
from Products.CMFCore.utils import getToolByName
from plone.formwidget.contenttree.source import ObjPathSource, ObjPathSourceBinder


class RootObjPathSource(ObjPathSource):

    def __init__(self, context, selectable_filter, navigation_tree_query=None):
        self.context = context        
        portal_tool = getToolByName(context, "portal_url")
        nav_root = portal_tool.getPortalObject()
        query_builder = getMultiAdapter((nav_root, self),
                                        INavigationQueryBuilder)
        query = query_builder()

        if navigation_tree_query is None:
            navigation_tree_query = {}

        # Copy path from selectable_filter into the navigation_tree_query
        # normally it does not make sense to show elements that wouldn't be
        # selectable anyway and are unneeded to navigate to selectable items
        if ('path' not in navigation_tree_query
                and 'path' in selectable_filter.criteria):
            navigation_tree_query['path'] = selectable_filter.criteria['path']

        query.update(navigation_tree_query)
        from logging import getLogger
        log = getLogger(__name__)
        log.info(query)
        self.navigation_tree_query = query
        self.selectable_filter = selectable_filter

        self.catalog = getToolByName(context, "portal_catalog")

        
        self.portal_path = portal_tool.getPortalPath()

class RootObjPathSourceBinder(ObjPathSourceBinder):
    path_source = RootObjPathSource