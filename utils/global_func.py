# словарь соответствия расширение=картинка
extention_icon_dict = {
    'unknown': 'ext_unknown.png',
    'pdf': 'ext_pdf.png',
    'xls': 'ext_excel.png',
    'xlsx': 'ext_excel.png',
    'xlsm': 'ext_excel.png',
    'doc': 'ext_word.png',
    'docx': 'ext_word.png',
    'jpg': 'ext_jpg.png'
}

def get_image_name_by_ext (extention):
    return extention_icon_dict[extention]
