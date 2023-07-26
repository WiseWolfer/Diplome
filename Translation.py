from PyQt5.QtCore import QCoreApplication


def tr(text_to_translate):
    """text translation"""
    return QCoreApplication.translate('@default', text_to_translate)
