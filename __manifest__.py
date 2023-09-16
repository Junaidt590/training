{
    'name': "estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'view/estate_property_views.xml',
        'view/estate_form_view.xml',
        'view/estate_property_type.xml',
        'view/estate_property_tag.xml',
    ],
}