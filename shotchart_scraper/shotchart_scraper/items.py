import scrapy


def create_item_class(cls_name, fields):
    field_dict = {field: scrapy.Field() for field in fields}
    return type(str(cls_name), (scrapy.item.DictItem,), {'fields': field_dict})
