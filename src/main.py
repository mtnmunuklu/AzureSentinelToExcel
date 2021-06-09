import sys
sys.path.append("../")

from src.app.azuresentinel import AzureSentinel

if __name__ == "__main__":
    sentinelconverter = AzureSentinel()
    sentinelconverter.read_from_file()
    sentinelconverter.write_to_excel()
