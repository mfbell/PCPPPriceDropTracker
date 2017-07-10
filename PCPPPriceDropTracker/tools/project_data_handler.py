"""PCPPPriceDropTracker project data handler module.

Handles all project related data.
To access project data, use PD like a dictionary, it self-saves on edit.

"""

__all__ = ["PDHandler", "PDPath", "PD"]


try:
    from .tools import main, Tools, CallbackOnEditDict, SelfSavingDict
except ImportError as e:
    try:
        from tools import main, Tools, CallbackOnEditDict, SelfSavingDict
    except Exception as e2:
        raise e


# Path of project_data.
PDPath = "X://coding//projects//PCPPPriceDropTracker//PCPPPriceDropTracker//project_data.json"

class PDHandler(SelfSavingDict):
    """Project Data Handler class.

    To include other methods in the future.

    """

    def __init__(self, path=PDPath):
        """Initialization

        path - Path of project data | string
            / Defaults to PDPath

        """
        super().__init__(path)
        return

# Pre-called PDHandler.
PD = PDHandler()

if __name__ == '__main__':
    main(__doc__)
