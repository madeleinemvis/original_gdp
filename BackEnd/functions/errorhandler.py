class Error(Exception):
    """Base class for other exceptions"""
    pass


class NoObjectsError(Error):
    """No Documents Found in Collection"""
    pass


class NoCollectionsError(Error):
    """No Collections in Database"""