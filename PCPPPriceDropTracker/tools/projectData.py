"""Project Data Handler for PCPPPriceDropTracker."""

from .tools import main
from .dictionaries import SelfSavingFileDictionary


__all__ = ["PDPath", "PD", "pdname", "countries", "config"]

# Project Data Path
PDPath = ".\PCPPPriceDropTracker\project_data.json"
# Project Data loaded into a SelfSavingDict
PD = SelfSavingFileDictionary(PDPath)
# Project Name - Would like to change pdname to PDName at some point...
pdname = PD["project"]["name"]
# Countries supported by the project
countries = PD["project"]["sites"]
# Project config loaded into a SelfSavingDict
config = SelfSavingFileDictionary(PD["project"]["config_file"])

if __name__ == '__main__':
    main(__doc__)
