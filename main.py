import argparse
from osgeo import gdal
import numpy as np

parser = argparse.ArgumentParser(
    description="Calculate median of red channel for COG file."
)

parser.add_argument(
    "url",
    help="URL of COG file to process."
)

def print_median_for(band: gdal.Band):
    arr = band.ReadAsArray()
    median = np.nanmedian(arr)
    print(f"Median of {band.GetDescription()} band is: {median}")


def main(url: str):
    gd = gdal.Open(f"/vsicurl/{url}")
    
    for i in range(gd.RasterCount):
        band_n = i + 1
        band = gd.GetRasterBand(band_n)

        if not band:
            continue

        color_interpretation = band.GetColorInterpretation()
        description = band.GetDescription()

        if color_interpretation == gdal.GCI_RedBand or description == "Red":
            print_median_for(band)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args.url)
